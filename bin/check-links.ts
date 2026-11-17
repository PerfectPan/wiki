import { existsSync, lstatSync, readFileSync, readdirSync } from "node:fs";
import { dirname, isAbsolute, normalize, relative, resolve } from "node:path";

export interface LinkIssue {
  file: string;
  line: number;
  level: "error" | "warning";
  message: string;
}

export interface LinkCheckResult {
  filesChecked: number;
  issues: LinkIssue[];
  errorCount: number;
  warningCount: number;
}

const isMarkdownFile = (relPath: string): boolean => relPath.endsWith(".md");

function walkMarkdown(root: string, dir: string, out: string[]): void {
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    if (entry.name.startsWith(".") || entry.name === "node_modules") continue;
    const full = resolve(dir, entry.name);
    if (entry.isDirectory()) {
      walkMarkdown(root, full, out);
    } else if (entry.isFile() && isMarkdownFile(entry.name)) {
      out.push(relative(root, full).replace(/\\/g, "/"));
    }
  }
}

function buildStemIndex(allMd: string[]): Map<string, string[]> {
  const index = new Map<string, string[]>();
  const add = (key: string, path: string): void => {
    const list = index.get(key) ?? [];
    list.push(path);
    index.set(key, list);
  };
  for (const rel of allMd) {
    const stem = rel.slice(0, -3);
    const base = stem.split("/").pop() ?? stem;
    add(stem, rel);
    add(base, rel);
  }
  return index;
}

