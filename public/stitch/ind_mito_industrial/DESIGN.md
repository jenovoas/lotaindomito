---
name: Indómito Industrial
colors:
  surface: '#131313'
  surface-dim: '#131313'
  surface-bright: '#393939'
  surface-container-lowest: '#0e0e0e'
  surface-container-low: '#1c1b1b'
  surface-container: '#20201f'
  surface-container-high: '#2a2a2a'
  surface-container-highest: '#353535'
  on-surface: '#e5e2e1'
  on-surface-variant: '#e0c0b2'
  inverse-surface: '#e5e2e1'
  inverse-on-surface: '#313030'
  outline: '#a88a7e'
  outline-variant: '#594238'
  surface-tint: '#ffb595'
  primary: '#ffb595'
  on-primary: '#571e00'
  primary-container: '#ee671c'
  on-primary-container: '#4c1a00'
  inverse-primary: '#a23f00'
  secondary: '#65dabc'
  on-secondary: '#00382d'
  secondary-container: '#1ca388'
  on-secondary-container: '#003026'
  tertiary: '#bcc9ca'
  on-tertiary: '#263334'
  tertiary-container: '#869394'
  on-tertiary-container: '#202c2d'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffdbcd'
  primary-fixed-dim: '#ffb595'
  on-primary-fixed: '#351000'
  on-primary-fixed-variant: '#7c2e00'
  secondary-fixed: '#82f7d8'
  secondary-fixed-dim: '#65dabc'
  on-secondary-fixed: '#002019'
  on-secondary-fixed-variant: '#005142'
  tertiary-fixed: '#d8e5e6'
  tertiary-fixed-dim: '#bcc9ca'
  on-tertiary-fixed: '#121e1f'
  on-tertiary-fixed-variant: '#3d494a'
  background: '#131313'
  on-background: '#e5e2e1'
  surface-variant: '#353535'
typography:
  display-lg:
    fontFamily: Montserrat
    fontSize: 48px
    fontWeight: '900'
    lineHeight: 52px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Montserrat
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
  headline-lg-mobile:
    fontFamily: Montserrat
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 30px
  title-md:
    fontFamily: Montserrat
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Work Sans
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Work Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.05em
spacing:
  unit: 4px
  gutter: 16px
  margin-mobile: 20px
  margin-desktop: 40px
  stack-sm: 8px
  stack-md: 24px
  stack-lg: 48px
---

## Brand & Style
The design system for this museum-city experience bridges the raw, heavy history of industrial coal mining with the sharp, luminous precision of modern augmented reality. The brand personality is **Indomitable, Gritty, and Illuminating**. It evokes a sense of "digital archaeology"—unearthing the past through a high-tech lens.

The aesthetic follows a **Modern-Brutalest** approach mixed with **Tactile Industrialism**. It utilizes heavy strokes, metallic textures, and high-contrast digital overlays. Interface elements should feel like refurbished machinery: heavy-duty yet responsive. Motion should be mechanical and deliberate, mimicking the torque of gears or the flicker of a miner’s lamp.

## Colors
The palette is rooted in the "Abyss and the Forge." 

- **Deep Coal Black (#1A1A1A):** The foundation. Used for backgrounds to simulate the depths of a mine.
- **Rusty Orange (#D35400):** The primary action color, representing oxidation and heritage machinery.
- **Ocean Teal (#16A085):** Secondary color for historical narratives and the coastal setting of Lota.
- **Weathered Stone (#7F8C8D):** Used for borders and secondary text to provide a sense of aged granite and concrete.
- **Neon Mint (#00FFC2):** A critical accent reserved exclusively for AR markers, digital "glitches," and interactive gamification milestones to contrast the historical grit.

## Typography
Typography is architectural and functional. **Montserrat** provides the heavy, geometric weight required for titles, echoing mid-century industrial signage. **Work Sans** is used for body copy to ensure high legibility against textured backgrounds. 

**JetBrains Mono** is introduced for technical data, coordinates, and gamified stats, reinforcing the "AR/Digital Overlay" theme. All headlines should be set in Uppercase when used for navigation or major section headers to mimic stamped metal plates.

## Layout & Spacing
The layout uses a **Rigid Grid** system inspired by blueprint schematics. 

- **Grid:** A 12-column grid for desktop and a 4-column grid for mobile.
- **Structure:** Content should be housed in clearly defined "modules" or panels. Use 2px "Weathered Stone" borders to separate zones rather than whitespace alone.
- **Rhythm:** Spacing is tight and efficient (4px base). Elements should feel packed and structural, like a control room dashboard.
- **AR Viewports:** Ensure a "Safe Zone" margin of 80px at the bottom of the screen to clear the thumb-zone for the primary gamified HUD.

## Elevation & Depth
This design system avoids soft, ambient shadows. Instead, it uses **Tonal Layering** and **Hard Insets**:

- **The Pit (Base):** Background is always the Deep Coal Black.
- **The Plate (Surface):** Cards and panels use a slightly lighter grey or a subtle noise texture to simulate rusted metal or slate.
- **The Etch:** Instead of drop shadows, use 1px inner shadows (Top/Left: Light Grey, Bottom/Right: Black) to make elements look embossed or debossed into the interface.
- **AR Overlay:** Digital elements use a "Neon Glow" (Outer Glow, 0px spread, 8px blur) in the accent mint color to appear as if projected in front of the physical world.

## Shapes
The shape language is **Sharp and Angular**. 

- **Corners:** 0px radius for all primary containers, buttons, and input fields to maintain a brutalist, industrial feel. 
- **Bevels:** Use 45-degree clipped corners (dog-ears) for "Special" items like rare artifacts or primary quest buttons to suggest a military or industrial ID tag.
- **Stroke:** All interactive containers must have a minimum 2px solid border.

## Components
- **Buttons:** Rectangular, no radius. Primary buttons use Rusty Orange with black text. Secondary buttons use a transparent background with a Stone Grey border. On hover/active, the border flickers to Neon Mint.
- **Chips/Badges:** Styled like metal rivets or stamped tags. Use JetBrains Mono for the text.
- **Input Fields:** Darker than the background, using an inset shadow and a "Weathered Stone" bottom border.
- **Cards:** Must feature a subtle "Coal Dust" grain texture. Headers of cards should be separated by a horizontal rule that mimics a weld line.
- **Progress Bars:** Segmented blocks rather than a smooth fill, resembling a mechanical gauge or gear teeth.
- **Iconography:** Use "Minimalist Industrial" icons. Lines must be consistent 2px weight. Icons like the "Coal Lamp" should "light up" (change to Neon Mint) when a location is discovered or a quest is active.
- **HUD (Heads-Up Display):** Fixed corner elements displaying coordinates and "Oxygen/Energy" levels, using thin lines and monospaced type to frame the camera view.