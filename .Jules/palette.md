## 2026-08-25 - WalletHUD Accessibility\n**Learning:** Using aria-label on generic spans may not always be announced by all screen readers without a role. \n**Action:** For generic text elements, evaluate if visual tooltips (title) are sufficient or if structural roles are needed alongside ARIA labels.

## 2026-08-26 - MochilaMinera Keyboard Accessibility
**Learning:** The item-card and quest-card components were originally just divs. Adding role="button" and tabindex="0" is necessary for keyboard focus, but Vue requires both @keydown.enter and @keydown.space.prevent to fully mimic button behavior for keyboard users.
**Action:** Always ensure custom interactive elements have proper roles, tabindex, keydown handlers, and :focus-visible states.
