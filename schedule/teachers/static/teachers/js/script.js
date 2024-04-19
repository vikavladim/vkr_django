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


setTimeout(setListeners, 200);

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
    // elements = document.querySelectorAll('#id_subject_from, #id_subject_to');
    // // elements = elements.concat(Array.from(document.querySelectorAll('#id_subject_to')));
    // console.log('вот такие элементы во фроме', elements);
    // elements.forEach(function (item) {
    //     item.addEventListener('change', handleListItemClick);
    // });

    const selectorTo = document.querySelector('#id_subject_to');

    // function handleSelectChanges(mutationsList, observer) {
    //     // const addedNodes = [];
    //     // const removedNodes = [];
    //
    //
    //     mutationsList.forEach(function (mutation) {
    //         console.log("мы зашли")
    //         //
    //         // const addedOptions = addedNodes.filter(el_A => !removedNodes.includes(el_A));
    //         // const removedOptions = removedNodes.filter(el_A => !addedNodes.includes(el_A));
    //         //
    //         // console.log('addedOptions', addedOptions);
    //         // console.log('removedOptions', removedOptions);
    //         if (mutation.type === 'childList') {
    //             mutation.removedNodes.forEach(function (node) {
    //                 if (node.tagName === 'OPTION') {
    //                     console.log('Удалена опция:', node);
    //                     // options.pop(node)
    //                 }
    //             });
    //
    //             mutation.addedNodes.forEach(function (node) {
    //                 if (node.tagName === 'OPTION') {
    //                     console.log('Добавлена новая опция:', node);
    //                     // options.push(node)
    //                 }
    //
    //             });
    //         }
    //     });
    // }

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
