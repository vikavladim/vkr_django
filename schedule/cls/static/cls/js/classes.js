// window.onload = setListeners;

const observer = new MutationObserver((mutationsList, observer) => {
    mutationsList.forEach(mutation => {
        if (mutation.addedNodes && mutation.addedNodes.length > 0) {
            if (Array.from(mutation.addedNodes).some(node => node.id === 'id_discipline')) {
                setListeners();
                 observer.disconnect();
            }
        }
    });
});

const config = {childList: true, subtree: true};
observer.observe(document, config);

let selectorTo;
let pSelector;
let programIdElem;
let disciplineSelect;
let lastState = true;
let newState = true;

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
    classElem=document.getElementById('classId');
    digitElem=document.getElementById('id_digit');
    $.ajax({
        type: 'GET',
        url: '/classes/getTeachersFromDB/',
        data: {
            selectedValues: values,
            classId: classElem? classElem.value : null,
            programId: programIdElem.value,
            cls_digit: digitElem? digitElem.value : null,
        },
        success: function (response) {
            response['array'].forEach(function (elem) {
                discipline = elem.discipline;
                teachers = elem.teachers;
                selectedTeacherId = elem.selectedTeacherId;
                let load = elem.load;

                var pElement = $('<p id="p-select-' + discipline.id + '" name="p-select-' + discipline.id + '">');
                var labelElement = $('<label for="select-' + discipline.id + '">' + discipline.str + '</label>');
                var selectElement = $('<select name="select-' + discipline.id + '" id="id_select-' + discipline.id + '">');
                selectElement.append($('<option value="0">Не выбрано</option>'));

                teachers.forEach(function (teacher) {
                    var optionElement = $('<option value="' + teacher.id + '">' + teacher.str + '</option>');
                    if (teacher.id === selectedTeacherId) {
                        optionElement.attr('selected', 'selected');
                    }
                    selectElement.append(optionElement);
                });

                var hoursInput = $('<input type="number" name="hours-week" id="id_hours-week' + discipline.id + '" value="' + load + '" min="1">');
                var hoursLabel = $('<label for="hours-week">Часов в неделю:</label>');

                pElement.append(labelElement);
                pElement.append(selectElement);

                pElement.append(hoursLabel);
                pElement.append(hoursInput);

                // $('#form').append(pElement);
                $('#but2').before(pElement);
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

// Обработчик выбора предметов в списке
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
    pSelector = document.querySelector('div.selector').parentNode;

    programIdElem = document.querySelector('#id_program');
    programIdElem.addEventListener('change', changeProgram);
    disciplineSelect = document.querySelector('div.selector');

    oldOptions = selectorTo.querySelectorAll('option');
    oldOptions = Array.from(oldOptions);

    const observerTo = new MutationObserver(handleSelectTo);
    observerTo.observe(selectorTo, {childList: true});

    document.querySelectorAll('#id_discipline_to')
        .forEach(elem => addOptions(elem));
}

//обработчик выбора программы
function changeProgram() {
    lastState = newState;
    newState = programIdElem.value === 0;
    if (!newState) {
        changeDisciplines();
        // setListeners();
        //     SelectFilter.init("id_discipline", "предметы", 0, "/static/admin/");

    }
    if (lastState === true && newState === false) {
        changeAllChildren(disciplineSelect, false);
    } else if (lastState === false && newState === true) {
        changeAllChildren(disciplineSelect, true);
    }
}

function changeAllChildren(element, state) {
    element.childNodes.forEach(function (child) {
        if (child.nodeType === Node.ELEMENT_NODE) {
            // if (child.tagName.toLowerCase() === 'a') {
            if (state) {
                child.classList.remove('disabled-link');
            } else {
                child.classList.add('disabled-link');
            }
            // }
        }
        changeAllChildren(child, state);
    });
}

// изменение дисциплин и нагрузки по программам
function changeDisciplines() {
    fetch('/classes/change_disciplines/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ program_id: document.getElementById('id_program').value })
})
.then(response => {
    if (response.ok) {
        return response.json();
    }
    throw new Error('Network response was not ok.');
})
.then(data => {
    var allDisciplines = data.all_disciplines;
    var selectDisciplinesIds = data.select_disciplines_ids;

    pSelector.querySelector('div.selector').remove();

    var selectElement = document.createElement('select');
    selectElement.id = 'id_discipline';
    selectElement.name = 'discipline';
    selectElement.multiple = true;
    selectElement.classList.add('filtered');

    pSelector.appendChild(selectElement);

    allDisciplines.forEach(function (discipline) {
        var option = document.createElement('option');
        option.value = discipline.id;
        option.text = discipline.name;
        if (selectDisciplinesIds.includes(discipline.id)) {
            option.selected = true;
        }
        selectElement.appendChild(option);
    });

    SelectFilter.init("id_discipline", "предметы", 0, "/static/admin/");
})
.catch(error => {
    console.error('Ошибка при выполнении запроса:', error);
});
}


// обработчик формы, отправляет дополнительные поля
function handleFormSubmit() {
    // event.preventDefault(); // Предотвращение стандартного поведения отправки формы
    var paragraphs = document.body.querySelectorAll('p[id^="p-select-"]');
    var selectOptions = [];

    paragraphs.forEach(function (paragraph) {
        var selectElement = paragraph.querySelector('select');
        var selectedTeacher = selectElement.options[selectElement.selectedIndex].value;

        selectOptions.push({
            'id_discipline': parseInt(paragraph.id.match(/\d+/)[0]),
            'teacher': selectedTeacher === "0" ? null : selectedTeacher,
            'hours_week': paragraph.querySelector('[id^="id_hours-week"]').value
        })
    });

    var data = {
        'class_id': document.getElementById('classId').value,
        'array': selectOptions,
    };

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/classes/teachers_field_form/', true);
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
}
