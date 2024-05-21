// window.onload = setListeners;

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

let selectorTo;

//Отправка выбранных функций и изменение контента
function addOptions(options) {
    values = [];
    options = Array.from(options);
    options.forEach(function (option) {
        values.push(option.value)
    });
    $.ajax({
        type: 'GET',
        url: '/teachers/getDataFromDB/',
        data: {
            selectedValues: values,
            teacherId: document.getElementById('teacherId') ? document.getElementById('teacherId').value : null
        },
        success: function (response) {
            response['array'].forEach(function (elem) {
                subject = elem.subject;
                classes = elem.classes;
                selectedClasses = elem.selectedClassesId;

                var pElement = $('<p id="p-select-' + subject.id + '" name="p-select-' + subject.id + '">');
                var labelElement = $('<label for="select-' + subject.id + '">' + subject.str + '</label>');
                var selectElement = $('<select name="select-' + subject.id + '" multiple id="id_select-' + subject.id + '">');

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
                $('#but2').before(pElement);

                SelectFilter.init("id_select-" + subject.id, "классы для " + subject.str, 0, "/static/admin/");
                swapDivLabel(document.querySelector(`#p-select-${subject.id} .selector`));
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

// обработчик формы, отправляет дополнительные поля
function handleFormSubmit() {
    // event.preventDefault(); // Предотвращение стандартного поведения отправки формы
    var selects = document.body.querySelectorAll('select[id^="id_select-"][id$="to"]');
    var selectOptions = [];

    selects.forEach(function (select) {
        selectOptions.push({
            'id_subject': parseInt(select.id.match(/\d+/)[0]),
            'classes': Array.from(select.options).map(option => option.value)
        })
    });

    var data = {
        'teacher_id': document.getElementById('teacherId').value,
        'array': selectOptions,
    };

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/teachers/classes_field_form/', true);
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
