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

// function handleMenuItemClick(this_item) {
//         const menuItems = document.querySelectorAll('.nav-link');
//         menuItems.forEach(item => {
//             item.classList.remove('active');
//             item.classList.remove('nav-item');
//             item.classList.add('link-body-emphasis');
//         });
//         this_item.classList.remove('link-body-emphasis');
//         this_item.classList.add('active');
//         this_item.classList.add('nav-item');
//     }
    // document.addEventListener('DOMContentLoaded', function () {
    //     const menuItems = document.querySelectorAll('.nav-link');
    //     let selectedMenuItem = localStorage.getItem('selectedMenuItem');
    //
    //     // Восстановление состояния выбранного элемента, если он сохранен в localStorage
    //     if (selectedMenuItem) {
    //         menuItems.forEach(item => {
    //             item.classList.remove('active');
    //             item.classList.remove('nav-item');
    //             item.classList.add('link-body-emphasis');
    //         });
    //         document.querySelector(selectedMenuItem).classList.add('active');
    //     }
    //
    //     // Обработчик клика по элементу меню
    //     menuItems.forEach(item => {
    //         item.addEventListener('click', function () {
    //             menuItems.forEach(item => {
    //                 item.classList.remove('active');
    //                 item.classList.remove('nav-item');
    //                 item.classList.add('link-body-emphasis');
    //             });
    //
    //             this.classList.add('active');
    //
    //             // Сохранение выбранного элемента в localStorage
    //             localStorage.setItem('selectedMenuItem', `#${this.id}`);
    //         });
    //     });
    // });