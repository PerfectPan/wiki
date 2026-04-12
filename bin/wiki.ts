#!/usr/bin/env node

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const ROOT = resolve(__dirname, "..");
const PROMPTS_DIR = resolve(ROOT, "prompts");

const HELP_TEXT = `wiki CLI

用法:
  bin/wiki help
  bin/wiki ingest <source>
  bin/wiki query <question>
  bin/wiki lint
  bin/wiki migrate <logseq-page>

命令:
  ingest   为新来源生成标准 ingest 提示词
  query    为知识问答生成标准 query 提示词
  lint     为巡检知识库生成标准 lint 提示词
  migrate  为 Logseq 页面迁移生成标准 migrate 提示词
`;

type TemplateValues = Record<string, string>;

function loadTemplate(name: string): string {
  return readFileSync(resolve(PROMPTS_DIR, `${name}.md`), "utf8");
}

function render(name: string, extra: TemplateValues = {}): string {
  let text = loadTemplate(name);
  const values: TemplateValues = {
    ROOT,
    AGENTS: resolve(ROOT, "AGENTS.md"),
    SCHEMA: resolve(ROOT, "SCHEMA.md"),
    INDEX: resolve(ROOT, "index.md"),
    LOG: resolve(ROOT, "log.md"),
    RAW_SOURCES: resolve(ROOT, "raw", "sources"),
    RAW_ASSETS: resolve(ROOT, "raw", "assets"),
    TOPICS: resolve(ROOT, "wiki", "topics"),
    SYNTHESES: resolve(ROOT, "wiki", "syntheses"),
    COMPARISONS: resolve(ROOT, "wiki", "comparisons"),
    ...extra,
  };

  for (const [key, value] of Object.entries(values)) {
    text = text.replaceAll(`{{${key}}}`, value);
  }

  return text;
}

function die(message: string): never {
  console.error(message);
  process.exit(1);
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
    process.stdout.write(render("ingest", { INPUT: rest.join(" ") }));
    return;
  }

  if (command === "query") {
    if (rest.length === 0) {
      die('缺少 question 参数。用法: bin/wiki query "<question>"');
    }
    process.stdout.write(render("query", { INPUT: rest.join(" ") }));
    return;
  }

  if (command === "lint") {
    process.stdout.write(render("lint"));
    return;
  }

  if (command === "migrate") {
    if (rest.length === 0) {
      die("缺少 logseq-page 参数。用法: bin/wiki migrate <logseq-page>");
    }
    process.stdout.write(render("migrate", { INPUT: rest.join(" ") }));
    return;
  }

  die(`未知命令: ${command}`);
}

main(process.argv);
