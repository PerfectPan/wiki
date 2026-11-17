import { existsSync, lstatSync, readFileSync, readdirSync } from "node:fs";
import { dirname, isAbsolute, normalize, relative, resolve } from "node:path";

export interface LinkIssue {
  readonly file: string;
  readonly line: number;
  readonly level: "error" | "warning";
  readonly message: string;
}

export interface LinkCheckResult {
  readonly filesChecked: number;
  readonly issues: readonly LinkIssue[];
  readonly errorCount: number;
  readonly warningCount: number;
}

interface VisibleLine {
  readonly line: number;
  readonly text: string;
}

interface FileScanResult {
  readonly issues: readonly LinkIssue[];
  readonly indexTargets: readonly string[];
}

const toPosix = (p: string): string => p.replace(/\\/g, "/");
const isMarkdownFile = (relPath: string): boolean => relPath.endsWith(".md");

const walkMarkdown = (root: string, dir: string): readonly string[] =>
  readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    if (entry.name.startsWith(".") || entry.name === "node_modules") return [];
    const full = resolve(dir, entry.name);
    if (entry.isDirectory()) return walkMarkdown(root, full);
    return entry.isFile() && isMarkdownFile(entry.name) ? [toPosix(relative(root, full))] : [];
  });

const buildStemIndex = (allMd: readonly string[]): ReadonlyMap<string, readonly string[]> =>
  allMd.reduce((acc, rel) => {
    const stem = rel.slice(0, -3);
    const base = stem.split("/").pop() ?? stem;
    for (const key of [stem, base]) {
      acc.set(key, [...(acc.get(key) ?? []), rel]);
    }
    return acc;
  }, new Map<string, readonly string[]>());

