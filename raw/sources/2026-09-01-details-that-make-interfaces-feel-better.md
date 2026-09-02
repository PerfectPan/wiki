<!--
source: https://jakub.kr/writing/details-that-make-interfaces-feel-better
type: blog
fetched: 2026-09-01
-->

# Details that make interfaces feel better
Great interfaces rarely come from a single thing. They’re usually a collection of small things that compound into a great experience. Below are a few small details I use to make my interfaces feel better.
## Text wrapping
A quick way to improve how text behaves in your app is to use text-wrap: balance. It distributes text evenly across each line, which is ideal for titles.
wrapDesigning interfaces that feel natural and intuitive
Great design is invisible. It guides users without them ever noticing.
balanceDesigning interfaces that feel natural and intuitive
Great design is invisible. It guides users without them ever noticing.
Width220pxHide guidestext-wrap: balance distributes text evenly across lines
You can also use text-wrap: pretty to prevent orphaned words at the end of sentences. This is better suited for paragraphs rather than titles.
wrapDesigning interfaces that feel natural and intuitive
Great design is invisible. It guides users without them ever noticing.
prettyDesigning interfaces that feel natural and intuitive
Great design is invisible. It guides users without them ever noticing.
Width215pxHide guidestext-wrap: pretty prevents orphaned words at the end of a paragraph.
In practice, you’ll often pair them: text-wrap: balance on the title and text-wrap: pretty on the description.
wrapDesigning interfaces that feel natural and intuitive
Great design is invisible. It guides users without them ever noticing.
balance + prettyDesigning interfaces that feel natural and intuitive
Great design is invisible. It guides users without them ever noticing.
Width220pxHide guidesI often pair these two properties. text-wrap: balance on the title and text-wrap: pretty on the description.
## Concentric border radius
Concentric offset is a technique used to create a balanced visual look when nesting elements inside one another. This is one of the more important concepts that make interfaces feel great and it often goes unnoticed.
padding: 8px12px12px20px12pxShow Values
There is a formula to calculate the correct values and it’s very simple. The outer radius equals the inner radius plus the padding.
outer radiusinner radiuspadding
There’s still a surprising number of apps and interfaces that don’t do this and instead mismatch border radii. If you’re not already doing this, I’d recommend starting. It will make your interfaces feel much better.
Outer radius20pxInner radius12pxPadding8pxChange the values to see how the border radius adapts
## Animate icons contextually
Animating opacity, scale and blur on icons when they are shown contextually makes the transition feel better and more responsive.

```
<button onClick={handle} className="button">
  {isCopied ? <CheckIcon /> : <Icon />}
</button>
```
MotionCSS
No AnimationOpacityAllno-animation.tsx
You can achieve the same effect with CSS alone as well. I personally prefer Motion, because it allows me to use spring animations easily.
## Make text crispy
On macOS, text rendering can sometimes appear heavier than intended.
Subpixel rendering
Default font smoothing uses subpixel antialiasing on macOS.
Antialiased rendering
Grayscale antialiasing produces thinner, crisper light text.
Setting -webkit-font-smoothing: antialiased or just antialiased in Tailwind makes text render slightly thinner and crisper.

```
<html lang="en">
  <body class="font-sans antialiased">
    <main>
      {children}
    </main>
  </body>
</html>
```
layout.tsx
The best way to apply this is to add it to the entire layout. That way it applies to all of the text elements in your app.
## Use tabular numbers
If your numbers shift when they update, use font-variant-numeric: tabular-nums or just tabular-nums in Tailwind.
10001000Click the play button to make the numbers run up
It makes the digits equal width. Keep in mind that some fonts, such as Inter, change the look of numerals when this property is used.
## Make your animations interruptible
When it comes to interruptibility, CSS transitions and keyframe animations behave differently. Transitions interpolate toward the latest state and can be interrupted, while keyframe animations run on a fixed timeline and don’t retarget after they start.
CSS keyframeCSS transitionRotateClick the rotate button rapidly to see the difference
Users often change their intent mid-interaction. For example, a user may open a dropdown menu and decide they want to do something else before the animation finishes.
AnimateTry to toggle the animation again while it’s running
If animations aren’t interruptible, it can make the interface feel broken. For example, on iOS, interruptibility is quite prevalent for this very reason.
MenuMenuFastInterrupt the animation while it’s running to see the difference
A rule of thumb that can help you decide when to use CSS transitions vs keyframe animations is that CSS transitions are great for interactions, while keyframe animations are better for staged sequences that run once.
ToggleInterrupt the animation while it’s running to see the difference
## Split and stagger entering elements
Enter animations often combine opacity, blur and translateY. It helps to break the animated components into smaller chunks and animate them individually instead of animating a big block at once.
Build software that never breaksInterfere is the experience layer for modern product teams. Detect, triage, and fix bugs automatically.Request a demoJoin waitlistBlockSectionsIndividual
The first variant animates a single container that holds the title, description and buttons. The second variant animates the title, description and buttons individually, with a 100ms delay between each section.

```
<div className="animate-enter" style={{ "--stagger": 1 }}>
  <Title />
</div>
<div className="animate-enter" style={{ "--stagger": 2 }}>
  <Description />
</div>
<div className="animate-enter" style={{ "--stagger": 3 }}>
  <Buttons />
</div>
```
staggered-enter.tsx
The third variant animates the title by splitting it into individual spans. Each span contains a word and is animated individually with an 80ms delay between them.