function parseSourceRefs(content: string): { line: number; value: string }[] {
  const lines = content.replace(/\r\n/g, "\n").split("\n");
  if (lines[0]?.trim() !== "---") return [];

  const refs: { line: number; value: string }[] = [];
  let inRefs = false;
  for (let i = 1; i < lines.length; i++) {
    const line = lines[i];
    if (/^(---|\.\.\.)\s*$/.test(line)) break;

    const itemMatch = line.match(/^\s+-\s+(.*)$/);
    if (itemMatch && inRefs) {
      const value = itemMatch[1].trim().replace(/^['"]|['"]$/g, "");
      if (value) refs.push({ line: i + 1, value });
      continue;
    }

    const kvMatch = line.match(/^([a-zA-Z_][a-zA-Z0-9_]*):\s*(.*)$/);
    if (kvMatch) {
      inRefs = kvMatch[1] === "source_refs" && kvMatch[2].trim() === "";
    }
  }
  return refs;
}

function resolveWikilink(
  root: string,
  target: string,
  stemIndex: Map<string, string[]>,
  isEmbed: boolean,
  fileDir: string,
): string | null {
  if (isEmbed) {
    const candidates = [
      resolve(root, "raw/assets", target),
      resolve(fileDir, target),
      resolve(root, target),
    ];
    for (const c of candidates) {
      if (existsSync(c)) return relative(root, c).replace(/\\/g, "/");
    }
    return null;
  }

  const exactCandidates = [target, `${target}.md`];
  for (const c of exactCandidates) {
    const abs = resolve(root, c);
    if (existsSync(abs) && lstatSync(abs).isFile()) {
      return c.replace(/\\/g, "/");
    }
  }

  const byStem = stemIndex.get(target);
  if (byStem && byStem.length > 0) {
    return byStem[0];
  }
  return null;
}

function resolveMarkdownDest(root: string, fileDir: string, dest: string): boolean {
  const cleaned = dest.trim().split(/\s+/)[0].replace(/^<|>$/g, "");
  if (!cleaned || /^(https?:\/\/|mailto:|file:\/\/|#)/i.test(cleaned)) {
    return true;
  }
  const withoutAnchor = cleaned.split("#")[0];
  if (!withoutAnchor) return true;

  const relToFile = normalize(resolve(fileDir, withoutAnchor));
  const relToRoot = normalize(resolve(root, withoutAnchor));
  return existsSync(relToFile) || existsSync(relToRoot);
}

function scanFileLinks(
  root: string,
  relPath: string,
  stemIndex: Map<string, string[]>,
  indexTargets: Set<string>,
): LinkIssue[] {
  const absPath = resolve(root, relPath);
  const content = readFileSync(absPath, "utf8");
  const lines = content.replace(/\r\n/g, "\n").split("\n");
  const fileDir = dirname(absPath);
  const issues: LinkIssue[] = [];

  // Check frontmatter source_refs on wiki pages.
  if (relPath.startsWith("wiki/")) {
    for (const ref of parseSourceRefs(content)) {
      if (/^https?:\/\//i.test(ref.value)) continue;
      const exists =
        existsSync(resolve(root, ref.value)) ||
        existsSync(resolve(root, `${ref.value}.md`));
      if (!exists) {
        const isRepoPath = ref.value.startsWith("raw/") || ref.value.startsWith("wiki/");
        issues.push({
          file: relPath,
          line: ref.line,
          level: isRepoPath ? "error" : "warning",
          message: `source_refs 路径不存在: ${ref.value}`,
        });
      }
    }
  }

  let frontmatter = lines[0]?.trim() === "---";
  let fence = "";
  let inComment = false;

  for (let i = 0; i < lines.length; i++) {
    let line = lines[i];
    if (frontmatter) {
      if (i > 0 && /^(---|\.\.\.)\s*$/.test(line)) {
        frontmatter = false;
      }
      continue;
    }

    const marker = line.match(/^\s*(?:[-+*]\s+|\d+[.)]\s+)?(`{3,}|~{3,})/);
    if (fence) {
      if (
        marker &&
        marker[1][0] === fence[0] &&
        marker[1].length >= fence.length &&
        line.slice(marker[0].length).trim() === ""
      ) {
        fence = "";
      }
      continue;
    }
    if (marker && !inComment) {
      fence = marker[1];
      continue;
    }

    const listItem = /^\s*(?:[-+*]\s+|\d+[.)]\s+)/.test(line);
    if (/^( {4}|\t)/.test(line) && !listItem) continue;

    // Strip HTML comments across lines.
    let visible = "";
    let offset = 0;
    while (offset < line.length) {
      if (inComment) {
        const end = line.indexOf("-->", offset);
        if (end < 0) {
          offset = line.length;
        } else {
          offset = end + 3;
          inComment = false;
        }
      } else {
        const start = line.indexOf("<!--", offset);
        if (start < 0) {
          visible += line.slice(offset);
          break;
        }
        visible += line.slice(offset, start);
        offset = start + 4;
        inComment = true;
      }
    }

    // Strip inline code spans so code examples aren't treated as links.
    visible = visible.replace(/(`+)(.*?)\1(?!`)/g, "");

    // 1. Scan ![[embed]] and [[wikilink]]
    const wikiRe = /(!?)\[\[([^\]\n]+)\]\]/g;
    let wm: RegExpExecArray | null;
    while ((wm = wikiRe.exec(visible)) !== null) {
      const isEmbed = wm[1] === "!";
      const rawInside = wm[2];
      const normalizedInside = rawInside.replace(/\\\|/g, "|");
      const target = normalizedInside.split("|")[0].split("#")[0].trim();
      if (!target) continue;

      const resolved = resolveWikilink(root, target, stemIndex, isEmbed, fileDir);
      if (resolved) {
        if (relPath === "index.md" && !isEmbed) {
          indexTargets.add(resolved);
        }
      } else {
        const isHardError = isEmbed || target.includes("/") || relPath === "index.md";
        issues.push({
          file: relPath,
          line: i + 1,
          level: isHardError ? "error" : "warning",
          message: isEmbed
            ? `嵌入资源不存在: ![[${rawInside}]]`
            : `断链 wikilink: [[${rawInside}]]`,
        });
      }
    }

    // 2. Scan [text](dest) and ![alt](dest) after stripping wikilinks
    const noWiki = visible.replace(/!?\[\[[^\]\n]+\]\]/g, "");
    const mdRe = /!?\[[^\]\n]*\]\(([^)\n]+)\)/g;
    let mm: RegExpExecArray | null;
    while ((mm = mdRe.exec(noWiki)) !== null) {
      const dest = mm[1];
      if (!resolveMarkdownDest(root, fileDir, dest)) {
        issues.push({
          file: relPath,
          line: i + 1,
          level: "error",
          message: `断链 Markdown 链接: (${dest})`,
        });
      }
    }
  }

  return issues;
}

export function checkLinks(root: string, targetArg?: string): LinkCheckResult {
  const allMd: string[] = [];
  walkMarkdown(root, root, allMd);
  allMd.sort();

  const stemIndex = buildStemIndex(allMd);
  const indexTargets = new Set<string>();
  const issues: LinkIssue[] = [];

  let filesToScan: string[];
  let checkIndexCoverage = false;

  if (targetArg) {
    const absTarget = isAbsolute(targetArg) ? targetArg : resolve(root, targetArg);
    if (!existsSync(absTarget)) {
      throw new Error(`目标不存在: ${targetArg}`);
    }
    const stat = lstatSync(absTarget);
    if (stat.isDirectory()) {
      filesToScan = [];
      walkMarkdown(root, absTarget, filesToScan);
      filesToScan.sort();
    } else {
      filesToScan = [relative(root, absTarget).replace(/\\/g, "/")];
    }
  } else {
    checkIndexCoverage = true;
    filesToScan = allMd.filter((p) => !p.startsWith("raw/"));
  }

  for (const rel of filesToScan) {
    issues.push(...scanFileLinks(root, rel, stemIndex, indexTargets));
  }

  if (checkIndexCoverage && existsSync(resolve(root, "index.md"))) {
    const wikiPages = allMd.filter((p) => p.startsWith("wiki/"));
    for (const page of wikiPages) {
      if (!indexTargets.has(page)) {
        issues.push({
          file: "index.md",
          line: 1,
          level: "error",
          message: `index.md 漏收页面: ${page}`,
        });
      }
    }
  }

  const errorCount = issues.filter((i) => i.level === "error").length;
  const warningCount = issues.filter((i) => i.level === "warning").length;
  return { filesChecked: filesToScan.length, issues, errorCount, warningCount };
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

  const byFile = new Map<string, LinkIssue[]>();
  for (const issue of result.issues) {
    if (quietWarnings && issue.level === "warning") continue;
    const list = byFile.get(issue.file) ?? [];
    list.push(issue);
    byFile.set(issue.file, list);
  }

  for (const [file, fileIssues] of byFile) {
    const hasError = fileIssues.some((i) => i.level === "error");
    const header = hasError ? `❌ ${file}` : `⚠️  ${file}`;
    const log = hasError ? console.error : console.log;
    log(`\n${header}`);
    for (const issue of fileIssues) {
      const fn = issue.level === "error" ? console.error : console.log;
      fn(`  [${issue.level}] L${issue.line}: ${issue.message}`);
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
