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
  bin/wiki prompts <list|search|show|check> [...]

命令:
  ingest    抓取来源并存入 raw/sources/
  check     校验 Markdown 文件的 frontmatter 是否符合 SCHEMA 规范
  prompts   提示词库：列表、搜索、打印原文、校验（见 prompts/README.md）

prompts 子命令:
  list [--tag <tag>] [--level <档>] [--json]   列出提示词
  search <关键词> [--json]                     在元数据与正文里搜索
  show <id> [--meta]                           打印提示词原文
  check                                        校验 prompts/ 下所有提示词文件

工作流引导见 .agents/skills/
`;

const VALID_TYPES = ["topic", "synthesis", "comparison"] as const;
const VALID_CATEGORIES = [
  "frontend",
  "design",
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

  // prompts/ 下的文件走提示词规则，而不是 wiki 页面规则
  if (relPath === PROMPT_DIR || relPath.startsWith(`${PROMPT_DIR}/`)) {
    return checkPromptFile(filePath);
  }

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

/* ------------------------------------------------------------------ *
 * prompts/
 * ------------------------------------------------------------------ */

const PROMPT_DIR = "prompts";
const PROMPT_REQUIRED = ["id", "title", "scene", "level", "tags", "source", "added"] as const;
const PROMPT_LEVELS = ["推荐", "可参考", "偏薄"] as const;
const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;

interface PromptRecord {
  path: string;
  id: string;
  fm: Frontmatter;
  body: string;
  blocks: number;
}

function promptPaths(): string[] {
  const dir = resolve(ROOT, PROMPT_DIR);
  let names: string[];
  try {
    names = readdirSync(dir);
  } catch {
    return [];
  }
  return names
    .filter((name) => name.endsWith(".md") && name !== "README.md")
    .map((name) => resolve(dir, name))
    .sort();
}

/**
 * 拆分提示词文件：frontmatter 之后的所有内容就是提示词原文。
 * 原文不加代码块包装，元数据全部写在 frontmatter 里。
 */
function splitPromptBody(content: string): { body: string; extra: string[]; blocks: number } {
  const lines = content.split("\n");
  let i = 0;
  if (lines[0]?.trim() === "---") {
    i = 1;
    while (i < lines.length && lines[i].trim() !== "---") i++;
    i++;
  }
  const body = lines.slice(i).join("\n").replace(/^\n+/, "").replace(/\s+$/, "");
  return { body, extra: [], blocks: body.trim() === "" ? 0 : 1 };
}

function readPrompt(path: string): PromptRecord {
  const content = readFileSync(path, "utf8");
  const fm = parseFrontmatter(content) ?? {};
  const fallbackId = path.split("/").pop()!.replace(/\.md$/, "");
  const id = typeof fm["id"] === "string" && fm["id"] !== "" ? (fm["id"] as string) : fallbackId;
  const { body, blocks } = splitPromptBody(content);
  return { path, id, fm, body, blocks };
}

function checkPromptFile(filePath: string): CheckIssue[] {
  const issues: CheckIssue[] = [];
  const name = filePath.split("/").pop()!;

  if (name === "README.md") {
    return issues;
  }

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

  for (const field of PROMPT_REQUIRED) {
    const value = fm[field];
    if (!(field in fm)) {
      issues.push({ level: "error", message: `缺少必填字段: ${field}` });
    } else if (Array.isArray(value) ? value.length === 0 : String(value).trim() === "") {
      issues.push({ level: "error", message: `字段为空: ${field}` });
    }
  }

  const expectedId = name.replace(/\.md$/, "");
  if (typeof fm["id"] === "string" && fm["id"] !== expectedId) {
    issues.push({ level: "error", message: `id (${fm["id"]}) 与文件名 (${expectedId}) 不一致` });
  }

  const level = fm["level"];
  if (typeof level === "string" && !PROMPT_LEVELS.includes(level as (typeof PROMPT_LEVELS)[number])) {
    issues.push({
      level: "error",
      message: `level 值无效: "${level}"，必须是 ${PROMPT_LEVELS.join(" / ")} 之一`,
    });
  }

  if ("tags" in fm && !Array.isArray(fm["tags"])) {
    issues.push({ level: "error", message: "tags 必须是数组格式" });
  }

  const added = fm["added"];
  if (typeof added === "string" && !DATE_RE.test(added)) {
    issues.push({ level: "error", message: `added 日期格式无效: "${added}"，必须是 YYYY-MM-DD` });
  }

  const { body } = splitPromptBody(content);
  if (body.trim() === "") {
    issues.push({ level: "error", message: "frontmatter 之后没有正文（提示词原文不能为空）" });
  }

  return issues;
}

function collectPromptRecords(): PromptRecord[] {
  return promptPaths().map(readPrompt);
}

function promptToJson(record: PromptRecord): Record<string, unknown> {
  const out: Record<string, unknown> = { path: relative(ROOT, record.path) };
  for (const key of ["id", "title", "scene", "level", "tags", "source", "source_note", "notes", "added"] as const) {
    if (key in record.fm) {
      out[key] = record.fm[key];
    }
  }
  return out;
}

function runPrompts(rest: string[]): void {
  const sub = rest[0];
  if (!sub || sub === "help" || sub === "-h" || sub === "--help") {
    process.stdout.write(`用法:
  bin/wiki prompts list [--tag <tag>] [--level <档>] [--json]
  bin/wiki prompts search <关键词> [--json]
  bin/wiki prompts show <id> [--meta]
  bin/wiki prompts check

