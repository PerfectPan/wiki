---
title: Google Cloud Open Knowledge Format source note
source:
  - https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing/
  - https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf
  - https://raw.githubusercontent.com/GoogleCloudPlatform/knowledge-catalog/main/okf/SPEC.md
captured: 2026-06-15
---

# Google Cloud Open Knowledge Format source note

## Source facts

- Google Cloud published "Introducing the Open Knowledge Format" on 2026-06-12.
- OKF v0.1 is described as an open specification for representing metadata, context, and curated knowledge in a human- and agent-friendly format.
- The format models a knowledge bundle as a directory of Markdown files with YAML frontmatter.
- The only required frontmatter field is `type`.
- The spec says consumers use `type` for routing, filtering, and presentation, and should tolerate unknown types gracefully.
- Recommended fields include `title`, `description`, `resource`, `tags`, and `timestamp`.
- Concept identity is derived from the file path without the `.md` suffix.
- OKF uses standard Markdown links between concept documents; absolute bundle-relative links are recommended for stability.
- `index.md` is optional and supports progressive disclosure.
- `log.md` is optional and represents chronological history, but the spec also recommends Git repositories as a distribution form because they provide history, attribution, and diffs.
- The spec is deliberately minimal: it does not define a central schema registry, a fixed taxonomy of types, a required SDK, or a required serving/query runtime.

## Local reading

OKF is less important as a Google Cloud product announcement than as a signal that file-first, Markdown-first, agent-readable knowledge bases are becoming a standardizable pattern.

For this wiki, the useful conclusion is not to copy OKF wholesale. The better direction is OKF-compatible:

- keep the existing `raw/` and `wiki/` separation;
- keep branch plus PR review as the governance layer;
- add `description`, `resource`, and `timestamp` as export-friendly fields;
- convert Obsidian wikilinks to standard Markdown links only in an export path;
- treat Git and PRs as the durable change history instead of maintaining a duplicate hand-written `log.md`.
- keep using `type` as the wiki page role (`topic`, `synthesis`, `comparison`) and use `category` / `tags` for domain filtering. If a page describes a real external resource, add an optional `resource_type` field instead of overloading the internal `type`.
