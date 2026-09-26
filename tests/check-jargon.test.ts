import assert from "node:assert/strict";
import { execFileSync, spawnSync } from "node:child_process";
import { cpSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { test } from "node:test";

const source = resolve(dirname(fileURLToPath(import.meta.url)), "..");

function fixture(t: { after: (fn: () => void) => void }) {
  const root = mkdtempSync(resolve(tmpdir(), "wiki-jargon-"));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  cpSync(resolve(source, "bin"), resolve(root, "bin"), { recursive: true });
  cpSync(resolve(source, "package.json"), resolve(root, "package.json"));
  const write = (file: string, content: string) => {
    mkdirSync(dirname(resolve(root, file)), { recursive: true });
    writeFileSync(resolve(root, file), content);
  };
  const git = (...args: string[]) => execFileSync("git", args, { cwd: root, encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] });
  git("init", "-q");
  git("config", "user.name", "Test");
  git("config", "user.email", "test@example.invalid");
  git("config", "commit.gpgsign", "false");
  git("config", "core.hooksPath", resolve(root, "no-hooks"));
  const commit = () => { git("add", "."); git("commit", "-qm", "test baseline"); };
  const run = (...args: string[]) => {
    const result = spawnSync(process.execPath, [resolve(root, "bin/wiki.ts"), "check-jargon", ...args], { cwd: root, encoding: "utf8" });
    return { status: result.status, output: result.stdout + result.stderr };
  };
  return { root, write, git, commit, run };
}

test("reports prose and descriptive metadata, preserving positions", (t) => {
  const f = fixture(t);
  f.write("wiki/中文 页面.md", "---\ntitle: 护栏\ndescription: |\n  工具门禁\nsource_refs:\n  - 契约.md\n---\n# 契约\n| 说明 | 透传 |\n");
  const result = f.run();
  assert.equal(result.status, 1);
  for (const position of ["2:8", "4:5", "8:3", "9:8"]) assert.ok(result.output.includes(`wiki/中文 页面.md:${position}:`), result.output);
  assert.match(result.output, /4 个问题/);
});

test("preserves raw material, code, quotations, URLs and link targets", (t) => {
  const f = fixture(t);
  f.write("raw/source.md", "护栏");
  f.write("prompts/example.md", "门禁");
  f.write("wiki/page.md", [
    "正文 `护栏` 和 ``契约 ` 示例``。", "> 门禁", "```ts", "护栏", "```",
    "~~~~", "契约", "~~~", "门禁", "~~~~", "    护栏", "<!--", "门禁", "-->",
    "[[护栏]] [[wiki/契约|接口说明]] [来源](https://example.com/门禁)",
    "https://example.com/护栏", "[ref]: https://example.com/门禁", "契约测试。Reactive Framework。",
  ].join("\n"));
  assert.equal(f.run().status, 0);
  f.write("wiki/page.md", "[[old|护栏]] [门禁](https://example.com)");
  assert.match(f.run().output, /2 个问题/);
});

test("term exceptions do not exempt other occurrences on the same line", (t) => {
  const f = fixture(t);
  f.write("wiki/page.md", "契约测试验证契约。");
  assert.match(f.run().output, /page.md:1:7:.*契约/);
});

test("nested list items are prose rather than indented code", (t) => {
  const f = fixture(t);
  f.write("wiki/page.md", "- 说明\n    - 护栏\n    1. 门禁\n");
  const result = f.run();
  assert.equal(result.status, 1);
  assert.match(result.output, /2 个问题/);
});

test("a reasoned exception applies only to named terms on that line", (t) => {
  const f = fixture(t);
  f.write("wiki/page.md", "社会契约 <!-- jargon-allow: 契约; 书名 -->\n契约\n");
  assert.match(f.run().output, /page.md:2:1:/);
  assert.match(f.run().output, /1 个问题/);
  f.write("wiki/page.md", "契约 门禁 <!-- jargon-allow: 契约; 原标题 -->");
  assert.match(f.run().output, /1 个问题/);
  f.write("wiki/page.md", "契约 <!-- jargon-allow: 契约 -->");
  assert.match(f.run().output, /必须.*保留理由/);
});

test("incremental checks ignore old prose and retain full code-block context", (t) => {
  const f = fixture(t);
  f.write("wiki/page.md", "旧护栏\n\n```\nold\n```\n");
  f.commit();
  f.write("wiki/page.md", "旧护栏\n\n```\n门禁\n```\n新增说明\n");
  assert.equal(f.run("--base", "HEAD").status, 0);
  f.write("wiki/新增 页面.md", "门禁");
  assert.match(f.run("--base", "HEAD").output, /新增 页面.md:1:1:/);
  assert.equal(f.run().status, 1);
});

