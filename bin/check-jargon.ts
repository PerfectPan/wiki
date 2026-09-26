import { execFileSync } from "node:child_process";
import { lstatSync, readFileSync, readdirSync } from "node:fs";
import { isAbsolute, relative, resolve } from "node:path";

interface Rule {
  term: string;
  suggestion: string;
  exceptions: string[];
}

interface Finding {
  line: number;
  column: number;
  message: string;
}

const blank = (text: string): string => " ".repeat(text.length);
const isWikiPage = (path: string): boolean => path.startsWith("wiki/") && path.endsWith(".md");

function scan(content: string, rules: Rule[]): Finding[] {
  const findings: Finding[] = [];
  const lines = content.replace(/\r\n/g, "\n").split("\n");
  let frontmatter = lines[0] === "---";
  let proseField = false;
  let fence = "";
  let inComment = false;

  for (let index = 0; index < lines.length; index++) {
    let line = lines[index];
    if (frontmatter) {
      if (index === 0) continue;
      if (/^(---|\.\.\.)\s*$/.test(line)) {
        frontmatter = false;
        continue;
      }
      const field = line.match(/^([\w-]+):/);
      if (field) proseField = ["title", "description"].includes(field[1]);
      if (!proseField) continue;
    } else {
      if (/^\s*>/.test(line)) continue;
      const marker = line.match(/^\s*(?:[-+*]\s+|\d+[.)]\s+)?(`{3,}|~{3,})/);
      if (fence) {
        if (marker && marker[1][0] === fence[0] && marker[1].length >= fence.length &&
            line.slice(marker[0].length).trim() === "") fence = "";
        continue;
      }
      if (marker && !inComment) {
        fence = marker[1];
        continue;
      }
      const listItem = /^\s*(?:[-+*]\s+|\d+[.)]\s+)/.test(line);
      if ((/^( {4}|\t)/.test(line) && !listItem) || /^\s*\[[^\]]+\]:/.test(line)) continue;
    }

    // Mask code and link destinations without moving diagnostic columns.
    line = line.replace(/(`+)(.*?)\1(?!`)/g, blank)
      .replace(/\[\[([^\]\n]+)\]\]/g, (match, inside: string) => {
        const separator = inside.indexOf("|");
        return separator < 0 ? blank(match) : blank(match.slice(0, separator + 3)) + inside.slice(separator + 1) + "  ";
      })
      .replace(/\]\([^\n]*?\)/g, blank)
      .replace(/https?:\/\/[^\s<>]+/g, blank);

    const allowed = new Set<string>();
    let visible = "";
    let offset = 0;
    while (offset < line.length) {
      if (inComment) {
        const end = line.indexOf("-->", offset);
        const until = end < 0 ? line.length : end + 3;
        visible += blank(line.slice(offset, until));
        offset = until;
        if (end >= 0) inComment = false;
      } else {
        const start = line.indexOf("<!--", offset);
        if (start < 0) {
          visible += line.slice(offset);
          break;
        }
        visible += line.slice(offset, start);
        const end = line.indexOf("-->", start + 4);
        const comment = line.slice(start + 4, end < 0 ? undefined : end).trim();
        if (comment.startsWith("jargon-allow:")) {
          const directive = comment.match(/^jargon-allow:\s*([^;]+);\s*(\S.*)$/);
          const terms = directive?.[1].split(/[,，]/).map((term) => term.trim()) ?? [];
          if (end < 0 || !directive || terms.some((term) => !rules.some((rule) => rule.term === term))) {
            findings.push({ line: index + 1, column: start + 1, message: "jargon-allow 必须在同一行列出词表中的词，并在分号后说明保留理由" });
          } else {
            for (const term of terms) allowed.add(term);
          }
        }
        offset = start;
        inComment = true;
      }
    }
    visible = visible.replace(/<[^>]+>/g, blank);
    for (const rule of rules) {
      if (allowed.has(rule.term)) continue;
      let searchable = visible;
      for (const exception of rule.exceptions) searchable = searchable.replaceAll(exception, blank(exception));
      for (let at = searchable.indexOf(rule.term); at >= 0; at = searchable.indexOf(rule.term, at + rule.term.length)) {
        findings.push({ line: index + 1, column: at + 1, message: `“${rule.term}”：${rule.suggestion}` });
      }
    }
  }
  return findings;
}

function collectFiles(path: string): string[] {
  const stat = lstatSync(path);
  if (stat.isSymbolicLink()) return [];
  if (stat.isFile()) return path.endsWith(".md") ? [path] : [];
  return readdirSync(path).sort().flatMap((name) => collectFiles(resolve(path, name)));
}

function addedLines(diff: string): Set<number> {
  const result = new Set<number>();
  for (const match of diff.matchAll(/^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@/gm)) {
    const start = Number(match[1]);
    const count = match[2] === undefined ? 1 : Number(match[2]);
    for (let line = start; line < start + count; line++) result.add(line);
  }
  return result;
}

export function runJargonCheck(root: string, args: string[]): void {
  try {
    const rules: Rule[] = JSON.parse(readFileSync(resolve(root, "bin/jargon-rules.json"), "utf8"));
    const git = (...argv: string[]): string => execFileSync("git", argv, { cwd: root, encoding: "utf8", maxBuffer: 32 * 1024 * 1024 });
    let mode: "all" | "staged" | "base" = "all";
    let target = "wiki";
    let base = "";
    if (args[0] === "--staged" && args.length === 1) mode = "staged";
    else if (args[0] === "--base" && args.length === 2 && !args[1].startsWith("-")) {
      mode = "base";
      base = git("merge-base", args[1], "HEAD").trim();
    } else if (args.length === 1 && !args[0].startsWith("-")) target = args[0];
    else if (args.length !== 0) throw new Error("用法: bin/wiki check-jargon [path | --staged | --base <ref>]");

    let files: string[];
    const diffArgs = mode === "staged" ? ["--cached"] : [base];
    const untracked = new Set<string>();
    if (mode === "all") {
      const path = resolve(root, target);
      const rel = relative(root, path);
      if (isAbsolute(rel) || (rel !== "wiki" && !rel.startsWith("wiki/"))) throw new Error("用词检查只接受 wiki/ 下的页面或目录；原始素材与 prompt 原文不在检查范围内");
      files = collectFiles(path).map((file) => relative(root, file)).filter(isWikiPage);
    } else {
      files = git("diff", ...diffArgs, "--name-only", "-z", "--no-renames", "--diff-filter=ACM", "--", "wiki/")
        .split("\0").filter(isWikiPage);
      if (mode === "base") {
        for (const file of git("ls-files", "--others", "--exclude-standard", "-z", "--", "wiki/").split("\0").filter(isWikiPage)) untracked.add(file);
        files = [...new Set([...files, ...untracked])];
      }
    }

    let count = 0;
    for (const file of files.sort()) {
      const content = mode === "staged" ? git("show", `:${file}`) : readFileSync(resolve(root, file), "utf8");
      // Parse the whole document so changed lines retain their Markdown context.
      const changed = mode === "all" || untracked.has(file) ? null : addedLines(git("diff", ...diffArgs, "--no-ext-diff", "--no-textconv", "--no-renames", "--unified=0", "--", file));
      for (const finding of scan(content, rules)) {
        if (changed && !changed.has(finding.line)) continue;
        console.error(`${file}:${finding.line}:${finding.column}: ${finding.message}`);
        count++;
      }
    }
    console.log(`用词检查完成: ${files.length} 个文件，${count} 个问题${mode === "all" ? "" : "（仅新增或改写行）"}`);
    if (count > 0) process.exitCode = 1;
  } catch (error) {
    console.error(`用词检查失败: ${(error as Error).message}`);
    process.exitCode = 1;
  }
}
