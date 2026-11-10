<!--
source: https://www.turboai.dev/blog/claude-code-idle-compaction-guide
type: blog
fetched: 2026-11-10
-->

# Claude Code "Compacted while idle": What Idle Compaction Does and How to Turn It Off[#](#claude-code-compacted-while-idle-what-idle-compaction-does-and-how-to-turn-it-off)
Published October 16, 2026 by [Alex Sorokoletov](/about)
"Compacted while idle, before the prompt cache expired" means Claude Code summarized your conversation while you were away. It does this to a conversation of 200K tokens or more after about 54 minutes idle, just before the one-hour prompt cache expires. To stop it, switch **Idle compaction** off in /config (v2.1.302 or later) or add "idleCompaction": false to settings.json (v2.1.290 or later).[1]
## Where it runs (v2.1.314)[#](#where-it-runs-v2-1-314)
Idle compaction started in the terminal. From v2.1.314 it also runs in VS Code and in Claude Desktop's Code tab, for subscribers who turned telemetry off, and on Bedrock, Vertex, Foundry and LLM gateways when the session uses the one-hour prompt cache.[3] In VS Code and the Code tab, the conversation is summarized while idle, and the summary is used on your next message only if the prompt cache has expired by then.
On an API key, Bedrock, Vertex or Foundry, the prompt cache lasts 5 minutes unless you set "promptCacheTtl": "1h" in settings.json or ENABLE_PROMPT_CACHING_1H=1. A session on the 5-minute cache is never idle-compacted. A Claude subscription within its usage limits gets the one-hour cache by default, so it gets idle compaction by default too.
## Why Claude Code compacts an idle session[#](#why-claude-code-compacts-an-idle-session)
A terminal session on the one-hour prompt cache pays the cached input rate while the cache is warm. When the hour runs out, the next message reprocesses the whole conversation at the full input rate. For a 300K-token session, that is 300K uncached tokens to say "continue". Idle compaction replaces the history with a summary shortly before the cache expires, so the next turn starts from the summary.
The cost of that saving is the same as any compaction: detail that is not in the summary is gone. Instructions given early in the session, rejected approaches, and exact file contents are the usual losses. That is the core of the complaint in [issue #98747](https://github.com/anthropics/claude-code/issues/98747), filed on v2.1.286, when there was no setting to stop it.
## How to turn off idle compaction[#](#how-to-turn-off-idle-compaction)
From v2.1.302, open /config and switch **Idle compaction** off. The row saves "idleCompaction": false to ~/.claude/settings.json. It shows only when idle compaction is turned on for your account, and not when a project, local or managed settings file already sets idleCompaction. The idle notices in v2.1.302 also end with turn off with "idleCompaction": false in settings.json.[2]
To set it by hand, add the setting to ~/.claude/settings.json for every project, or to .claude/settings.json for one project:

```
{
  "idleCompaction": false
}

```

The setting needs v2.1.290 or later. Setting it to true does not turn idle compaction on. Anthropic turns the feature on remotely, and true only means "do not block it".
To keep idle compaction but apply it only to larger sessions, raise the token minimum:

```
{
  "env": {
    "CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS": "500000"
  }
}

```

Values below 100,000 are raised to 100,000. With the variable unset, the minimum is 200,000.
Turning off auto-compaction also stops idle compaction: DISABLE_AUTO_COMPACT=1, DISABLE_COMPACT=1, or "autoCompactEnabled": false. Before v2.1.290 that was the only way to stop it, at the price of no automatic compaction near the context limit either.
## When idle compaction runs[#](#when-idle-compaction-runs)
Every condition in this table must hold. If one fails, the session is left alone.

| Condition | Default | What changes it |
| --- | --- | --- |
| Feature turned on remotely | Off unless Anthropic turns it on | Anthropic's remote configuration |
| Auto-compaction on | On | DISABLE_AUTO_COMPACT, DISABLE_COMPACT, autoCompactEnabled |
| Idle compaction not blocked | Not blocked | "idleCompaction": false |
| Session uses the one-hour prompt cache | On for a Claude subscription within its usage limits; off for an API key, Bedrock, Vertex and Foundry | "promptCacheTtl" ("5m" or "1h"), ENABLE_PROMPT_CACHING_1H, CLAUDE_CODE_PROMPT_CACHE_TTL |
| Cache still warm, and the conversation prefix unchanged since the last request | n/a | A lapsed cache or edited history skips it |
| Conversation size | 200,000 tokens | CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS (floor 100,000) |
| Idle time | 90% of the hour, about 54 minutes | Remote configuration, clamped to 50-95% (30 to 57 minutes) |
| No newer request, not near a usage limit | n/a | A request in flight or a usage-limit warning skips it |

````````````````````
If a turn is in flight when the timer fires, the conversation compacts between turns.
## A second mode in v2.1.300: compact on return[#](#a-second-mode-in-v2-1-300-compact-on-return)
v2.1.300 adds a mode that writes the summary in the background while you are idle and applies it when you come back. Its message was "Compacted after an hour idle, using a summary written while you were away". From v2.1.307 it reads "Compacted using a summary written while you were away". This mode also needs precomputeCompactionEnabled, the setting that lets Claude Code prepare a compaction summary before it is needed. "idleCompaction": false turns off both modes.
## Timeline: shipped before it was documented[#](#timeline-shipped-before-it-was-documented)

| Version | Published | Change |
| --- | --- | --- |
| v2.1.283 | 2026-09-25 | Idle compaction ships, with the "Compacted while idle" message. The only way to stop it is to turn off auto-compaction. |
| v2.1.290 | 2026-10-05 | "idleCompaction": false and CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS arrive. The release notes do not mention either. |
| v2.1.299 | 2026-10-14 | First release-notes entry: "Added idle compaction in the terminal", with both controls marked as needing v2.1.290. |
| v2.1.300 | 2026-10-14 | Compact-on-return mode added. |
| v2.1.302 | 2026-10-16 | An Idle compaction row in /config, and both idle notices say how to turn it off. |
| v2.1.314 | 2026-10-30 | Idle compaction reaches VS Code and Claude Desktop's Code tab, subscribers with telemetry off, and Bedrock, Vertex, Foundry and LLM gateways on the one-hour cache. |
| v2.1.307 | 2026-10-21 | The compact-on-return notice is shortened to "Compacted using a summary written while you were away". |

****``
For ten days, from v2.1.283 to v2.1.290, idle compaction could run with no setting to stop it except turning off auto-compaction completely.
## Should you turn it off?[#](#should-you-turn-it-off)
Keep it on if your long sessions often sit idle past an hour and you mostly continue the same task, because the next message then costs a summary instead of the full history. Turn it off if you come back to a long session to refer to exact earlier output, if a session carries instructions that a summary tends to drop, or if you prefer to run /compact yourself with custom instructions. A middle option is a higher [CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS](/docs/claude-code/env-vars/CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS), so only very large sessions are compacted.
## FAQ[#](#faq)
**Q: What does "Compacted while idle, before the prompt cache expired" mean?**
A: Claude Code replaced your conversation history with a summary while the session was idle, about 54 minutes after your last message, because the conversation was over 200K tokens and its one-hour prompt cache was about to expire.
**Q: Why did Claude Code compact my conversation when I didn't ask?**
A: That is idle compaction. A conversation of 200K tokens or more, left idle for about 54 minutes on the one-hour prompt cache, is summarized before the cache expires. Since v2.1.314 this also happens in VS Code, Claude Desktop's Code tab, and on Bedrock, Vertex, Foundry and gateways that use the one-hour cache. Add "idleCompaction": false to ~/.claude/settings.json to stop it.
**Q: How do I disable idle compaction in Claude Code?**
A: In v2.1.302 or later, switch **Idle compaction** off in /config. In v2.1.290 or later, add "idleCompaction": false to ~/.claude/settings.json. Turning off auto-compaction with DISABLE_AUTO_COMPACT=1 also stops it.
**Q: Does "idleCompaction": true turn it on?**
A: No. Anthropic turns idle compaction on remotely. true only leaves it unblocked.
**Q: What is CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS?**
A: The minimum conversation size, in tokens, for idle compaction. The default is 200,000, and values below 100,000 are raised to 100,000.
**Q: Which version added idle compaction?**
A: v2.1.283, published September 25, 2026. The release notes first mention it in v2.1.299.
**Q: Is compactOnIdle a Claude Code setting?**
A: No. The setting is idleCompaction, and false is the only value that changes behavior.
*Sources: [1] [Claude Code changelog, v2.1.299](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) | [2] [Claude Code changelog, v2.1.302](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) | [3] [Claude Code changelog, v2.1.314](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)*
*Related: [CLAUDE_AUTOCOMPACT_PCT_OVERRIDE Guide](/blog/claude-autocompact-pct-override-guide) | [Context Window Management Guide](/blog/claude-code-context-window-management) | [CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS in the env-var glossary](/docs/claude-code/env-vars/CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS) | [Claude Code v2.1.299 analysis](/blog/claude-code-env-vars-v2-1-299) | [Claude Code v2.1.314 analysis](/blog/claude-code-env-vars-v2-1-314)*
### Let's Connect
