const observer = new MutationObserver((mutationsList, observer) => {
    mutationsList.forEach(mutation => {
        if (mutation.addedNodes && mutation.addedNodes.length > 0) {
            if (Array.from(mutation.addedNodes).some(node => node.id === 'id_discipline')) {
                setListeners();
            }
        }
    });
});

const config = {childList: true, subtree: true};
observer.observe(document, config);

function swapDivLabel(divElement) {
    labelElement = divElement.nextElementSibling;
    divElement.parentNode.insertBefore(labelElement, divElement);
    labelElement.style.fontSize = "16px";
    labelElement.style.fontWeight = "bold";
}


//Отправка выбранных функций и изменение контента
function addOptions(options) {
    values = [];
    options = Array.from(options);
    options.forEach(function (option) {
        values.push(option.value)
    });
    let program = document.getElementById('objectId');
    $.ajax({
        type: 'GET',
        url: '/programs/getHoursFromDB/',
        data: {
            selectedValues: values,
            programId: program ? program.value : null
        },
        success: function (response) {
            response['array'].forEach(function (elem) {
                discipline = elem.discipline;
                let load = elem.load;

                var pElement = $('<p id="p-select-' + discipline.id + '" name="p-select-' + discipline.id + '">');
                var labelElement = $('<label for="select-' + discipline.id + '">' + discipline.str + '</label>');

                var hoursInput = $('<input type="number" name="hours-week" id="id_hours-week' + discipline.id + '" value="' + load + '" min="1">');
                var hoursLabel = $('<label for="hours-week">Часов в неделю:</label>');

                pElement.append(labelElement);

                pElement.append(hoursLabel);
                pElement.append(hoursInput);

                $('#but2').parent().before(pElement);
            });
        },
        error: function (err) {
            console.error('Произошла ошибка при получении данных из базы данных', err);
        }
    });
}

function differenceMassive(arr1, arr2) {
    return arr1.filter(el => !arr2.some(el2 => el2.value === el.value));
}

// обработчик формы, отправляет дополнительные поля
function handleFormSubmit() {
    event.preventDefault(); // Предотвращение стандартного поведения отправки формы
    var paragraphs = document.body.querySelectorAll('p[id^="p-select-"]');
    var selectOptions = [];

    paragraphs.forEach(function (paragraph) {
        selectOptions.push({
            'id_discipline': parseInt(paragraph.id.match(/\d+/)[0]),
            'load': paragraph.querySelector('[id^="id_hours-week"]').value
        })
    });

    var data = {
        'id': document.getElementById('objectId').value,
        'digit': document.getElementById('id_digit').value,
        'program_name': document.getElementById('id_name').value,
        'array': selectOptions,
    };

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/programs/load_field_form/', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                // console.log('AJAX request successful');
            } else {
                console.error('AJAX request failed with status: ' + xhr.status);
            }
        }
    };

    xhr.send(JSON.stringify(data));
    window.location.href = '/programs';
}

function handleSelectTo() {
    newOptions = selectorTo.querySelectorAll('option');
    newOptions = Array.from(newOptions);

    const addedOptions = differenceMassive(newOptions, oldOptions);
    const removedOptions = differenceMassive(oldOptions, newOptions);

    addOptions(addedOptions);
    removedOptions.forEach(option => {
        document.getElementById("p-select-" + option.value).remove();
    });

    oldOptions = newOptions;
}

// Основная функция программы
function setListeners() {
    SelectFilter.init("id_discipline", "предметы", 0, "/static/admin/");
    swapDivLabel(document.querySelector('div.selector'));

    selectorTo = document.querySelector('#id_discipline_to');

    oldOptions = selectorTo.querySelectorAll('option');
    oldOptions = Array.from(oldOptions);

    const observerTo = new MutationObserver(handleSelectTo);
    observerTo.observe(selectorTo, {childList: true});

    document.querySelectorAll('#id_discipline_to')
        .forEach(elem => addOptions(elem));
}