/**
 * Apply a mask to table cells based on a custom attribute.
 * @param {string} tableId - ID of the table
 */
function applyCustomMasks(table) {
    const cells = table.querySelectorAll('td[data-mask]');
  
    cells.forEach(cell => {
      const maskType = cell.dataset.mask;
      const originalValue = cell.dataset.value;
  
      // Check the mask type and apply the corresponding function
      if (maskType === "cpf") {
        cell.textContent = formatCPF(originalValue);
      } else if (maskType === "phone") {
        cell.textContent = formatPhone(originalValue);
      }
      // Add more mask types as needed
    });
  }
  
  /**
   * Format a string as a CPF.
   * @param {string} value - The CPF string to format
   * @returns {string} - Formatted CPF
   */
  function formatCPF(value) {
    value = value.replace(/\D/g, "");
    value = value.replace(/(\d{3})(\d)/, "$1.$2");
    value = value.replace(/(\d{3})(\d)/, "$1.$2");
    value = value.replace(/(\d{3})(\d{1,2})$/, "$1-$2");
    return value;
  }
  
  /**
   * Format a string as a phone number.
   * @param {string} value - The phone number string to format
   * @returns {string} - Formatted phone number
   */
  function formatPhone(value) {
    value = value.replace(/\D/g, "");
    value = value.replace(/(\d{2})(\d{4,5})(\d{4})/, "($1) $2-$3");
    return value;
  }

document.addEventListener("DOMContentLoaded", function() {
    const tables = document.getElementsByClassName("table-component");
    
    for (let table of tables) {
        applyCustomMasks(table);
    }
})