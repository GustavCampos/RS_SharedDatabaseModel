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

document.addEventListener("DOMContentLoaded", function () {
    const elementsToMask = document.querySelectorAll('[data-mask]')

    for (let element of elementsToMask) {
        element.setAttribute("data-value", element.textContent)

        switch (element.getAttribute("data-mask")) {
            case "cpf": {
                element.textContent = formatCPF(element.textContent)
                break;
            }
            case "phone": {
                element.textContent = formatPhone(element.textContent)
                break;
            }
        }
    }
})