test("staged checks read the index, not the worktree", (t) => {
  const f = fixture(t);
  f.write("wiki/page.md", "已有说明\n");
  f.commit();
  f.write("wiki/page.md", "已有说明\n护栏\n");
  f.git("add", "wiki/page.md");
  f.write("wiki/page.md", "已有说明\n输出检查\n");
  assert.equal(f.run("--staged").status, 1);
  f.git("add", "wiki/page.md");
  f.write("wiki/page.md", "已有说明\n门禁\n");
  assert.equal(f.run("--staged").status, 0);
});

test("renames with Chinese names are checked and deleted files are ignored", (t) => {
  const f = fixture(t);
  f.write("wiki/旧 页面.md", "契约\n");
  f.commit();
  f.git("mv", "wiki/旧 页面.md", "wiki/新 页面.md");
  assert.match(f.run("--staged").output, /新 页面.md:1:1:/);
  f.git("rm", "-f", "wiki/新 页面.md");
  assert.equal(f.run("--staged").status, 0);
});

test("bad arguments, missing files and invalid bases fail visibly", (t) => {
  const f = fixture(t);
  f.write("wiki/page.md", "正文");
  f.commit();
  for (const args of [["--base"], ["--staged", "wiki"], ["--base", "missing-ref"], ["wiki/missing.md"], ["raw/source.md"]]) {
    assert.equal(f.run(...args).status, 1, args.join(" "));
  }
});

test("pre-commit rejects staged jargon", (t) => {
  const f = fixture(t);
  cpSync(resolve(source, ".githooks"), resolve(f.root, ".githooks"), { recursive: true });
  f.write("wiki/page.md", "护栏\n");
  f.git("add", "wiki/page.md");
  const result = spawnSync("bash", [resolve(f.root, ".githooks/pre-commit")], {
    cwd: f.root, encoding: "utf8", env: { ...process.env, PATH: `${dirname(process.execPath)}:${process.env.PATH}` },
  });
  assert.equal(result.status, 1);
  assert.match(result.stdout + result.stderr, /page.md:1:1:.*护栏/);
});

test("every configured term has a suggestion and is detected", (t) => {
  const f = fixture(t);
  const rules = JSON.parse(readFileSync(resolve(source, "bin/jargon-rules.json"), "utf8"));
  assert.equal(new Set(rules.map((r: { term: string }) => r.term)).size, rules.length);
  for (const rule of rules) {
    assert.ok(rule.suggestion);
    f.write("wiki/page.md", `正文${rule.term}。`);
    assert.equal(f.run().status, 1, rule.term);
  }
});

for (const configPath of [".claude/settings.json", ".codex/hooks.json"]) {
  test(`${configPath} returns repair guidance from a repository subdirectory`, (t) => {
    const f = fixture(t);
    f.write("wiki/page.md", "已有内容\n");
    f.commit();
    f.write("wiki/page.md", "已有内容\n护栏\n");
    const config = JSON.parse(readFileSync(resolve(source, configPath), "utf8"));
    const group = config.hooks.PostToolUse[0];
    const tool = configPath.startsWith(".claude") ? "Edit" : "apply_patch";
    assert.ok(new RegExp(group.matcher).test(tool));
    assert.ok(new RegExp(group.matcher).test("Bash"));
    const run = () => spawnSync("sh", ["-c", group.hooks[0].command], {
      cwd: resolve(f.root, "wiki"), encoding: "utf8",
      input: JSON.stringify({ hook_event_name: "PostToolUse", tool_name: tool, tool_input: {} }),
      env: { ...process.env, CLAUDE_PROJECT_DIR: f.root, PATH: `${dirname(process.execPath)}:${process.env.PATH}` },
    });
    const result = run();
    assert.equal(result.status, 0, result.stderr);
    const output = JSON.parse(result.stdout);
    assert.equal(output.hookSpecificOutput.hookEventName, "PostToolUse");
    assert.match(output.hookSpecificOutput.additionalContext, /wiki\/page.md:2:1:.*护栏/);
    assert.equal(output.decision, undefined);
    f.write("wiki/page.md", "已有内容\n输出检查\n");
    assert.equal(run().stdout, "");
  });
}

test("hook ignores read events and reports malformed events", (t) => {
  const f = fixture(t);
  const run = (input: string) => spawnSync(process.execPath, [resolve(f.root, "bin/jargon-hook.ts")], { input, encoding: "utf8" });
  assert.equal(run(JSON.stringify({ hook_event_name: "PostToolUse", tool_name: "Read" })).stdout, "");
  const result = run("broken json");
  assert.equal(result.status, 0);
  assert.match(JSON.parse(result.stdout).hookSpecificOutput.additionalContext, /无法读取事件/);
});

test("hook surfaces scanner failure instead of reporting success", (t) => {
  const f = fixture(t);
  f.write("wiki/page.md", "内容\n");
  const result = spawnSync(process.execPath, [resolve(f.root, "bin/jargon-hook.ts")], {
    input: JSON.stringify({ hook_event_name: "PostToolUse", tool_name: "Bash" }), encoding: "utf8",
  });
  assert.equal(result.status, 0);
  assert.match(JSON.parse(result.stdout).hookSpecificOutput.additionalContext, /用词检查失败/);
});
