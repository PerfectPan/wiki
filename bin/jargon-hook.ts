import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");

function feedback(message: string): void {
  process.stdout.write(JSON.stringify({
    hookSpecificOutput: {
      hookEventName: "PostToolUse",
      additionalContext: message,
    },
  }) + "\n");
}

try {
  const event = JSON.parse(readFileSync(0, "utf8"));
  if (event.hook_event_name === "PostToolUse" && /^(Write|Edit|MultiEdit|apply_patch|Bash)$/.test(event.tool_name ?? "")) {
    // A shell command or patch can touch multiple files; inspect repository changes rather than guessing paths from tool arguments.
    const result = spawnSync(process.execPath, [resolve(root, "bin/wiki.ts"), "check-jargon", "--base", "HEAD"], {
      cwd: root,
      encoding: "utf8",
      timeout: 10000,
      maxBuffer: 1024 * 1024,
    });
    if (result.error || result.status === null) {
      feedback("Wiki 用词检查未完成。请运行 bin/wiki check-jargon --base HEAD 检查修改；不要把本次检查视为通过。");
    } else if (result.status !== 0) {
      const report = (result.stderr + result.stdout).trim();
      const excerpt = report.length > 6000 ? report.slice(0, 6000) + "\n报告已截断，运行检查命令查看完整结果。" : report;
      feedback("Wiki 用词检查未通过。请阅读以下报告，只修正本任务相关的文字，不改写原始引用或其他人的修改。正式名称可按 bin/README.md 注明保留理由。修改后运行 bin/wiki check-jargon --base HEAD 复查。\n" + excerpt);
    }
  }
} catch (error) {
  feedback(`Wiki 用词 hook 无法读取事件或运行检查：${(error as Error).message}。请手动运行 bin/wiki check-jargon --base HEAD。`);
}
