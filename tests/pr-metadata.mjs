import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const conventional = /^(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test|synthesis)(\([a-z0-9-]+\))?!?: \S[^\r\n]*$/u;
const nonLatinLetter = /(?=\p{Letter})\P{Script=Latin}/u;

function checkTitle(title) {
  if (!conventional.test(title)) throw new Error('Use an English Conventional Commits title: type(scope): description');
  if (nonLatinLetter.test(title) || /[《》]/u.test(title)) throw new Error('PR titles must be in English. Keep original page names in the description instead.');
}

function checkBody(body) {
  let fence = '';
  const prose = body.split(/\r?\n/u).map((line) => {
    const marker = line.match(/^\s*(`{3,}|~{3,})/u);
    if (fence) {
      if (marker && marker[1][0] === fence[0] && marker[1].length >= fence.length && line.slice(marker[0].length).trim() === '') fence = '';
      return '';
    }
    if (marker) { fence = marker[1]; return ''; }
    if (/^\s*>/u.test(line)) return '';
    return line;
  }).join('\n')
    .replace(/<!--[\s\S]*?-->/gu, '')
    .replace(/(`+)(.*?)\1(?!`)/gu, '')
    .replace(/!?\[[^\]\n]*\]\([^\n]*?\)/gu, '')
    .replace(/https?:\/\/[^\s<>]+/gu, '');
  if (!/[A-Za-z]/u.test(prose)) throw new Error('PR descriptions must include an English explanation, not only links or code.');
  if (nonLatinLetter.test(prose)) throw new Error('Write PR description prose in English. Put original paths/names in inline code, sources in links, and source quotations in blockquotes.');
}

function selfTest() {
  for (const title of ['docs(auth): clarify token revocation', 'fix(bin)!: correct parsing', 'synthesis: compare frameworks']) checkTitle(title);
  for (const title of ['', 'docs: 中文标题', 'docs: résumé 中文', 'docs: описание', 'wip: work', 'docs(Auth): change', 'docs: ', 'docs: first\nsecond']) assert.throws(() => checkTitle(title), title);
  for (const body of [
    'Explain the change and validation.',
    'Updated `wiki/中文.md`. See [中文来源](https://example.com).\n> 原文引用\n\nTests passed.',
    'Preserve the sample.\n```text\n中文示例\n```',
    'Describe the change. <!-- 中文模板提示 -->',
  ]) checkBody(body);
  for (const body of ['', '## Summary\n中文说明', '## Summary\nОписание', '`中文.md`', '[source](https://example.com)', '> quoted text', '```\ncode\n```']) assert.throws(() => checkBody(body), body);
  console.log('PR metadata self-test passed');
}

try {
  const args = process.argv.slice(2);
  if (args[0] === '--self-test' && args.length === 1) selfTest();
  else if (args[0] === '--title' && args.length === 2) checkTitle(args[1]);
  else if (args.length === 0) {
    const pr = process.env.GITHUB_EVENT_PATH ? JSON.parse(readFileSync(process.env.GITHUB_EVENT_PATH, 'utf8')).pull_request : null;
    checkTitle(pr?.title ?? process.env.PR_TITLE ?? '');
    checkBody(pr?.body ?? process.env.PR_BODY ?? '');
    console.log('PR title and description checks passed');
  } else throw new Error('Usage: node tests/pr-metadata.mjs [--self-test | --title <title>]');
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
