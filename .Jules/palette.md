## 2026-08-25 - WalletHUD Accessibility\n**Learning:** Using aria-label on generic spans may not always be announced by all screen readers without a role. \n**Action:** For generic text elements, evaluate if visual tooltips (title) are sufficient or if structural roles are needed alongside ARIA labels.

## 2026-08-26 - MochilaMinera Keyboard Accessibility
**Learning:** The item-card and quest-card components were originally just divs. Adding role="button" and tabindex="0" is necessary for keyboard focus, but Vue requires both @keydown.enter and @keydown.space.prevent to fully mimic button behavior for keyboard users.
**Action:** Always ensure custom interactive elements have proper roles, tabindex, keydown handlers, and :focus-visible states.
## 2024-03-24 - Prevent Rapid Multiple Clicks on Game Choices
**Learning:** Disabling interactive choices during short state transitions (like when showing success/error feedback) prevents accidental double-clicks and clearly communicates that the UI is processing the input. Without it, users might spam-click buttons and skip ahead unexpectedly.
**Action:** Always add `:disabled` states to choice buttons when an interaction causes a temporary delay before moving to the next state, and apply styles for disabled elements such as `opacity: 0.5` and `cursor: not-allowed` while avoiding pseudo-classes like `:hover`.
## 2026-09-13 - MochilaMinera Tab Accessibility
**Learning:** Tabs need `aria-controls` to connect the tab to the `tabpanel` content, and the `tabpanel` needs `aria-labelledby` to connect back to the tab. Progress bars need `role="progressbar"`, `aria-valuenow`, `aria-valuemin`, and `aria-valuemax` to be properly announced.
**Action:** When implementing custom tabbed interfaces or progress bars, always ensure these ARIA attributes are correctly linked using IDs.
