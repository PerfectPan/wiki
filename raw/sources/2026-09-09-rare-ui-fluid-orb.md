<!--
source: https://www.rareui.com/components/fluidorb
type: blog
fetched: 2026-09-09
-->

## Components
# Display[Folder component](/components/foldercomponent)[Code Block](/components/codeblock)[Gravity Letters](/components/gravityletters)[GitHub activity](/components/githubactivity)[Step player](/components/stepplayer)[Animated counter](/components/animatedcounter)AI kit[Fluid Orb](/components/fluidorb)[Grid Reveal](/components/gridreveal)[Matrix orb](/components/matrixorb)Navigation[Bounce sidebar](/components/bouncesidebar)[Hook Sidebar](/components/hooksidebar)[Proximity Sidebar](/components/proximitysidebar)[Scroll Progress](/components/scrollprogressindicator)[Gooey nav](/components/gooeynav)Inputs[Duration Picker](/components/durationpicker)[OTP Input](/components/otpinput)[Delete button](/components/deletebutton)Feedback[Emoji reaction](/components/emojireaction)[Notification bell](/components/notificationbell)InstallInstallFluid Orb
An animated WebGL orb with drifting fluid shading, inspired by ChatGPT's voice mode.
## Interaction Type
Ambient — the color patches drift left, right, up, down and diagonally on their own, blending and reforming with no interaction required. Honors prefers-reduced-motion by holding a still frame.
## Props
Options you can pass to customize this component.
PropTypeDescriptioncolor#1A73F2#FF3B30#F75001#34C759Any hex color for the fluid. The middle and bottom bands are derived from it (a pale tint and the full color), while the top stays white. Defaults to the original blue.
sizenumberDiameter of the orb in pixels.
classNamestringExtra classes merged onto the root element (data-slot="fluid-orb").
## Installation
## npmpnpmyarnbunnpx shadcn@latest add swamimalode07/rare-ui/fluid-orbHow to use

```
import FluidOrb from "@/components/ui/fluid-orb"
export function Demo() {  return <FluidOrb size={280} color="#F75001" />}
```
## Source Code
Click the code icon in the top-right corner to view the source code.
## Keep in mind
Most components here are recreations of great work from around the web. I don't claim to be the original creator - this is my attempt to reverse-engineer, replicate, and often add a few extra features. I've tried to credit everyone; if I missed someone, let me know.
## Credits
- •Inspired by chatgpt.com
## Contact
Found a bug or issue? Feel free to drop a DM.
## License & Usage
- •Free to use and modify in both personal and commercial projects.
- •Attribution to Rare UI is appreciated when using a component.
- •Please don't resell the components as your own kit.

```
1

```
