---
id: keyframe-transition-scrub
title: Scroll through video transitions
scene: When a prototype needs scroll-controlled transitions between visual states.
level: reference
tags:
  - design
  - video
  - interaction
source: https://www.lennysnewsletter.com/p/how-to-turn-your-ai-into-a-world
source_note: Technique 5, second example.
notes:
  - The last frame of each clip supplies the starting frame for the next clip.
  - The source names a specific video model; availability and output quality need verification.
  - The API key in the body is a source placeholder.
added: 2026-09-22
---

Build a demo page for a suitcase that uses a video model to create interactive transitions between a couple of screens. Each screen should show the suitcase in a different state, with vertical motion that feels appropriate for scrolling:
- Initially, have the suitcase floating high up in the air
- Then have it land on the floor and pop open
- Finally, have its contents neatly land into it from the top
Generate the initial frame using your image generation skill. Then, generate a video clip that starts from that frame and animates to the next state. Use the final frame of that video to seed the next transition so that it continues seamlessly. Scrub through the transitions one by one as the user scrolls.
Use this fal.ai API key: sk-a1b2c3d4…
Use a video model with strong physics and consistency, like Seedance 2.5.
