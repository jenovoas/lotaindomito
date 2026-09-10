## 2026-08-25 - WalletHUD Accessibility\n**Learning:** Using aria-label on generic spans may not always be announced by all screen readers without a role. \n**Action:** For generic text elements, evaluate if visual tooltips (title) are sufficient or if structural roles are needed alongside ARIA labels.

## 2026-08-26 - MochilaMinera Keyboard Accessibility
**Learning:** The item-card and quest-card components were originally just divs. Adding role="button" and tabindex="0" is necessary for keyboard focus, but Vue requires both @keydown.enter and @keydown.space.prevent to fully mimic button behavior for keyboard users.
**Action:** Always ensure custom interactive elements have proper roles, tabindex, keydown handlers, and :focus-visible states.
## 2024-03-24 - Prevent Rapid Multiple Clicks on Game Choices
**Learning:** Disabling interactive choices during short state transitions (like when showing success/error feedback) prevents accidental double-clicks and clearly communicates that the UI is processing the input. Without it, users might spam-click buttons and skip ahead unexpectedly.
**Action:** Always add `:disabled` states to choice buttons when an interaction causes a temporary delay before moving to the next state, and apply styles for disabled elements such as `opacity: 0.5` and `cursor: not-allowed` while avoiding pseudo-classes like `:hover`.


**Learning:** Custom modals should always allow users to dismiss them by clicking the background overlay (`@click.self`). Furthermore, custom modal elements need `role="dialog"` and `aria-modal="true"` alongside a descriptive label (like `aria-label`) to be fully accessible to screen readers.

## 2026-09-10 - Modal Backdrop Dismissal and Accessibility
**Learning:** Custom modals should always allow users to dismiss them by clicking the background overlay (`@click.self`). Furthermore, custom modal elements need `role="dialog"` and `aria-modal="true"` alongside a descriptive label (like `aria-label`) to be fully accessible to screen readers.
**Action:** When creating or updating custom modals, always implement background click dismissal and ensure standard ARIA dialog attributes are present.
