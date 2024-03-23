$(document).ready(function() {
    var table = $('#logsTable').DataTable();

    // Gebruik de externe #searchInput om de tabel te filteren.
    $('#searchInput').on('keyup', function() {
        table.search(this.value).draw();
    });
});
