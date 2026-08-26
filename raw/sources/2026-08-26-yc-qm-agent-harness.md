<!--
source: https://qm.ycombinator.com/
type: blog
author: Y Combinator
published: 2026-07
fetched: 2026-08-26
-->

# QM — Open-Source Agent Harness from YC

July 2026

We're open-sourcing an agent harness we call QM.[1]

It allows startups (and YC) to work with a fleet of OpenClaw-like agents. Every employee and project gets one, as needed.

It's designed to be easy to administer and especially helpful for work-related tasks.

YC has experimented with several harnesses, and this is the result of those learnings. The first was a basic agent loop in Ruby, with some tools that could access internal data. It was easy for people to get value from on day one, but it was limited in the scope of what it could do. We eventually extended it to support things like crons, and webhook triggers, but the launch of OpenClaw pushed us in a new direction.

Next we provisioned over 50 Hermes agents for individual employees to work as personal assistants. Managing a fleet of even this size became challenging. We wanted something that was as flexible as Hermes, but with the simplicity of our original system.

We also wanted something that we could own and host ourselves. The open source ecosystem is incredibly important, and we want to see it continue to develop.

The code is at [github.com/yc-software/qm](https://github.com/yc-software/qm).

If you find it useful, or have questions, send an email to labs@ycombinator.com.

## Notes

[1] Short for quartermaster, the person on a ship who coordinates belowdecks to keep things in order.
