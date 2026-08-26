#!/usr/bin/env node

import { readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { execSync } from "node:child_process";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const ROOT = resolve(__dirname, "..");

const HELP_TEXT = `wiki CLI

用法:
  bin/wiki help
  bin/wiki ingest <source>
  bin/wiki check [path]

命令:
  ingest    抓取来源并存入 raw/sources/
  check     校验 Markdown 文件的 frontmatter 是否符合 SCHEMA 规范

工作流引导见 .agents/skills/
`;

const VALID_TYPES = ["topic", "synthesis", "comparison"] as const;
const VALID_CATEGORIES = [
  "frontend",
  "ai",
  "languages",
  "systems",
  "algorithms",
  "architecture",
  "tooling",
  "product",
  "career",
  "life",
] as const;

const REQUIRED_FIELDS = [
  "title",
  "type",
  "category",
  "created",
  "updated",
  "tags",
  "source_refs",
] as const;

interface Frontmatter {
  [key: string]: string | string[];
}

interface CheckIssue {
  level: "error" | "warning";
  message: string;
}

function die(message: string): never {
  console.error(message);
  process.exit(1);
}

/**
 * 解析 Markdown 文件的 YAML frontmatter。
 * 支持简单的 key: value 和 key: 后跟缩进列表的格式。
 */
function parseFrontmatter(content: string): Frontmatter | null {
  const lines = content.split("\n");
  if (lines[0]?.trim() !== "---") {
    return null;
  }

  const fm: Frontmatter = {};
  let i = 1;
  let currentKey: string | null = null;

  while (i < lines.length) {
    const line = lines[i];

    if (line.trim() === "---") {
      break;
    }

    // 数组项：以 "- " 开头
    const arrayItemMatch = line.match(/^\s+-\s+(.*)$/);
    if (arrayItemMatch && currentKey) {
      const value = arrayItemMatch[1].trim();
      const existing = fm[currentKey];
      if (Array.isArray(existing)) {
        existing.push(value);
      } else {
        fm[currentKey] = [value];
      }
      i++;
      continue;
    }

    // key: value 或 key:
    const kvMatch = line.match(/^([a-zA-Z_][a-zA-Z0-9_]*):\s*(.*)$/);
    if (kvMatch) {
      const key = kvMatch[1];
      const value = kvMatch[2].trim();
      if (value === "") {
        // 可能是空数组或后续有缩进列表
        fm[key] = [];
        currentKey = key;
      } else if (value === "[]") {
        fm[key] = [];
        currentKey = null;
      } else if (value.startsWith("[") && value.endsWith("]")) {
        // 内联数组: [a, b, c]
        const inner = value.slice(1, -1).trim();
        if (inner === "") {
          fm[key] = [];
        } else {
          fm[key] = inner.split(",").map((s) => s.trim());
        }
        currentKey = null;
      } else {
        fm[key] = value;
        currentKey = null;
      }
    }

    i++;
  }

  return fm;
}

/**
 * 校验单个文件的 frontmatter。
 */
function checkFile(filePath: string): CheckIssue[] {
  const issues: CheckIssue[] = [];
  const relPath = relative(ROOT, filePath);

  let content: string;
  try {
    content = readFileSync(filePath, "utf8");
  } catch {
    issues.push({ level: "error", message: "无法读取文件" });
    return issues;
  }

  const fm = parseFrontmatter(content);
  if (fm === null) {
    issues.push({ level: "error", message: "缺少 frontmatter（没有以 --- 开头的 YAML 块）" });
    return issues;
  }

  // 1. 必填字段检查
  for (const field of REQUIRED_FIELDS) {
    if (!(field in fm)) {
      issues.push({ level: "error", message: `缺少必填字段: ${field}` });
    }
  }

  // 2. type 枚举检查
  const type = fm["type"];
  if (typeof type === "string" && !VALID_TYPES.includes(type as (typeof VALID_TYPES)[number])) {
    issues.push({
      level: "error",
      message: `type 值无效: "${type}"，必须是 ${VALID_TYPES.join(" / ")} 之一`,
    });
  }

  // 3. category 枚举检查
  const category = fm["category"];
  if (typeof category === "string" && !VALID_CATEGORIES.includes(category as (typeof VALID_CATEGORIES)[number])) {
    issues.push({
      level: "error",
      message: `category 值无效: "${category}"，必须是 ${VALID_CATEGORIES.join(" / ")} 之一`,
    });
  }

  // 4. type 与目录一致性
  if (typeof type === "string") {
    const dir = relPath.split("/")[1]; // wiki/topics/... -> topics
    const expectedType =
      dir === "topics" ? "topic" : dir === "syntheses" ? "synthesis" : dir === "comparisons" ? "comparison" : null;
    if (expectedType && type !== expectedType) {
      issues.push({
        level: "error",
        message: `type 与目录不一致: type=${type}，目录 ${dir}/ 期望 ${expectedType}`,
      });
    }
  }

  // 5. category 与子目录一致性
  if (typeof category === "string") {
    const subdir = relPath.split("/")[2]; // wiki/topics/frontend/... -> frontend
    if (subdir && category !== subdir) {
      issues.push({
        level: "error",
        message: `category 与子目录不一致: category=${category}，子目录是 ${subdir}`,
      });
    }
  }

  // 6. 日期格式检查
  const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
  for (const field of ["created", "updated"] as const) {
    const value = fm[field];
    if (typeof value === "string" && !dateRegex.test(value)) {
      issues.push({
        level: "error",
        message: `${field} 日期格式无效: "${value}"，必须是 YYYY-MM-DD`,
      });
    }
  }

  // 7. tags 必须是数组
  if ("tags" in fm && !Array.isArray(fm["tags"])) {
    issues.push({ level: "error", message: "tags 必须是数组格式" });
  }

  // 8. source_refs 必须是数组
  if ("source_refs" in fm && !Array.isArray(fm["source_refs"])) {
    issues.push({ level: "error", message: "source_refs 必须是数组格式" });
  }

  // 9. description 建议有（warning）
  if (!("description" in fm)) {
    issues.push({ level: "warning", message: "缺少 description 字段，建议补上一句话摘要" });
  }

  // 10. OKF 字段一致性（warning）
  if ("resource" in fm && "source_refs" in fm) {
    const resource = fm["resource"];
    const sourceRefs = fm["source_refs"];
    if (Array.isArray(resource) && Array.isArray(sourceRefs)) {
      const r = [...resource].sort();
      const s = [...sourceRefs].sort();
      if (JSON.stringify(r) !== JSON.stringify(s)) {
        issues.push({
          level: "warning",
          message: "resource 与 source_refs 内容不一致，OKF 导出时可能有问题",
        });
      }
    }
  }

  if ("timestamp" in fm && "updated" in fm) {
    const timestamp = fm["timestamp"];
    const updated = fm["updated"];
    if (typeof timestamp === "string" && typeof updated === "string" && timestamp !== updated) {
      issues.push({
        level: "warning",
        message: `timestamp (${timestamp}) 与 updated (${updated}) 不一致`,
      });
    }
  }

  return issues;
}

/**
 * 递归收集目录下的所有 .md 文件。
 */
function collectMarkdownFiles(dir: string): string[] {
  const result: string[] = [];
  const entries = readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = resolve(dir, entry.name);
    if (entry.isDirectory()) {
      result.push(...collectMarkdownFiles(fullPath));
    } else if (entry.isFile() && entry.name.endsWith(".md")) {
      result.push(fullPath);
    }
  }
  return result;
}

