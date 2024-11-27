/**
 * Filter table rows based on input value.
 * @param {Event} event - Input event
 * @param {string} tableId - ID of the table
 */
function filterTable(event, tableId) {
    const filter = event.target.value.toLowerCase();
    const table = document.getElementById(tableId);
    const rows = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');

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
 * @param {string} tableId - ID of the table
 * @param {number} colIndex - Index of the column to sort by
 */
function sortTable(event, tableId, colIndex) {
    const table = document.getElementById(tableId);
    const tbody = table.getElementsByTagName('tbody')[0];
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

    // Update sort direction
    event.target.dataset.ascending = ascending;
}

/**
 * Access item page.
 * @param {Event} event - Click event
 * @param {string} goTo - URL of the client
 */
function accessTableItem(event, goTo) {
    event.preventDefault();
    console.log(goTo)
    window.location.replace(goTo);
}