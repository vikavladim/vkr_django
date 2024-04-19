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

// Найти все элементы списка и добавить обработчик события для каждого элемента
// var listItems = document.querySelectorAll('#yourListId li');
// listItems.forEach(function(item) {
//     item.addEventListener('click', handleListItemClick);
// });
// window.onload = function () {
//     window.document.body.onload = doThis; // note removed parentheses
// };


const targetElement = document.getElementById('id_subject_to');

const observer = new MutationObserver((mutationsList, observer) => {
    mutationsList.forEach(mutation => {
        if (mutation.addedNodes && mutation.addedNodes.length > 0) {
            if (Array.from(mutation.addedNodes).some(node => node.id === 'id_subject_to')) {
                console.log('Элемент с id "id_subject_to" появился на странице!');
            setListeners();
            }
        }
    });
});

// Настройка конфигурации MutationObserver
const config = { childList: true, subtree: true };

// Начинаем наблюдение за целевым элементом с заданной конфигурацией
observer.observe(document, config);




// setTimeout(setListeners, 200);

function handleListItemClick(event) {
    console.log("Мы зашли в обработчик")
    // var selectedOptions = Array.from(event.target.selectedOptions).map(option => option.value);
    // // Вы можете выполнить действия с выбранными вариантами, например, отправить их на сервер
    // console.log('Выбранные варианты:', selectedOptions);
    //
    // $.ajax({
    //     type: 'GET',
    //     url: '/teachers/getDataFromDB/',
    //     data: {
    //         selectedValue: selectedOptions,
    //     },
    //     success: function (response) {
    //         console.log('Данные из базы данных:', response);
    //     },
    //     error: function (err) {
    //         console.error('Произошла ошибка при получении данных из базы данных');
    //     }
    // });
}

function setListeners() {
    const selectorTo = document.querySelector('#id_subject_to');

    oldOptions = selectorTo.querySelectorAll('option');
    oldOptions = Array.from(oldOptions);

    function handleSelectTo(mutationsList, observer) {
        newOptions = selectorTo.querySelectorAll('option');
        newOptions = Array.from(newOptions);

        const addedOptions = [];
        const removedOptions = [];

        // const addedOptions = newOptions.filter(el_A => !oldOptions.includes(el_A));
        newOptions.forEach(el_A => {
            if (!oldOptions.some(el_B => el_B.value === el_A.value)) {
                addedOptions.push(el_A);
            }
        });

        oldOptions.forEach(el_A => {
            if (!newOptions.some(el_B => el_B.value === el_A.value)) {
                removedOptions.push(el_A);
            }
        })
        if (addedOptions.length > 0) {
            console.log('addedOptions', addedOptions);
        }
        if (removedOptions.length > 0) {
            console.log('removedOptions', removedOptions);
        }
        oldOptions = newOptions;
    }

    const observerTo = new MutationObserver(handleSelectTo);
    observerTo.observe(selectorTo, {childList: true});
}



