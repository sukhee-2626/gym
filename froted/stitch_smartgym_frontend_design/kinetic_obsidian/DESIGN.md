```markdown
# Design System Strategy: The Kinetic Frontier

## 1. Overview & Creative North Star
**Creative North Star: "The Synthetic Pulse"**
This design system rejects the static nature of traditional SaaS dashboards. Instead, it treats the UI as a living, breathing organism—a "Synthetic Pulse" that mirrors the high-energy, data-driven environment of a state-of-the-art gym. We move beyond "templates" by employing intentional asymmetry, overlapping "glass" panes, and a depth model that feels like a futuristic HUD (Heads-Up Display).

The experience is defined by **Kinetic Energy**. Every interaction should feel fluid and intentional. We break the grid by allowing neon "light-leaks" and organic "orb" particles to drift behind the functional layer, creating a sense of infinite digital space.

## 2. Color Strategy
Our palette is rooted in a deep, nocturnal base (`surface`), punctuated by high-vibrancy "Electric" accents. 

### The "No-Line" Rule
Traditional 1px solid borders are strictly prohibited for sectioning. Structural definition must be achieved through:
1.  **Tonal Shifts:** Placing a `surface_container_high` element against a `surface` background.
2.  **Luminescent Shadows:** Using the `secondary` or `primary` glow to define the edge of a focused element.
3.  **Glass Differentiation:** Relying on `backdrop-filter: blur(20px)` to create a perceived boundary between layers.

### Surface Hierarchy & Nesting
Treat the UI as a stack of physical, semi-transparent materials.
*   **Base Layer:** `surface` (#0b0e14) — The dark void.
*   **Sectional Layer:** `surface_container_low` — Sub-regions of the app.
*   **Component Layer:** `surface_container_highest` — The most interactive elements (cards, inputs).
*   **Floating Layer:** Glassmorphic panes using `surface_variant` at 40% opacity with blur.

### The "Glass & Gradient" Rule
To achieve the premium, state-of-the-art feel, all primary CTAs and high-level data visualizations must utilize a **Neon Mesh Gradient**. Transition from `primary_dim` (#bb00fc) to `secondary` (#00eefc) to create a sense of movement.

## 3. Typography: The Modern Architectural Scale
We use a high-contrast pairing of **Space Grotesk** for structural impact and **Manrope** for technical clarity.

*   **Display & Headlines (Space Grotesk):** These are our "Impact" levels. Bold weights are mandatory. Use `display-lg` (3.5rem) for high-energy motivational stats or hero titles. These should feel like architectural statements.
*   **Titles & Body (Manrope):** The "Utility" levels. Manrope provides a sophisticated, technical feel that remains legible even at `body-sm` (0.75rem). 
*   **Tonal Hierarchy:** Use `on_surface` for primary content and `on_surface_variant` for metadata. Never use pure white text; it vibrates too harshly against the dark background.

## 4. Elevation & Depth
Depth in this system is a product of **Luminance**, not just shadow.

*   **The Layering Principle:** Instead of standard shadows, we use "Stacking." A `surface_container_lowest` item nested inside a `surface_container_high` creates an "etched" look.
*   **Ambient Glows:** For floating elements (Modals, Hovered Cards), use a shadow tinted with the `primary` token (#df8eff) at 5% opacity. The blur radius should be large (32px–64px) to mimic a neon tube's glow.
*   **The "Ghost Border" Fallback:** Where containment is critical for accessibility, use `outline_variant` (#45484f) at **15% opacity**. This creates a "hairline" edge that feels like a reflection on glass rather than a physical stroke.
*   **Backdrop Blur:** All floating components must implement `backdrop-filter: blur(12px)`.

## 5. Components

### Cards
*   **Design:** No dividers. Separate header from body using a 24px padding (`xl`).
*   **Effect:** Apply a `0.5px` top-border (Ghost Border) to simulate a "light-catching" edge on glass. 
*   **Hover State:** Increase backdrop-blur and apply a subtle `secondary_dim` outer glow.

### Buttons
*   **Primary:** Gradient fill (`primary_dim` to `tertiary_dim`). Border-radius: `full`.
*   **Secondary:** Glassmorphic background with a `secondary` ghost border.
*   **Tertiary:** No background. Bold `primary` text with a micro-glow on hover.

### High-Tech Inputs
*   **Visual:** `surface_container_lowest` background. 
*   **Active State:** The bottom edge glows with a 2px `secondary` gradient. Use "floating" labels in `label-sm`.

### Sidebar (Desktop) & Bottom Bar (Mobile)
*   **Style:** Ultra-glassmorphic. These should feel like they are floating over the background orbs.
*   **Active Indicator:** Use a vertical "light bar" in `secondary` next to the active menu item. Avoid blocky "active background" shapes.

### The "Pulse" Indicator (Context-Specific)
*   **Function:** A small, animated dot using `secondary` with a radiating pulse effect to show "Live" AI workout tracking or active gym occupancy.

## 6. Do’s and Don’ts

### Do:
*   **Do** use asymmetrical layouts. A sidebar that doesn't reach the bottom of the screen feels more "premium" and custom.
*   **Do** use `primary_container` for subtle highlights behind text to create "highlighter" effects for key metrics.
*   **Do** ensure all "glass" components have high contrast against the `on_surface` text for WCAG compliance.

### Don’t:
*   **Don’t** use solid black (#000000) for anything except the absolute lowest surface tier (`surface_container_lowest`).
*   **Don’t** use standard 1px borders or heavy dividers. They break the "Liquid" feel of the system.
*   **Don’t** animate with "linear" easing. Use `cubic-bezier(0.22, 1, 0.36, 1)` for a "slick, heavy" movement feel.
*   **Don’t** clutter the screen. If you have a particle background, give the UI elements enough `xl` (1.5rem) spacing to let the "energy" breathe through.