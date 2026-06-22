# GitHub Feed Digest Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a daily GitHub Home Feed digest automation that fetches meaningful project activity, pushes a short notification, and opens a PR that persists the digest into `PerfectPan/wiki`.

**Architecture:** Use `/users/PerfectPan/received_events` as the primary feed source, enrich selected events with repo / PR / release metadata, score them into project-focused digest items, then fan out to notifier and wiki PR sinks. Keep the first implementation file-based and idempotent: overlap the fetch window, read recent wiki raw event JSON files for dedupe, and avoid a database until the workflow proves useful.

**Tech Stack:** TypeScript, Node.js 22, GitHub REST + GraphQL APIs, GitHub Actions cron, Vitest, `tsx`, `zod`, webhook notifier, `gh` for local validation and PR creation fallback.

---

### Task 1: Scaffold the automation repository

**Files:**
- Create: `/Users/perfectpan/Documents/rss-summary/package.json`
- Create: `/Users/perfectpan/Documents/rss-summary/tsconfig.json`
- Create: `/Users/perfectpan/Documents/rss-summary/vitest.config.ts`
- Create: `/Users/perfectpan/Documents/rss-summary/src/main.ts`
- Create: `/Users/perfectpan/Documents/rss-summary/tests/smoke.test.ts`

**Step 1: Write the failing smoke test**

```ts
import { describe, expect, it } from "vitest";

describe("rss-summary", () => {
  it("loads the CLI entrypoint", async () => {
    const mod = await import("../src/main");
    expect(mod.run).toBeTypeOf("function");
  });
});
```

**Step 2: Run test to verify it fails**

Run:

```bash
cd /Users/perfectpan/Documents/rss-summary
npm test
```

Expected: FAIL because `package.json` and `src/main.ts` do not exist yet.

**Step 3: Add minimal scaffold**

`package.json`:

```json
{
  "name": "rss-summary",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "tsx src/main.ts",
    "test": "vitest run",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": {
    "@octokit/graphql": "^9.0.0",
    "@octokit/rest": "^22.0.0",
    "zod": "^4.0.0"
  },
  "devDependencies": {
    "@types/node": "^22.0.0",
    "tsx": "^4.0.0",
    "typescript": "^5.0.0",
    "vitest": "^3.0.0"
  }
}
```

`src/main.ts`:

