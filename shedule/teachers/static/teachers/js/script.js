// window.onload = function() {
//     console.log(document)
// var table = document.getElementById('t1')
// var tbody = table.getElementsByTagName('tbody')[0];
// var rows = table.getElementsByTagName('tr');
//
// for (var i = 0; i < rows.length; i++) {
//     var cells = rows[i].getElementsByTagName('td');
//     for (var j = 0; j < cells.length; j++) {
//         cells[j].setAttribute('contenteditable', true);
//     }
// }
// }

function deleteRow(btn) {
  var row = btn.parentNode.parentNode; // Получаем родительскую строку
  row.parentNode.removeChild(row); // Удаляем строку из таблицы
}