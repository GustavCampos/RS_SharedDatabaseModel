import { applyCustomMasks } from "./utils/mask"

// Apply masks after the table loads
document.addEventListener("DOMContentLoaded", () => {
  applyCustomMasks('clickableTable');
});