```
@keyframes enter {
  from {
    transform: translateY(8px);
    filter: blur(8px);
    opacity: 0;
  }
}

.animate-enter {
  animation: enter 800ms cubic-bezier(0.25, 0.46, 0.45, 0.94) both;
  animation-delay: calc(var(--delay, 0ms) * var(--stagger, 0));
}

.animate-enter-individual-title {
  --delay: 80ms;
}
```
enter-animation.css
The description remains a single block and the buttons are also animated individually rather than as one container.
## Make exit animations subtle
Exit animations often work better when they’re more subtle than enter animations.
AnimateToggle the animation to compare the subtle and full exits side by side
The exiting elements don’t need the same amount of attention as the ones entering. In the first example, we only animate x between 0 and calc(-100% - 4px), which is the drawer’s full width plus the padding. This way it slides all the way off screen.

```
<motion.div
  key="menu"
  className="container"
  initial={{ x: "calc(-100% - 4px)" }}
  animate={{ x: 0 }}
  exit={{ x: "calc(-100% - 4px)" }}
  transition={{ type: "spring", duration: 0.45, bounce: 0 }}
/>
```
exit-animation.tsx
In the second example, when the element exits, we don’t animate x at all. We instead animate opacity and filter.

```
<motion.div
  key="menu"
  className="container"
  initial={{ x: "calc(-100% - 4px)" }}
  animate={{ x: 0 }}
  exit={{ opacity: 0, filter: "blur(4px)" }}
  transition={{ type: "spring", duration: 0.45, bounce: 0 }}
/>
```
subtle-exit-animation.tsx
By doing this, the exit animation becomes much softer and less jarring. It doesn’t demand the same amount of attention as the enter animation.
## Align optically, not geometrically
Aligning items geometrically works great most of the time, but there are instances where it just looks off. When that happens, it is best to align items optically instead.
GeometricOpticalButtonShow Padding
For example, when a button has both text and an icon, it is better to have slightly less padding on the side of the icon to optically align the content.
GeometricOpticalShow MarginChange the alignment mode and click the button to see the difference. In this example only the Play icon is optically aligned.
This often happens with icons. While a lot of icon packs already account for this, there are shapes that need to be optically aligned. I usually fix it by adding margin or padding depending on the container.
GeometricOpticalShow MarginChange the alignment mode and click the button to see the difference
For icons, the best way to fix it is in the svg itself, so no additional margin or padding needs to be added.
## Use shadows instead of borders
Instead of borders, I often prefer to use a subtle box-shadow that adds more depth to the element. The change is mostly noticeable in light mode, but it applies to dark mode too. In dark mode the shadow looks like a border would.
BorderShadow
The shadow in this example is composed of three different shadows.

```
.border-shadow {
  box-shadow:
    0px 0px 0px 1px rgba(0, 0, 0, 0.06),
    0px 1px 2px -1px rgba(0, 0, 0, 0.06),
    0px 2px 4px 0px rgba(0, 0, 0, 0.04);
}

@media (prefers-color-scheme: dark) {
  .border-shadow {
    box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.08);
  }
}
```
border-shadow
For the hover state, it is the same box-shadow, just slightly darker. To transition between the shadows, we can use transition-property: box-shadow;.

```
.border-shadow {
  box-shadow:
    0px 0px 0px 1px rgba(0, 0, 0, 0.08),
    0px 1px 2px -1px rgba(0, 0, 0, 0.08),
    0px 2px 4px 0px rgba(0, 0, 0, 0.06);
}

@media (prefers-color-scheme: dark) {
  .border-shadow {
    box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.12);
  }
}
```
border-shadow-hover
It also helps when using images or multiple colors as backgrounds. Shadows are versatile and adapt well to any background since they use transparency.
BorderShadow
Solid colors, on the other hand, don’t work well when used on backgrounds other than the ones they were designed for.
## Add an outline to images
A visual tweak I use a lot is adding a 1px black or white (depending on the mode) outline with 10% opacity to images.
Show Border
This creates a sense of depth and a somewhat consistent outline around the element.

```
.border-overlay {
  outline: 1px solid rgba(0, 0, 0, 0.1);
  outline-offset: -1px;
}

.dark .border-overlay {
  outline-color: rgba(255, 255, 255, 0.1);
}
```
image-outline.css
I mostly use this in design systems where other elements also use borders.
## Show Border
Skill
I’m glad that [a lot of people (opens in a new tab)](https://x.com/jakubkrehel/status/2031414681043186004) found this article useful. Based on the feedback I got, I decided to turn the tips from this article into a skill.
npx skills add jakubkrehel/make-interfaces-feel-better[Skills (opens in a new tab)](https://skills.sh/jakubkrehel/make-interfaces-feel-better/make-interfaces-feel-better)[GitHub (opens in a new tab)](https://github.com/jakubkrehel/make-interfaces-feel-better)
You can install it by running the command in your terminal. The skill is available for Claude Code, Codex, Cursor Agent, Gemini CLI and more.
After you install the skill, navigate to the root of the project you want to use it in and run the skill by typing /make-interfaces-feel-better.
## More
If you enjoy articles like this and want to learn more, take a look at Interfaces, my design engineering magazine.
It’s where I share everything I know, from animation and typography to layout, color and everything else that is a part of building a *great* interface.
