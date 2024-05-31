// window.onload = setListeners;

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

let selectorTo;

//Отправка выбранных функций и изменение контента
function addOptions(options) {
    values = [];
    options = Array.from(options);
    options.forEach(function (option) {
        values.push(option.value)
    });
    teacherElem = document.getElementById('teacherId');
    $.ajax({
        type: 'GET',
        url: '/teachers/getDataFromDB/',
        data: {
            selectedValues: values,
            teacherId: teacherElem ? teacherElem.value : null
        },
        success: function (response) {
            response['array'].forEach(function (elem) {
                discipline = elem.discipline;
                classes = elem.classes;
                selectedClasses = elem.selectedClassesId;

                var pElement = $('<p id="p-select-' + discipline.id + '" name="p-select-' + discipline.id + '">');
                var labelElement = $('<label for="select-' + discipline.id + '">' + discipline.str + '</label>');
                var selectElement = $('<select name="select-' + discipline.id + '" multiple id="id_select-' + discipline.id + '">');

                classes.forEach(function (classObj) {
                    var optionElement = $('<option value="' + classObj.id + '">' + classObj.str + '</option>');
                    if (selectedClasses.includes(classObj.id)) {
                        optionElement.attr('selected', 'selected');
                    }
                    selectElement.append(optionElement);
                });

                container = document.getElementById("form");

                pElement.append(labelElement);
                pElement.append(selectElement);

                // $('#form').append(pElement);
                $('#but2').parent().before(pElement);

                SelectFilter.init("id_select-" + discipline.id, "классы для " + discipline.str, 0, "/static/admin/");
                swapDivLabel(document.querySelector(`#p-select-${discipline.id} .selector`));
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

function swapDivLabel(divElement) {
    labelElement = divElement.nextElementSibling;
    divElement.parentNode.insertBefore(labelElement, divElement);
    labelElement.style.fontSize = "16px";
    labelElement.style.fontWeight = "bold";
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

// обработчик формы, отправляет дополнительные поля
function handleFormSubmit() {
    event.preventDefault(); // Предотвращение стандартного поведения отправки формы
    var selects = document.body.querySelectorAll('select[id^="id_select-"][id$="to"]');
    var selectOptions = [];

    selects.forEach(function (select) {
        selectOptions.push({
            'id_discipline': parseInt(select.id.match(/\d+/)[0]),
            'classes': Array.from(select.options).map(option => option.value)
        })
    });


    var formData = new FormData(document.querySelector('#form'));
    teacherElem = document.getElementById('teacherId');
    var data = {
        'teacher_id': teacherElem ? teacherElem.value : null,
        'array': selectOptions,
    };
    if (teacherElem) {
        sendData(data);
    } else {
        $.ajax({
            type: "POST",
            url: "/teachers/create/",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                data['teacher_id']=response;
                sendData(data);
            },
            error: function (xhr, status, error) {
                console.log(xhr.responseText);
            }
        });
        // var data = {
        //     'teacher_id': teacherElem ? teacherElem.value : null,
        //     'fio': document.getElementById('id_fio').value,
        //     'position': document.getElementById('id_position').value,
        //     'room': document.getElementById('id_room').value,
        //     'photo': document.getElementById('id_photo').files[0],
        //     'array': selectOptions,
        // };
        //
        // var xhr = new XMLHttpRequest();
        // xhr.open('POST', '/teachers/classes_field_form/', true);
        // xhr.setRequestHeader('Content-Type', 'application/json');

        // var teacherElem = document.getElementById('teacherId');
        // var fio = document.getElementById('id_fio').value;
        // var position = document.getElementById('id_position').value;
        // var room = document.getElementById('id_room').value;
        // var photoFile = document.getElementById('id_photo').files[0];
        //
        //
        // var formData = new FormData();
        // formData.append('teacher_id', teacherElem ? teacherElem.value : null);
        // formData.append('fio', fio);
        // formData.append('position', position);
        // formData.append('room', room);
        // formData.append('photo', photoFile);
        // formData.append('array', JSON.stringify(selectOptions));
        //
        // var xhr = new XMLHttpRequest();
        // xhr.open('POST', '/teachers/classes_field_form/', true);
        // xhr.send(formData);
        //
        // xhr.onreadystatechange = function () {
        //     if (xhr.readyState === 4) {
        //         if (xhr.status === 200) {
        //             // console.log('AJAX request successful');
        //         } else {
        //             console.error('AJAX request failed with status: ' + xhr.status);
        //         }
        //     }
        // };

        // xhr.send(JSON.stringify(data));
    }
}

function sendData(data) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/teachers/classes_field_form/', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(data));
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                // console.log('AJAX request successful');
                window.location.href = '/teachers';
            } else {
                console.error('AJAX request failed with status: ' + xhr.status);
            }
        }
    };
}
