//
// function createLists() {
//     var selectedValue = $('#firstList').val();
//     // Отправить запрос на сервер для получения отфильтрованных значений на основе selectedValue
//     $.get('/getFilteredValues', { selectedValue: selectedValue }, function(filteredValues) {
//         // Очистить второй список
//         $('#secondList').empty();
//         // Добавить отфильтрованные значения во второй список
//         $.each(filteredValues, function(index, value) {
//             $('#secondList').append($('<option>').text(value).attr('value', value));
//         });
//     });
// }
//
// function updateSecondList() {
//     var selectedValue = $('#firstList').val();
//     // Отправить запрос на сервер для получения отфильтрованных значений на основе selectedValue
//     $.get('/getFilteredValues', { selectedValue: selectedValue }, function(filteredValues) {
//         // Очистить второй список
//         $('#secondList').empty();
//         // Добавить отфильтрованные значения во второй список
//         $.each(filteredValues, function(index, value) {
//             $('#secondList').append($('<option>').text(value).attr('value', value));
//         });
//     });
// }

// Обработчик события для нажатия на элемент списка
// function handleListItemClick(event) {
//     var selectedValue = event.target.textContent;
//
//     // Отправка запроса на сервер с использованием AJAX
//     $.ajax({
//         type: 'POST',
//         url: '/getDataFromDB', // URL для обработки запроса на сервере
//         data: { selectedValue: selectedValue }, // Данные для отправки на сервер
//         success: function(response) {
//             console.log('Данные из базы данных:', response);
//         },
//         error: function(err) {
//             console.error('Произошла ошибка при получении данных из базы данных');
//         }
//     });
// }
//
// // Найти все элементы списка и добавить обработчик события для каждого элемента
// var listItems = document.querySelectorAll('#yourListId li');
// listItems.forEach(function(item) {
//     item.addEventListener('click', handleListItemClick);
// });