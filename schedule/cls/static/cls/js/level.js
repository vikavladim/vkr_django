const observer = new MutationObserver((mutationsList, observer) => {
    mutationsList.forEach(mutation => {
        if (mutation.addedNodes && mutation.addedNodes.length > 0) {
            if (Array.from(mutation.addedNodes).some(node => node.id === 'id_subject')) {
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
    $.ajax({
        type: 'GET',
        url: '/grades/getHoursFromDB/',
        data: {
            selectedValues: values,
            gradeId: document.getElementById('gradeId').value
        },
        success: function (response) {
            response['array'].forEach(function (elem) {
                subject = elem.subject;
                let load = elem.load ? elem.load : 1;

                var pElement = $('<p id="p-select-' + subject.id + '" name="p-select-' + subject.id + '">');
                var labelElement = $('<label for="select-' + subject.id + '">' + subject.str + '</label>');
                // var selectElement = $('<select name="select-' + subject.id + '" id="id_select-' + subject.id + '">');
                // selectElement.append($('<option value="0">Не выбрано</option>'));

                // teachers.forEach(function (teacher) {
                //     var optionElement = $('<option value="' + teacher.id + '">' + teacher.str + '</option>');
                //     if (teacher.id === selectedTeacherId) {
                //         optionElement.attr('selected', 'selected');
                //     }
                //     selectElement.append(optionElement);
                // });

                var hoursInput = $('<input type="number" name="hours-week" id="id_hours-week' + subject.id + '" value="' + load + '" min="1">');
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

// обработчик формы, отправляет дополнительные поля
function handleFormSubmit() {
    // event.preventDefault(); // Предотвращение стандартного поведения отправки формы
    var paragraphs = document.body.querySelectorAll('p[id^="p-select-"]');
    var selectOptions = [];

    paragraphs.forEach(function (paragraph) {
        var selectElement = paragraph.querySelector('select');
        var selectedTeacher = selectElement.options[selectElement.selectedIndex].value;

        selectOptions.push({
            'id_subject': parseInt(paragraph.id.match(/\d+/)[0]),
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

// Основная функция программы
function setListeners() {
    SelectFilter.init("id_subject", "предметы", 0, "/static/admin/");
    swapDivLabel(document.querySelector('div.selector'));

    selectorTo = document.querySelector('#id_subject_to');

    oldOptions = selectorTo.querySelectorAll('option');
    oldOptions = Array.from(oldOptions);

    const observerTo = new MutationObserver(handleSelectTo);
    observerTo.observe(selectorTo, {childList: true});

    document.querySelectorAll('#id_subject_to')
        .forEach(elem => addOptions(elem));
}