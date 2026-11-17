import { mkdtempSync, mkdirSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import assert from "node:assert/strict";
import test from "node:test";
import { checkLinks } from "../bin/check-links.ts";

function makeFixture(files: Record<string, string>): { dir: string; cleanup: () => void } {
  const dir = mkdtempSync(join(tmpdir(), "wiki-check-links-"));
  for (const [rel, content] of Object.entries(files)) {
    const abs = join(dir, rel);
    mkdirSync(join(abs, ".."), { recursive: true });
    writeFileSync(abs, content, "utf8");
  }
  return { dir, cleanup: () => rmSync(dir, { recursive: true, force: true }) };
}

test("passes valid wikilinks, table-escaped aliases, anchors, assets, and index coverage", () => {
  const { dir, cleanup } = makeFixture({
    "index.md": "# Nav\n- [[wiki/topics/ai/agent|Agent]]\n- [[wiki/topics/ai/mcp|MCP]]\n",
    "raw/assets/diagram.png": "png",
    "raw/sources/agent.md": "# Agent raw\n",
    "wiki/topics/ai/agent.md": [
      "---",
      "title: Agent",
      "type: topic",
      "category: ai",
      "created: 2026-11-17",
      "updated: 2026-11-17",
      "tags: []",
      "source_refs:",
      "  - raw/sources/agent.md",
      "---",
      "| Col |",
      "| --- |",
      "| [[wiki/topics/ai/mcp\\|MCP]] |",
      "See [[mcp#Overview]] and ![[diagram.png]] and [raw](../../../raw/sources/agent.md).",
    ].join("\n"),
    "wiki/topics/ai/mcp.md": "---\ntitle: MCP\n---\n## Overview\n",
  });
  try {
    const res = checkLinks(dir);
    assert.equal(res.errorCount, 0);
    assert.equal(res.warningCount, 0);
  } finally {
    cleanup();
  }
});

test("reports errors for broken path links, missing assets, missing index entries, and broken repo source_refs", () => {
  const { dir, cleanup } = makeFixture({
    "index.md": "# Nav\n- [[wiki/topics/ai/agent|Agent]]\n- [[wiki/topics/ai/ghost|Ghost]]\n",
    "wiki/topics/ai/agent.md": [
      "---",
      "title: Agent",
      "source_refs:",
      "  - raw/sources/missing.md",
      "---",
      "Broken [[wiki/topics/ai/nope]], ![[missing.png]], and [bad](./nope.md).",
    ].join("\n"),
    "wiki/topics/ai/orphan.md": "---\ntitle: Orphan\n---\nHello\n",
  });
  try {
    const res = checkLinks(dir);
    assert.equal(res.errorCount, 6);
    const msgs = res.issues.map((i) => i.message);
    assert.ok(msgs.some((m) => m.includes("raw/sources/missing.md")));
    assert.ok(msgs.some((m) => m.includes("[[wiki/topics/ai/nope]]")));
    assert.ok(msgs.some((m) => m.includes("![[missing.png]]")));
    assert.ok(msgs.some((m) => m.includes("(./nope.md)")));
    assert.ok(msgs.some((m) => m.includes("[[wiki/topics/ai/ghost|Ghost]]")));
    assert.ok(msgs.some((m) => m.includes("wiki/topics/ai/orphan.md")));
  } finally {
    cleanup();
  }
});

test("treats bare concept stubs and non-repo source_refs as warnings only", () => {
  const { dir, cleanup } = makeFixture({
    "index.md": "# Nav\n- [[wiki/topics/ai/agent|Agent]]\n",
    "wiki/topics/ai/agent.md": [
      "---",
      "title: Agent",
      "source_refs:",
      "  - memory/2026-04-23.md",
      "---",
      "See [[Uncreated Concept]].",
    ].join("\n"),
  });
  try {
    const res = checkLinks(dir);
    assert.equal(res.errorCount, 0);
    assert.equal(res.warningCount, 2);
  } finally {
    cleanup();
  }
});

test("skips fenced code blocks, list-indented fences, indented code, inline code, and HTML comments", () => {
  const { dir, cleanup } = makeFixture({
    "index.md": "# Nav\n- [[wiki/topics/ai/agent|Agent]]\n",
    "wiki/topics/ai/agent.md": [
      "---",
      "title: Agent",
      "---",
      "Inline `[[wiki/missing]]` and `[x](./missing.md)`.",
      "<!-- [[wiki/missing-comment]] -->",
      "```md",
      "[[wiki/missing-fence]]",
      "```",
      "- ```cpp",
      "  int a = f[0](vector<int>);",
      "  ```",
      "\t[indented](nope.md)",
    ].join("\n"),
  });
  try {
    const res = checkLinks(dir);
    assert.equal(res.errorCount, 0);
    assert.equal(res.warningCount, 0);
  } finally {
    cleanup();
  }
});
