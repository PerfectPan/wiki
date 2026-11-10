<!--
source: https://www.dsebastien.net/2026-10-16-claude-code-idle-compaction-cheaper-to-resume-but-from-a-summary/
type: blog
fetched: 2026-11-10
-->

# [news](https://www.dsebastien.net/tag/news/)
            ↻ Updated Oct 2026
            2026-10-16 Claude Code idle compaction - cheaper to resume, but from a summary
In short
                    Claude Code now compacts long sessions while you're away. Leave a big conversation alone for about an hour and, when you come back, the conversation shows Compacted while idle, before the prompt cache expired. From that point on, Claude works from a summary of what you did together.
#### Sebastien Dubois
### 23 Oct 2026
                        · updated 23 Oct 2026
                            — 4 min read





    Share

























            Sébastien Dubois
Organize your thoughts, life & work ⚡ AI, Personal Organization, LifeOS, Obsidian.
#### [Subscribe](#/portal/signup)




            Go Further
#### ****[MOST POPULAR
                Knowii Community
                ALL courses + tools + community + future workshops
                Learn more →](https://www.store.dsebastien.net/product/knowii-community/)




                Featured
- ➤ 
                                The Best Obsidian Plugins for Finding Notes
- ➤ 
                                Navigate Your Obsidian Vault - Links, Graphs, Bookmarks and Hubs
- ➤ 
                                Search Your Obsidian Vault From Outside Obsidian
- ➤ 
                                If it isn't in the project's home, it doesn't exist
- ➤ 
                                Obsidian Search Beyond the Basics - Version History, CLI, Mobile and Performance
[📚 All Articles](/all-articles/)
            [🏷️ All Topics](/tags/)
            [🧵 Series](/series/)





            *Canonical version: ***[2026-10-16 Claude Code idle compaction - cheaper to resume, but from a summary](https://notes.dsebastien.net/30+Areas/33+Permanent+notes/33.04+Creations/News/2026-10-16+Claude+Code+idle+compaction+-+cheaper+to+resume,+but+from+a+summary?ref=dsebastien.net)*.*
[Claude Code](https://notes.dsebastien.net/30+Areas/33+Permanent+notes/33.02+Content/Claude+Code?ref=dsebastien.net) now compacts long sessions while you're away. Leave a big conversation alone for about an hour and, when you come back, the conversation shows Compacted while idle, before the prompt cache expired. From that point on, Claude works from a summary of what you did together.
It's a sensible default, and it saves usage. For deep sessions where nuance matters, though, I'd rather decide myself when (and how) my context gets compressed.
## What it does
[Lydia Hallie](https://notes.dsebastien.net/30+Areas/36+People/Lydia+Hallie?ref=dsebastien.net) (Claude Code team at [Anthropic](https://notes.dsebastien.net/30+Areas/33+Permanent+notes/33.02+Content/Anthropic?ref=dsebastien.net)) announced it on 14 October: "It now compacts long idle sessions right before the prompt cache expires (~1h). If you come back to it later, it only has to reprocess the summary instead of the entire conversation, which saves you some usage."
The reason is the prompt cache. Claude Code keeps long conversations on a one-hour cache, so each new message reads the history at the cheap cache-read price. Once that hour has passed, the cache is gone, and your next message reprocesses the whole history at the full input price. On a session with 500,000 tokens of history, that's a lot of usage for a single "ok, let's continue". I explain the 5-minute vs 1-hour cache logic in [Claude Code Prompt Caching](https://notes.dsebastien.net/30+Areas/33+Permanent+notes/33.02+Content/Claude+Code+Prompt+Caching?ref=dsebastien.net).
Idle compaction kicks in about 54 minutes after your last request, a few minutes before the cache expires, and compacts the conversation. Your next message then sends the summary instead of the full history.
According to the docs, all of these conditions must hold:
- You're in an interactive terminal session
- The conversation is on the one-hour cache TTL
- Claude Code can fetch feature flags from Anthropic (so it never runs if you set DISABLE_TELEMETRY or CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC, or if you use Bedrock, Foundry and other third-party providers)
- The context has reached 200,000 tokens (the default threshold)
- Your computer is awake at the 54-minute mark
Because of that 200K threshold, it mostly concerns 1M-context sessions. On a 200K window, regular auto-compaction fires before you ever get there.
## What you give up
Lydia says it herself in the follow-up post: "It does mean that Claude continues from a summary instead of your full context though."
Compaction is lossy. The summary keeps the broad strokes and drops details: the approach you tried and rejected two hours ago, the exact error message, the constraint you mentioned once at the start. And since you weren't there, nobody told the summary what to keep. That's the [tension between compression and context](https://notes.dsebastien.net/30+Areas/33+Permanent+notes/33.02+Content/Natural+tension+between+compression+and+context?ref=dsebastien.net): the more you compress, the more nuance you lose.
For many sessions, that's fine. If you were in the middle of a long refactoring and you'll pick it up tomorrow with "continue", the summary is enough, and you save a big chunk of usage.
For deep sessions, I'd think twice. Think of a design discussion full of nuance, a debugging session where the dead ends matter, or an analysis you built up over hours... In those sessions, Claude needs the details. Re-explaining what the summary forgot costs more than one full reprocess, and that's assuming you even notice what it forgot.
## How to control it
You have three options.
**Compact yourself before stepping away.** Run /compact focus on <what matters> before a break. You still get the cheap resume, but you choose what the summary keeps. The context window docs recommend the same focus trick for steering any summary.
Raise (or lower) the threshold with CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS. The default is 200000 and the minimum is 100000 (anything lower gets raised to it). Set it high, e.g. 600000, and only really huge sessions get compacted. Lower it to 150000 if you want sessions on a 200K window to qualify:

```
{
  "env": {
    "CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS": "600000"
  }
}

```
Or turn it off with "idleCompaction": false in settings.json (it works in any settings file and needs v2.1.290 or later). For a single session, DISABLE_AUTO_COMPACT=1 turns it off together with regular auto-compaction, and /compact keeps working.
Note that "autoCompactEnabled": false also turns idle compaction off. If you only want to stop the idle one, use idleCompaction. And DISABLE_COMPACT=1 goes further: it disables all compaction, including the manual /compact command.
## What I'd do
I'd keep it on. Most idle sessions get resumed with a quick follow-up, and paying full price for a few hundred thousand tokens of history just to say "continue" is a waste of usage.
Before leaving a session that matters, I'd compact it myself with a clear focus. And if you regularly leave nuanced 1M-context sessions open over lunch, set "idleCompaction": false and accept the cost of the full reprocess when you come back.
All the settings (and how they interact) are in [Claude Code Configuration](https://notes.dsebastien.net/30+Areas/33+Permanent+notes/33.02+Content/Claude+Code+Configuration?ref=dsebastien.net). For when to compact, clear or write a handoff file instead, see [Claude Code Tips and Best Practices](https://notes.dsebastien.net/30+Areas/33+Permanent+notes/33.02+Content/Claude+Code+Tips+and+Best+Practices?ref=dsebastien.net).
That's it for today! ✨
## References
- Lydia Hallie, idle compaction announcement (X, 2026-10-14): https://x.com/lydiahallie/status/2110484840256819380
- Lydia Hallie, how to turn it off and change the threshold (X, 2026-10-14): https://x.com/lydiahallie/status/2110484841926152622
- Claude Code changelog (v2.1.299): https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
- Claude Code settings reference, idleCompaction: https://code.claude.com/docs/en/settings-reference#idlecompaction
- Claude Code environment variables (CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS, DISABLE_AUTO_COMPACT, DISABLE_COMPACT): https://code.claude.com/docs/en/env-vars
- Claude Code context window docs: https://code.claude.com/docs/en/context-window
- GitHub issue #66115, "Feature request: auto-compact on idle timeout to prevent cache expiry cost" (community request): https://github.com/anthropics/claude-code/issues/66115
## Related
- Claude Code
- Claude Code Prompt Caching
- Claude Code Configuration
- Claude Code Tips and Best Practices
- Claude Code Memory
- Context Compression
- Natural tension between compression and context
- Lydia Hallie
- Anthropic
Enjoying this? **Subscribe for free** to get articles like this every week.
[Subscribe ✨](#/portal/signup)




        Free download
Grab the free Knowledge System Checklist
Subscribe to the newsletter and I'll send you practical systems every week — plus instant access to the guide.
Subscribe 💌









        Email sent
Free. No spam. Unsubscribe anytime.
## Keep reading
## [← Older article2026-10-21 Claude Duet - Anthropic's answer to Dots, in yet another app](/2026-10-21-claude-duet-anthropics-answer-to-dots-in-yet-another-app/)
            [Newer article →AI Skill Best Practices](/ai-skill-best-practices/)




            About Sébastien
Written by
Sébastien Dubois
Knowledge Management expert, 20+ years in IT. I help knowledge workers escape information overload with systems that actually work — writing about [AI](/tag/ai/), [Knowledge Management](/tag/personal-knowledge-management/), [Obsidian](/tag/obsidian/), [productivity](/tag/productivity/) and [knowledge work](/tag/knowledge-work/).
## [Join the Knowii Community](/join-the-knowii-community-and-fix-your-information-overload-problem/)
            [or subscribe free →](#/portal/signup)



            Ready to get to the next level?
Tired of information overwhelm? Build a system that works:
[🎯 Knowii Community
        Community + courses + tools in one place — pick the tier that fits.
            From €14.99/quarter](https://www.store.dsebastien.net/product/knowii-community/)
    Not ready to buy? Start free: [Knowledge System Checklist](https://www.dsebastien.net/free-knowledge-management-system-checklist/)
**Found this valuable?** Share it with someone who needs it.
