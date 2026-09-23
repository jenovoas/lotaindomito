## 2026-08-25 - WalletHUD Accessibility\n**Learning:** Using aria-label on generic spans may not always be announced by all screen readers without a role. \n**Action:** For generic text elements, evaluate if visual tooltips (title) are sufficient or if structural roles are needed alongside ARIA labels.

## 2026-08-26 - MochilaMinera Keyboard Accessibility
**Learning:** The item-card and quest-card components were originally just divs. Adding role="button" and tabindex="0" is necessary for keyboard focus, but Vue requires both @keydown.enter and @keydown.space.prevent to fully mimic button behavior for keyboard users.
**Action:** Always ensure custom interactive elements have proper roles, tabindex, keydown handlers, and :focus-visible states.
## 2024-03-24 - Prevent Rapid Multiple Clicks on Game Choices
**Learning:** Disabling interactive choices during short state transitions (like when showing success/error feedback) prevents accidental double-clicks and clearly communicates that the UI is processing the input. Without it, users might spam-click buttons and skip ahead unexpectedly.
**Action:** Always add `:disabled` states to choice buttons when an interaction causes a temporary delay before moving to the next state, and apply styles for disabled elements such as `opacity: 0.5` and `cursor: not-allowed` while avoiding pseudo-classes like `:hover`.
## 2024-05-18 - Accessible Modals with Dynamic Headings
**Learning:** When building multi-step modals where the primary heading (`h3` or `h4`) changes depending on the active step (e.g., intro, game, reward), using `aria-labelledby` with a static ID isn't viable because the heading element itself might be conditionally rendered (`v-if`/`v-else-if`), leading to missing or dangling references.
**Action:** In these cases, use `aria-label` directly on the element with `role="dialog"` providing a general, constant description of the modal's purpose (e.g., `aria-label="Micro-sesión"`) instead of relying on an internal dynamic heading ID.
## 2026-09-23 - Progress Bar ARIA Attributes
**Learning:** Visual progress indicators (like hold-bars or progress bars) require specific ARIA attributes for proper accessibility, specifically `role="progressbar"`, `aria-valuemin`, `aria-valuemax`, and `aria-valuenow`.
**Action:** Always ensure any dynamic visual progress indicator includes the complete set of standard ARIA progress bar attributes to be accessible to screen readers.
