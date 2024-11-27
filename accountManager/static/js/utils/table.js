/**
 * Filter table rows based on input value.
 * @param {Event} event - Input event
 * @param {Element} table - table html element
 */
function filterTable(event, table) {
    const filter = event.target.value.toLowerCase();
    const rows = table.querySelector('tbody').getElementsByTagName('tr');

    for (const row of rows) {
        const cells = row.getElementsByTagName('td');
        let isVisible = false;

        for (const cell of cells) {
            if (cell.textContent.toLowerCase().includes(filter)) {
                isVisible = true;
                break;
            }
        }

        row.style.display = isVisible ? '' : 'none';
    }
}

/**
 * Sort table rows by column.
 * @param {Event} event - Click event
 * @param {Element} table - Table Element
 * @param {number} colIndex - Index of the column to sort by
 */
function sortTable(event, table, colIndex) {
    const headers = table.querySelectorAll('th');
    for (const header of headers) {
        const icon = header.querySelector("i");
        if (icon) {
            icon.className = "fa-solid fa-sort";
        }
    }

    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.getElementsByTagName('tr'));
    const ascending = !event.target.dataset.ascending || event.target.dataset.ascending === 'false';

    // Sort rows
    rows.sort((a, b) => {
        const aText = a.getElementsByTagName('td')[colIndex].textContent.trim().toLowerCase();
        const bText = b.getElementsByTagName('td')[colIndex].textContent.trim().toLowerCase();

        if (aText < bText) return ascending ? -1 : 1;
        if (aText > bText) return ascending ? 1 : -1;
        return 0;
    });

    // Append sorted rows
    rows.forEach(row => tbody.appendChild(row));

    // Update sort direction and icon
    event.target.dataset.ascending = ascending;
    const icon = event.target.querySelector("i");
    if (icon) {
        icon.className = ascending ? "fa-solid fa-sort-up" : "fa-solid fa-sort-down";
    }
}

/**
 * Access item page.
 * @param {Event} event - Click event
 * @param {string} goTo - URL of the client
 */
function accessTableItem(event, goTo) {
    event.preventDefault();
    window.location.replace(goTo);
}

document.addEventListener("DOMContentLoaded", function(e) {
    const tables = document.getElementsByClassName("table-component");

    for (let component of tables) {
        const filter = component.querySelector("input");
        const table = component.querySelector("table");
        const headers = table.querySelectorAll('th');

        filter.addEventListener("change", (e) => {
            filterTable(e, table);
        });

        for (const header of headers) {
            const col_index = header.getAttribute("data-column-index")

            header.addEventListener("click", (e) => {
                sortTable(e, table, col_index)
            })
        }
    }
})