提示词文件格式见 prompts/README.md，分级标准见 wiki/topics/ai/Prompt.md。\n`);
    return;
  }

  const records = collectPromptRecords();

  if (sub === "list") {
    const json = rest.includes("--json");
    const tagFlag = rest.indexOf("--tag");
    const levelFlag = rest.indexOf("--level");
    const tag = tagFlag >= 0 ? rest[tagFlag + 1] : undefined;
    const level = levelFlag >= 0 ? rest[levelFlag + 1] : undefined;

    let hits = records;
    if (tag) {
      hits = hits.filter((r) => Array.isArray(r.fm["tags"]) && (r.fm["tags"] as string[]).includes(tag));
    }
    if (level) {
      hits = hits.filter((r) => r.fm["level"] === level);
    }

    if (json) {
      process.stdout.write(JSON.stringify(hits.map(promptToJson), null, 2) + "\n");
      return;
    }

    if (hits.length === 0) {
      console.log("没有匹配的提示词。");
      return;
    }
    const filters = [tag ? `tag=${tag}` : null, level ? `level=${level}` : null].filter(Boolean).join(" ");
    console.log(`提示词 ${hits.length} 条${filters ? `（${filters}）` : ""}\n`);
    for (const r of hits) {
      const tags = Array.isArray(r.fm["tags"]) ? (r.fm["tags"] as string[]).join(", ") : "";
      console.log(`- ${r.id} [${r.fm["level"] ?? "?"}] ${tags}`);
      console.log(`  ${r.fm["title"] ?? ""}`);
      console.log(`  场景: ${r.fm["scene"] ?? ""}`);
      console.log(`  原文: ${relative(ROOT, r.path)}`);
    }
    return;
  }

  if (sub === "search") {
    const keyword = rest[1];
    if (!keyword) {
      die("缺少关键词。用法: bin/wiki prompts search <关键词>");
    }
    const needle = keyword.toLowerCase();
    const hits = records.filter((r) => {
      const haystack = [
        r.id,
        String(r.fm["title"] ?? ""),
        String(r.fm["scene"] ?? ""),
        String(r.fm["source"] ?? ""),
        String(r.fm["source_note"] ?? ""),
        Array.isArray(r.fm["tags"]) ? (r.fm["tags"] as string[]).join(" ") : "",
        Array.isArray(r.fm["notes"]) ? (r.fm["notes"] as string[]).join(" ") : "",
        r.body,
      ]
        .join("\n")
        .toLowerCase();
      return haystack.includes(needle);
    });

    if (rest.includes("--json")) {
      process.stdout.write(JSON.stringify(hits.map(promptToJson), null, 2) + "\n");
      return;
    }
    if (hits.length === 0) {
      console.log(`没有命中 "${keyword}" 的提示词。`);
      return;
    }
    console.log(`命中 ${hits.length} 条 ("${keyword}")\n`);
    for (const r of hits) {
      console.log(`- ${r.id} [${r.fm["level"] ?? "?"}] ${r.fm["title"] ?? ""}`);
      console.log(`  场景: ${r.fm["scene"] ?? ""}`);
      console.log(`  原文: ${relative(ROOT, r.path)}`);
    }
    return;
  }

  if (sub === "show") {
    const id = rest[1];
    if (!id) {
      die("缺少 id。用法: bin/wiki prompts show <id>");
    }
    const target = records.find((r) => r.id === id.replace(/\.md$/, ""));
    if (!target) {
      die(`找不到提示词: ${id}（用 bin/wiki prompts list 查看可用 id）`);
    }
    if (rest.includes("--meta")) {
      for (const key of ["id", "title", "scene", "level", "source", "source_note", "added"] as const) {
        if (key in target.fm) {
          console.log(`${key}: ${target.fm[key]}`);
        }
      }
      const tags = target.fm["tags"];
      if (Array.isArray(tags)) {
        console.log(`tags: ${tags.join(", ")}`);
      }
      console.log("");
    }
    process.stdout.write(target.body + "\n");
    return;
  }

  if (sub === "check") {
    let errorCount = 0;
    let warningCount = 0;
    const files = promptPaths();
    for (const file of files) {
      const issues = checkPromptFile(file);
      const relPath = relative(ROOT, file);
      const fileErrors = issues.filter((i) => i.level === "error");
      const fileWarnings = issues.filter((i) => i.level === "warning");
      errorCount += fileErrors.length;
      warningCount += fileWarnings.length;
      if (fileErrors.length > 0) {
        console.error(`\n❌ ${relPath}`);
        for (const issue of fileErrors) {
          console.error(`  [error] ${issue.message}`);
        }
      }
      for (const issue of fileWarnings) {
        console.log(`\n⚠️  ${relPath}`);
        console.log(`  [warning] ${issue.message}`);
      }
    }

    // 索引导航：wiki/topics/ai/Awesome Prompts.md 应覆盖所有 id（只提醒，不阻断）
    const indexPath = resolve(ROOT, "wiki/topics/ai/Awesome Prompts.md");
    try {
      const index = readFileSync(indexPath, "utf8");
      const missing = files
        .map((f) => readPrompt(f).id)
        .filter((id) => !index.includes(`${PROMPT_DIR}/${id}`));
      if (missing.length > 0) {
        warningCount += 1;
        console.log(`\n⚠️  wiki/topics/ai/Awesome Prompts.md 未收录: ${missing.join(", ")}`);
      }
    } catch {
      warningCount += 1;
      console.log("\n⚠️  找不到 wiki/topics/ai/Awesome Prompts.md，跳过索引一致性检查");
    }

    console.log(`\n---`);
    console.log(`校验完成: ${files.length} 个提示词文件，${errorCount} 个错误，${warningCount} 个警告`);
    if (errorCount > 0) {
      process.exit(1);
    }
    return;
  }

  die(`未知的 prompts 子命令: ${sub}`);
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

  if (command === "prompts") {
    runPrompts(rest);
    return;
  }

  die(`未知命令: ${command}`);
}

main(process.argv);
