function updateRow(num, rank, username, code, score) {
    var row_text = "row";
    let row_to_update = row_text.concat(num);
    var row = document.getElementById(row_to_update);
    row.cells[0].innerHTML = rank;
    row.cells[1].innerHTML = username;
    row.cells[2].innerHTML = code;
    row.cells[3].innerHTML = score;
}