```ts
export async function run(): Promise<void> {
  console.log("github-feed-digest");
}

if (import.meta.url === `file://${process.argv[1]}`) {
  await run();
}
```

**Step 4: Run tests and typecheck**

Run:

```bash
npm install
npm test
npm run typecheck
```

Expected: PASS.

**Step 5: Commit**

```bash
git add package.json package-lock.json tsconfig.json vitest.config.ts src/main.ts tests/smoke.test.ts
git commit -m "feat: scaffold github feed digest"
```

### Task 2: Model the feed domain

**Files:**
- Create: `/Users/perfectpan/Documents/rss-summary/src/domain/feed-event.ts`
- Create: `/Users/perfectpan/Documents/rss-summary/src/domain/candidate-project.ts`
- Create: `/Users/perfectpan/Documents/rss-summary/tests/domain/feed-event.test.ts`

**Step 1: Write failing domain tests**

Test that a GitHub `PullRequestEvent` normalizes into an `ActivityCard`, and a `WatchEvent` normalizes into a project discovery signal.

Expected important fields:

- `eventId`
- `type`
- `actor`
- `repo`
- `createdAt`
- `action`
- `prNumber` for PR events
- `scoreReason` for digest scoring

**Step 2: Implement minimal domain types**

`FeedEvent` should remain close to GitHub payloads. `ActivityCard` is the internal card-like shape used by the scorer and renderer.

**Step 3: Run tests**

Run:

```bash
npm test -- tests/domain/feed-event.test.ts
```

Expected: PASS.

**Step 4: Commit**

```bash
git add src/domain tests/domain
git commit -m "feat: model github feed events"
```

### Task 3: Implement GitHub feed fetching

**Files:**
- Create: `/Users/perfectpan/Documents/rss-summary/src/github/github-client.ts`
- Create: `/Users/perfectpan/Documents/rss-summary/src/github/feed-source.ts`
- Create: `/Users/perfectpan/Documents/rss-summary/src/config.ts`
- Create: `/Users/perfectpan/Documents/rss-summary/tests/github/feed-source.test.ts`

**Step 1: Write failing tests with a fake client**

The tests should prove:

- the source fetches `/users/{username}/received_events`;
- pagination is capped to the configured page count;
- events older than the configured window are dropped;
- `following` is loaded separately for scoring metadata.

**Step 2: Implement GitHub client wrapper**

Expose methods:

```ts
getReceivedEvents(username: string, page: number): Promise<unknown[]>;
getFollowing(): Promise<Set<string>>;
getRepository(owner: string, repo: string): Promise<RepositoryMetadata>;
getPullRequest(owner: string, repo: string, number: number): Promise<PullRequestMetadata>;
```

**Step 3: Run tests**

Run:

```bash
npm test -- tests/github/feed-source.test.ts
```

Expected: PASS.

**Step 4: Commit**

```bash
git add src/github src/config.ts tests/github
git commit -m "feat: fetch github received events"
```

### Task 4: Add enrichment and scoring

**Files:**
- Create: `/Users/perfectpan/Documents/rss-summary/src/domain/scoring.ts`
- Create: `/Users/perfectpan/Documents/rss-summary/src/domain/enrichment.ts`
- Create: `/Users/perfectpan/Documents/rss-summary/tests/domain/scoring.test.ts`

**Step 1: Write failing scoring tests**

Cover these cases:

- `WatchEvent` by a followee ranks above routine PR updates.
- `ReleaseEvent` ranks high.
- multiple actors touching the same repo increases score.
- label-only PR events rank lower than merged PRs.
- repo topics matching configured interests increase score.

**Step 2: Implement transparent scoring**

Use constants first. Do not call an LLM in v1.

**Step 3: Run tests**

Run:

```bash
npm test -- tests/domain/scoring.test.ts
```

Expected: PASS.

**Step 4: Commit**

```bash
git add src/domain tests/domain/scoring.test.ts
git commit -m "feat: score github feed projects"
```

### Task 5: Render digest markdown

**Files:**
- Create: `/Users/perfectpan/Documents/rss-summary/src/render/markdown-digest.ts`
- Create: `/Users/perfectpan/Documents/rss-summary/tests/render/markdown-digest.test.ts`

**Step 1: Write failing renderer tests**

Assert that the renderer outputs:

- date heading;
- `值得看` section;
- item title and repo URL;
- actor and event reason;
- optional wiki PR link placeholder;
- no empty sections.

**Step 2: Implement Markdown renderer**

Keep the output compact enough for notification channels and readable enough for wiki raw sources.

**Step 3: Run tests**

Run:

```bash
npm test -- tests/render/markdown-digest.test.ts
```

Expected: PASS.

**Step 4: Commit**

```bash
git add src/render tests/render
git commit -m "feat: render github feed digest"
```

### Task 6: Implement wiki PR sink

**Files:**
- Create: `/Users/perfectpan/Documents/rss-summary/src/sinks/wiki-sink.ts`
- Create: `/Users/perfectpan/Documents/rss-summary/tests/sinks/wiki-sink.test.ts`

**Step 1: Write failing tests using a temp git repo**

The sink should:

- create `raw/sources/github-feed/YYYY/MM/YYYY-MM-DD.md`;
- create `raw/sources/github-feed/YYYY/MM/YYYY-MM-DD.events.json`;
- create or update branch `automation/github-feed/YYYY-MM-DD`;
- stage only those generated files;
- expose the commit message and PR body content.

**Step 2: Implement file writer first**

Use Node filesystem APIs for path creation and writes. Keep git operations behind a `GitAdapter` interface so tests can fake them.

**Step 3: Implement git adapter**

Use `git` and `gh` commands through `node:child_process`. Do not shell-interpolate secrets.

**Step 4: Run tests**

Run:

```bash
npm test -- tests/sinks/wiki-sink.test.ts
```

Expected: PASS.

**Step 5: Commit**

```bash
git add src/sinks tests/sinks
git commit -m "feat: write github digest wiki pr"
```

### Task 7: Implement notification sink

**Files:**
- Create: `/Users/perfectpan/Documents/rss-summary/src/sinks/notifier.ts`
- Create: `/Users/perfectpan/Documents/rss-summary/tests/sinks/notifier.test.ts`

**Step 1: Write failing notifier tests**

Cover:

- stdout notifier always succeeds;
- webhook notifier sends Markdown payload to configured URL;
- missing webhook URL disables webhook notifier without failing local runs;
- HTTP 4xx / 5xx returns a clear error.

**Step 2: Implement stdout and generic webhook**

Start with generic webhook. Add Telegram or Feishu-specific payloads only after the preferred channel is confirmed.

**Step 3: Run tests**

Run:

```bash
npm test -- tests/sinks/notifier.test.ts
```

Expected: PASS.

**Step 4: Commit**

```bash
git add src/sinks/notifier.ts tests/sinks/notifier.test.ts
git commit -m "feat: send github feed digest notifications"
```

### Task 8: Wire the CLI

**Files:**
- Modify: `/Users/perfectpan/Documents/rss-summary/src/main.ts`
- Create: `/Users/perfectpan/Documents/rss-summary/tests/main.test.ts`

**Step 1: Write failing integration-ish test**

Use fake source, scorer, renderer, wiki sink, and notifier. Assert the pipeline order:

```text
fetch -> dedupe -> enrich -> score -> render -> wiki -> notify
```

**Step 2: Implement orchestration**

CLI config should read:

- `GITHUB_TOKEN`
- `GITHUB_USERNAME`
- `WIKI_REPO_PATH`
- `NOTIFY_WEBHOOK_URL`
- `DIGEST_DATE`
- `DRY_RUN`

**Step 3: Run tests**

Run:

```bash
npm test
npm run typecheck
```

Expected: PASS.

**Step 4: Commit**

```bash
git add src/main.ts tests/main.test.ts
git commit -m "feat: orchestrate github feed digest"
```

### Task 9: Add GitHub Actions schedule

**Files:**
- Create: `/Users/perfectpan/Documents/rss-summary/.github/workflows/daily-github-feed.yml`
- Create: `/Users/perfectpan/Documents/rss-summary/docs/configuration.md`

**Step 1: Write configuration documentation**

Document required secrets:

- `GH_FEED_TOKEN`
- `NOTIFY_WEBHOOK_URL`
- wiki checkout deploy key or PAT with access to `PerfectPan/wiki`

**Step 2: Add scheduled workflow**

Run daily at Beijing morning time:

```yaml
on:
  schedule:
    - cron: "0 1 * * *"
  workflow_dispatch:
