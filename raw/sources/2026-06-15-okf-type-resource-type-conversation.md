---
title: OKF type and resource_type conversation
captured: 2026-06-15
source:
  - conversation with 董事长 on OKF, BigQuery examples, type filtering, and export mapping
---

# OKF type and resource_type conversation

## Context

This conversation refined how this wiki should map its internal page model to OKF.

The key question was whether OKF is only a Markdown documentation format, or whether it describes real resources such as BigQuery tables, API endpoints, metrics, dashboards, playbooks, automation jobs, and other assets.

## Decisions

- OKF should be treated as a semantic wrapper around real resources, not merely as a document store.
- Google's BigQuery examples show that OKF `type` can represent resource object types such as `BigQuery Table` or `BigQuery Dataset`.
- OKF `type` is used by consumers for routing, filtering, and presentation.
- This wiki's internal `type` should remain fixed as page role: `topic`, `synthesis`, or `comparison`.
- Real external resource type should be represented with optional `resource_type`, not by overloading internal `type`.
- `resource` should point to the real resource or source pointers.
- Export should support two modes:
  - knowledge mode: keep OKF `type` as internal page role.
  - resource mode: map `resource_type` to OKF `type` and preserve internal page role as `page_type`.

## Rationale

Keeping internal `type` fixed makes the wiki easier for agents to read, lint, and route. Adding optional `resource_type` preserves room for resource-catalog use cases without destabilizing existing page semantics.

