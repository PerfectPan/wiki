<!--
source: https://www.rareui.com/components/otpinput
type: blog
fetched: 2026-09-09
-->

## Components
# Display[Folder component](/components/foldercomponent)[Code Block](/components/codeblock)[Gravity Letters](/components/gravityletters)[GitHub activity](/components/githubactivity)[Step player](/components/stepplayer)[Animated counter](/components/animatedcounter)AI kit[Fluid Orb](/components/fluidorb)[Grid Reveal](/components/gridreveal)[Matrix orb](/components/matrixorb)Navigation[Bounce sidebar](/components/bouncesidebar)[Hook Sidebar](/components/hooksidebar)[Proximity Sidebar](/components/proximitysidebar)[Scroll Progress](/components/scrollprogressindicator)[Gooey nav](/components/gooeynav)Inputs[Duration Picker](/components/durationpicker)[OTP Input](/components/otpinput)[Delete button](/components/deletebutton)Feedback[Emoji reaction](/components/emojireaction)[Notification bell](/components/notificationbell)InstallInstallOTP Input
A one-time-code input whose characters roll into place behind a caret that slides from slot to slot.
## Dependencies
## motionInteraction Type
Type to fill each slot and move to the next one. Backspace clears a slot in place, then steps back on the next press. Arrow keys move between slots, and a caret slides along with you. Pasting a code, or letting the phone autofill one from a text message, drops it straight in. Set the status to turn the slots green, or shake them red on a wrong code.
## Props
Options you can pass to customize this component.
PropTypeDescriptionlengthnumberHow many boxes to render, so a 4 digit code is length={4}. Any count works.
sizesmmdlgOverall scale of the boxes. Maps to 40px (sm), 48px (md), and 56px (lg), and carries the text, caret, and gaps with it.
valuestringThe current code. Pass it to control the input yourself; leave it out to let the component track its own state.
defaultValuestringStarting code when the input is uncontrolled.
onChange(value: string) => voidFires on every edit with the full code so far.
onComplete(value: string) => voidFires once the last slot is filled.
typenumberslettersbothWhich characters a slot accepts. Anything else is ignored, including on paste.
statusidlesuccesserrorDrives the feedback state. Success traces a green ring around each box in turn, error rings them red and shakes the row once.
maskbooleanHides the characters, like a password field.
disabledbooleanBlocks input and dims every slot.
autoFocusbooleanFocuses the first slot on mount.
classNamestringExtra classes for the row that wraps the slots.
slotClassNamestringExtra classes for each slot, for sizing and colors.
## Installation
## npmpnpmyarnbunnpx shadcn@latest add swamimalode07/rare-ui/otp-inputHow to use

```
import { useState } from "react"import OtpInput, { type OtpStatus } from "@/components/ui/otp-input"
export function Demo() {  const [status, setStatus] = useState<OtpStatus>("idle")
  return (    <OtpInput      length={6}      size="md"      status={status}      onChange={() => setStatus("idle")}      onComplete={(code) => setStatus(checkCode(code) ? "success" : "error")}    />  )}
```
## Source Code
Click the code icon in the top-right corner to view the source code.
## Keep in mind
Most components here are recreations of great work from around the web. I don't claim to be the original creator - this is my attempt to reverse-engineer, replicate, and often add a few extra features. I've tried to credit everyone; if I missed someone, let me know.
## Contact
Found a bug or issue? Feel free to drop a DM.
## License & Usage
- •Free to use and modify in both personal and commercial projects.
- •Attribution to Rare UI is appreciated when using a component.
- •Please don't resell the components as your own kit.

```
1

```
OTP InputEnter 123456 to pass. Any other code fails.