function runCheck(targetPath?: string): void {
  const target = targetPath ? resolve(ROOT, targetPath) : resolve(ROOT, "wiki");

  let files: string[];
  try {
    const stat = statSync(target);
    if (stat.isFile()) {
      files = [target];
    } else if (stat.isDirectory()) {
      files = collectMarkdownFiles(target);
    } else {
      die(`路径既不是文件也不是目录: ${target}`);
    }
  } catch {
    die(`路径不存在: ${target}`);
  }

  let errorCount = 0;
  let warningCount = 0;

  for (const file of files) {
    const issues = checkFile(file);
    if (issues.length === 0) continue;

    const relPath = relative(ROOT, file);
    const fileErrors = issues.filter((i) => i.level === "error");
    const fileWarnings = issues.filter((i) => i.level === "warning");

    if (fileErrors.length > 0) {
      errorCount += fileErrors.length;
      console.error(`\n❌ ${relPath}`);
      for (const issue of fileErrors) {
        console.error(`  [error] ${issue.message}`);
      }
    }

    if (fileWarnings.length > 0) {
      warningCount += fileWarnings.length;
      console.log(`\n⚠️  ${relPath}`);
      for (const issue of fileWarnings) {
        console.log(`  [warning] ${issue.message}`);
      }
    }
  }

  console.log(`\n---`);
  console.log(`校验完成: ${files.length} 个文件，${errorCount} 个错误，${warningCount} 个警告`);

  if (errorCount > 0) {
    process.exit(1);
  }
}

function main(argv: string[]): void {
  const [, , command, ...rest] = argv;

  if (!command || command === "help" || command === "-h" || command === "--help") {
    process.stdout.write(HELP_TEXT);
    return;
  }

  if (command === "ingest") {
    if (rest.length === 0) {
      die("缺少 source 参数。用法: bin/wiki ingest <source>");
    }
    const source = rest.join(" ");
    // 如果是 URL，抓取并存入 raw/sources/
    if (source.startsWith("http://") || source.startsWith("https://")) {
      try {
        const script = resolve(ROOT, "tools", "ingest.py");
        let type = "blog";
        if (source.includes("github.com")) type = "repo";
        else if (source.includes("youtube.com") || source.includes("youtu.be")) type = "video";
        else if (source.includes("x.com") || source.includes("twitter.com")) type = "tweet";
        execSync(`python3 "${script}" "${source}" --type ${type}`, {
          stdio: "inherit",
        });
      } catch (e) {
        die(`抓取失败: ${(e as Error).message}`);
      }
    }
    return;
  }

  if (command === "check") {
    runCheck(rest[0]);
    return;
  }

  die(`未知命令: ${command}`);
}

main(process.argv);
