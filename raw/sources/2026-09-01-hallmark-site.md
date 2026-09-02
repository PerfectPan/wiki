<!--
source: https://www.usehallmark.com/
type: blog
fetched: 2026-09-01
-->

02⁄Examples
## Worked examples.
One-shotted. No shared theme. No shared layout.
[$ /hallmark build a guided sourdough app, Hum](examples/hum-07/)
[$ /hallmark build a repair-café manifesto poster, custom](examples/custom-04/)
[$ /hallmark build a landing page for a small-batch honey farm](examples/garden-01/)
[$ /hallmark build a page for an indie risograph print fair](examples/riso-01/)
[$ /hallmark build a portfolio for an experimental typographer](examples/press-01/)
[$ /hallmark build a SaaS product page, modern-minimal](examples/tally/)
[$ /hallmark build a travel booking site, atmospheric](examples/wayfare/)
[$ /hallmark build a creative studio with playful motion](examples/bananastudio/)
[$ /hallmark build a software architect personal site](_tests/06-anya-portfolio/)
[$ /hallmark build a Moroccan fashion brand landing page](examples/najm/)
[$ /hallmark build a developer infrastructure landing page](examples/hyperlane/)
[$ /hallmark build a content-extraction API, Cobalt](examples/cobalt-01/)
[$ /hallmark build a record-label EP page, Carnival](examples/carnival-01/)
[$ /hallmark build an AI reasoning tool, Lumen](examples/lumen-01/)
[$ /hallmark build a poster festival site, Grid](examples/grid-01/)









          03⁄Skills
## What it does.
Hallmark has one default behaviour and three explicit verbs. Each reads a different input and returns a
        different shape — same opinions, different jobs.
  1. Invocation(default) — just
                  ask
  1. Readsyour brief, project tokens,
                  framework
  1. Picksmacrostructure → theme →
                  enrichment
  1. Returnsa working page, stamped,
                  slop-tested
  1. Refusesrepeating the last 3
                  macrostructures
**````
  1. Invocationhallmark study <screenshot | URL>
  1. MacrostructureSplit Hero
  1. Hero archetypeH7 Clipped · copy-left
                  + product-mock right
  1. Display roleheavy geometric
                  sans
  1. Body rolesame family · regular
                  weight
  1. Label rolegrotesque · sentence
                  case
  1. Paper bandlight · pure white
  1. Accent huecool blue + magenta ·
                  organic gradient
  1. Rhythmleft-copy · right product card
                  · overlapping watercolor blobs
  1. Refusesto ID fonts · to copy
                  pixels
### ``
****
  1. ✗
                Purple-to-pink gradient hero
                →
                Solid surface, single accent
  1. ✗
                Inter as display + body
                →
                Pair distinctive display + body
  1. ✗
                Centered everything
                →
                Bias the layout, break symmetry
  1. ✗
                Sparkle ✨ emoji as badge
                →
                Pick an icon library, or drop it
  1. ✗
                Gradient pill CTA
                →
                Solid fill or outline, single hue
1. Redesign
              Same content. Same brand. Different bones. Hallmark throws out the structural
                fingerprint and rebuilds with a deliberately different one — new section rhythm, new heading placement,
                new component voice.










                Before






                After Hallmark redesign
*The page* is the demo.
04⁄Anti-patterns
## Slop, by name.
Five tells the LLM reaches for by default. The Hallmark fix beside each. hallmark audit flags every
        one of these on existing code.
1. 01

            The purple-gradient hero.
            A hero with a background gradient from purple to blue or purple to pink, white
              centred text. The single most-recognised AI aesthetic.


            Hallmark
            Pick a single anchor hue. One accent. No gradient backgrounds on heroes. If
              you want warmth, tint the neutrals.
1. 02

            Inter as display.
            Inter (or Roboto, or Open Sans) used as both display and body, no pairing face. A
              one-font page is a template page.


            Hallmark
            Pair a distinctive display face with a refined body. Two faces minimum, never
              the same family doing both jobs.
1. 03

            Centred everything.
            Headline centred, body centred, button centred, section after section of centred
              columns. Symmetry as default.


            Hallmark
            Bias the layout. Wide left margin, narrow right — or the reverse. Breaking
              symmetry once is enough to register intent.
1. 04

            The icon-tile feature card.
            Rounded rectangle, icon in a coloured square top-left, two-line heading,
              three-line copy, optional "Learn more →". The universal template.


            Hallmark
            If you need feature cards, let them be asymmetric — vary sizes, vary
              alignments, pull the icon inline. Or drop the icon and lead with type.
1. 05

            The AI nav.
            Wordmark hard-left, four inline links centred, CTA button hard-right, sticky on
              scroll, hairline border-bottom. The shape every LLM ships.


            Hallmark
            Pick a nav archetype that matches the page's genre — newspaper masthead,
              terminal command bar, edge-aligned minimal. The nav should tell you what kind of site you're on.
05⁄Foundations
## Foundations.
Eight rules that hold across every theme. None of them are settings.
- A
              a


          Type
          Pair a display face with a body face. Never one font doing both jobs.
- Colour
          OKLCH palettes. One anchor hue. The accent stays under five percent.
- Space
          A named scale. Multiples of four. No arbitrary 17-pixel paddings.
- Motion
          Exponential ease-out. Reduced-motion alternative for every animation.
- Voice
          Distinct register per theme. Never the SaaS-default neutral middle.
- Layout
          Bias the page. Asymmetric is intentional. Centred everything is a tell.
- Hierarchy
          Display, body, label. A weight ladder you can read in two seconds.
- Restraint
          Better nothing than bad something. The strongest fail-state is silence.
06⁄With / Without
## Same prompt. Two different outputs.
$ /hallmark build a landing page for a dev event launch.
Sonnet 4.6, no Hallmark
Default reach for the gradient. Generic stat strip, made-up Trustpilot rating, "10× faster" feature card.



          Sonnet 4.6 + Hallmark
Marquee Hero · Atelier · italic Fraunces. Real bottle, real grape, real region. No fabricated stats.








          07⁄Install
## Install.
I Run
$
            npx skills add nutlope/hallmark


              Copied





          II In
- Claude Code
              ~/.claude/skills/hallmark/
              auto-detected
- Cursor
              .cursor/rules/hallmark.mdc
              auto-detected
- Codex
              ~/.codex/skills/hallmark/
              auto-detected
``
            ``
            ``




          III Then
Ask your agent for a UI. hallmark attaches itself.
