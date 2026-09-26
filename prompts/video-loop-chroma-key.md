---
id: video-loop-chroma-key
title: Looping video with background removal
scene: When a prototype needs a video effect composited over its page background.
level: reference
tags:
  - design
  - video
  - image-generation
source: https://www.lennysnewsletter.com/p/how-to-turn-your-ai-into-a-world
source_note: Technique 5, first example.
notes:
  - The example renders the page colors into the glass effect before removing the video background.
  - Requires video generation and background removal tools.
  - The API key in the body is a source placeholder.
added: 2026-09-22
---

Can you replace the image on this page with a looping video clip that does something more interesting? Have the crystal splinter apart and slowly spin around. It should have awesome glassy effects that refract the page background and cast shadows and light around it.
To get convincing glass refraction effects, render the video of the glass over the page background colors first (so it bakes in the refraction effects), then remove the background with a video matting model.
Use this fal.ai API key: sk-a1b2c3d4…
Find appropriate recent models for video generation and background removal.