```

Use 01:00 UTC for 09:00 Asia/Shanghai.

**Step 3: Validate workflow syntax**

Run:

```bash
npm test
npm run typecheck
```

Expected: PASS.

**Step 4: Commit**

```bash
git add .github/workflows/daily-github-feed.yml docs/configuration.md
git commit -m "ci: schedule github feed digest"
```

### Task 10: End-to-end dry run

**Files:**
- No new files unless the dry run reveals a missing fixture or doc.

**Step 1: Run local dry run**

Run:

```bash
cd /Users/perfectpan/Documents/rss-summary
GITHUB_USERNAME=PerfectPan WIKI_REPO_PATH=/Users/perfectpan/workspace/wiki DRY_RUN=1 npm run dev
```

Expected:

- fetches received events;
- prints digest to stdout;
- does not push or open PR;
- reports generated wiki paths.

**Step 2: Run real wiki PR test on a feature branch**

Run:

```bash
GITHUB_USERNAME=PerfectPan WIKI_REPO_PATH=/Users/perfectpan/workspace/wiki npm run dev
```

Expected:

- creates `automation/github-feed/YYYY-MM-DD`;
- writes raw digest files;
- opens a draft PR against `PerfectPan/wiki`;
- notification includes the PR URL.

**Step 3: Commit final docs or fixes**

```bash
git add .
git commit -m "docs: document github feed digest operations"
```

## Validation Checklist

- `npm test`
- `npm run typecheck`
- local dry run with `DRY_RUN=1`
- one real wiki PR creation from a non-production test date
- confirm generated wiki files stay under `raw/sources/github-feed/`
- confirm no token, webhook URL, machine-specific secret, or generated log is committed