const parseSourceRefs = (content: string): readonly { line: number; value: string }[] => {
  const lines = content.replace(/\r\n/g, "\n").split("\n");
  if (lines[0]?.trim() !== "---") return [];

  const endIdx = lines.findIndex((l, i) => i > 0 && /^(---|\.\.\.)\s*$/.test(l));
  const fmLines = endIdx === -1 ? [] : lines.slice(1, endIdx);

  return fmLines.reduce<{ inRefs: boolean; refs: readonly { line: number; value: string }[] }>(
    (state, line, idx) => {
      const itemMatch = line.match(/^\s+-\s+(.*)$/);
      if (itemMatch && state.inRefs) {
        const value = itemMatch[1].trim().replace(/^['"]|['"]$/g, "");
        return value
          ? { ...state, refs: [...state.refs, { line: idx + 2, value }] }
          : state;
      }
      const kvMatch = line.match(/^([a-zA-Z_][a-zA-Z0-9_]*):\s*(.*)$/);
      return kvMatch
        ? { ...state, inRefs: kvMatch[1] === "source_refs" && kvMatch[2].trim() === "" }
        : state;
    },
    { inRefs: false, refs: [] },
  ).refs;
};

const stripComments = (
  line: string,
  initiallyInComment: boolean,
): { visible: string; inComment: boolean } => {
  const step = (offset: number, inComment: boolean, acc: string): { visible: string; inComment: boolean } => {
    if (offset >= line.length) return { visible: acc, inComment };
    if (inComment) {
      const end = line.indexOf("-->", offset);
      return end < 0
        ? { visible: acc, inComment: true }
        : step(end + 3, false, acc);
    }
    const start = line.indexOf("<!--", offset);
    return start < 0
      ? { visible: acc + line.slice(offset), inComment: false }
      : step(start + 4, true, acc + line.slice(offset, start));
  };
  return step(0, initiallyInComment, "");
};

const extractVisibleLines = (content: string): readonly VisibleLine[] => {
  const lines = content.replace(/\r\n/g, "\n").split("\n");
  const initialState = {
    frontmatter: lines[0]?.trim() === "---",
    fence: "",
    inComment: false,
    visible: [] as readonly VisibleLine[],
  };

  return lines.reduce((state, line, idx) => {
    if (state.frontmatter) {
      const closed = idx > 0 && /^(---|\.\.\.)\s*$/.test(line);
      return closed ? { ...state, frontmatter: false } : state;
    }

    const marker = line.match(/^\s*(?:[-+*]\s+|\d+[.)]\s+)?(`{3,}|~{3,})/);
    if (state.fence) {
      const closes =
        marker &&
        marker[1][0] === state.fence[0] &&
        marker[1].length >= state.fence.length &&
        line.slice(marker[0].length).trim() === "";
      return closes ? { ...state, fence: "" } : state;
    }
    if (marker && !state.inComment) {
      return { ...state, fence: marker[1] };
    }

    const listItem = /^\s*(?:[-+*]\s+|\d+[.)]\s+)/.test(line);
    if (/^( {4}|\t)/.test(line) && !listItem) return state;

    const { visible, inComment } = stripComments(line, state.inComment);
    const withoutInlineCode = visible.replace(/(`+)(.*?)\1(?!`)/g, "");
    return {
      ...state,
      inComment,
      visible: [...state.visible, { line: idx + 1, text: withoutInlineCode }],
    };
  }, initialState).visible;
};

const resolveWikilink = (
  root: string,
  target: string,
  stemIndex: ReadonlyMap<string, readonly string[]>,
  isEmbed: boolean,
  fileDir: string,
): string | null => {
  if (isEmbed) {
    const found = [
      resolve(root, "raw/assets", target),
      resolve(fileDir, target),
      resolve(root, target),
    ].find((candidate) => existsSync(candidate));
    return found ? toPosix(relative(root, found)) : null;
  }

  const exact = [target, `${target}.md`].find((candidate) => {
    const abs = resolve(root, candidate);
    return existsSync(abs) && lstatSync(abs).isFile();
  });
  if (exact) return toPosix(exact);

  return stemIndex.get(target)?.[0] ?? null;
};

const isValidMarkdownDest = (root: string, fileDir: string, dest: string): boolean => {
  const cleaned = dest.trim().split(/\s+/)[0].replace(/^<|>$/g, "");
  if (!cleaned || /^(https?:\/\/|mailto:|file:\/\/|#)/i.test(cleaned)) return true;
  const withoutAnchor = cleaned.split("#")[0];
  if (!withoutAnchor) return true;
  return (
    existsSync(normalize(resolve(fileDir, withoutAnchor))) ||
    existsSync(normalize(resolve(root, withoutAnchor)))
  );
};

const checkSourceRefs = (root: string, relPath: string, content: string): readonly LinkIssue[] =>
  relPath.startsWith("wiki/")
    ? parseSourceRefs(content).flatMap((ref) => {
        if (/^https?:\/\//i.test(ref.value)) return [];
        const exists =
          existsSync(resolve(root, ref.value)) || existsSync(resolve(root, `${ref.value}.md`));
        if (exists) return [];
        const isRepoPath = ref.value.startsWith("raw/") || ref.value.startsWith("wiki/");
        return [
          {
            file: relPath,
            line: ref.line,
            level: isRepoPath ? "error" : "warning",
            message: `source_refs 路径不存在: ${ref.value}`,
          },
        ];
      })
    : [];

const scanVisibleLine = (
  root: string,
  relPath: string,
  fileDir: string,
  stemIndex: ReadonlyMap<string, readonly string[]>,
  { line, text }: VisibleLine,
): FileScanResult => {
  const wikiMatches = [...text.matchAll(/(!?)\[\[([^\]\n]+)\]\]/g)];
  const wikiResults = wikiMatches.map((m) => {
    const isEmbed = m[1] === "!";
    const rawInside = m[2];
    const target = rawInside.replace(/\\\|/g, "|").split("|")[0].split("#")[0].trim();
    if (!target) return { issue: null, indexTarget: null };

    const resolved = resolveWikilink(root, target, stemIndex, isEmbed, fileDir);
    if (resolved) {
      return {
        issue: null,
        indexTarget: relPath === "index.md" && !isEmbed ? resolved : null,
      };
    }
    const isHardError = isEmbed || target.includes("/") || relPath === "index.md";
    return {
      issue: {
        file: relPath,
        line,
        level: isHardError ? ("error" as const) : ("warning" as const),
        message: isEmbed ? `嵌入资源不存在: ![[${rawInside}]]` : `断链 wikilink: [[${rawInside}]]`,
      },
      indexTarget: null,
    };
  });

  const withoutWiki = text.replace(/!?\[\[[^\]\n]+\]\]/g, "");
  const mdIssues: readonly LinkIssue[] = [...withoutWiki.matchAll(/!?\[[^\]\n]*\]\(([^)\n]+)\)/g)]
    .filter((m) => !isValidMarkdownDest(root, fileDir, m[1]))
    .map((m) => ({
      file: relPath,
      line,
      level: "error",
      message: `断链 Markdown 链接: (${m[1]})`,
    }));

  return {
    issues: [
      ...wikiResults.flatMap((r) => (r.issue ? [r.issue] : [])),
      ...mdIssues,
    ],
    indexTargets: wikiResults.flatMap((r) => (r.indexTarget ? [r.indexTarget] : [])),
  };
};

const scanFile = (
  root: string,
  relPath: string,
  stemIndex: ReadonlyMap<string, readonly string[]>,
): FileScanResult => {
  const absPath = resolve(root, relPath);
  const content = readFileSync(absPath, "utf8");
  const fileDir = dirname(absPath);

  const lineResults = extractVisibleLines(content).map((vl) =>
    scanVisibleLine(root, relPath, fileDir, stemIndex, vl),
  );

  return {
    issues: [
      ...checkSourceRefs(root, relPath, content),
      ...lineResults.flatMap((r) => r.issues),
    ],
    indexTargets: lineResults.flatMap((r) => r.indexTargets),
  };
};

const resolveFilesToScan = (
  root: string,
  allMd: readonly string[],
  targetArg?: string,
): { files: readonly string[]; checkIndexCoverage: boolean } => {
  if (!targetArg) {
    return {
      files: allMd.filter((p) => !p.startsWith("raw/")),
      checkIndexCoverage: true,
    };
  }
  const absTarget = isAbsolute(targetArg) ? targetArg : resolve(root, targetArg);
  if (!existsSync(absTarget)) {
    throw new Error(`目标不存在: ${targetArg}`);
  }
  return lstatSync(absTarget).isDirectory()
    ? { files: [...walkMarkdown(root, absTarget)].sort(), checkIndexCoverage: false }
    : { files: [toPosix(relative(root, absTarget))], checkIndexCoverage: false };
};

export function checkLinks(root: string, targetArg?: string): LinkCheckResult {
  const allMd = [...walkMarkdown(root, root)].sort();
  const stemIndex = buildStemIndex(allMd);
  const { files, checkIndexCoverage } = resolveFilesToScan(root, allMd, targetArg);

  const fileResults = files.map((rel) => scanFile(root, rel, stemIndex));
  const indexTargets = new Set(fileResults.flatMap((r) => r.indexTargets));

  const coverageIssues: readonly LinkIssue[] =
    checkIndexCoverage && existsSync(resolve(root, "index.md"))
      ? allMd
          .filter((p) => p.startsWith("wiki/") && !indexTargets.has(p))
          .map((page) => ({
            file: "index.md",
            line: 1,
            level: "error" as const,
            message: `index.md 漏收页面: ${page}`,
          }))
      : [];

  const issues = [...fileResults.flatMap((r) => r.issues), ...coverageIssues];
  const errorCount = issues.filter((i) => i.level === "error").length;
  const warningCount = issues.filter((i) => i.level === "warning").length;

  return { filesChecked: files.length, issues, errorCount, warningCount };
}

export function runLinksCheck(root: string, args: string[]): void {
  const quietWarnings = args.includes("--errors-only");
  const targetArg = args.find((a) => !a.startsWith("-"));

  let result: LinkCheckResult;
  try {
    result = checkLinks(root, targetArg);
  } catch (err) {
    console.error((err as Error).message);
    process.exit(1);
  }

  const visibleIssues = result.issues.filter((i) => !(quietWarnings && i.level === "warning"));
  const grouped = visibleIssues.reduce((acc, issue) => {
    acc.set(issue.file, [...(acc.get(issue.file) ?? []), issue]);
    return acc;
  }, new Map<string, readonly LinkIssue[]>());

  for (const [file, fileIssues] of grouped) {
    const hasError = fileIssues.some((i) => i.level === "error");
    const logHeader = hasError ? console.error : console.log;
    logHeader(`\n${hasError ? "❌" : "⚠️ "} ${file}`);
    for (const issue of fileIssues) {
      const logLine = issue.level === "error" ? console.error : console.log;
      logLine(`  [${issue.level}] L${issue.line}: ${issue.message}`);
    }
  }

  console.log(`\n---`);
  console.log(
    `链接检查完成: ${result.filesChecked} 个文件，${result.errorCount} 个错误，${result.warningCount} 个警告`,
  );
  if (result.errorCount > 0) {
    process.exit(1);
  }
}
