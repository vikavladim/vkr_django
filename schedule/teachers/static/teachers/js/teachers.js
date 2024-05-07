// Ожидание появления списка предметов на странице
const observer = new MutationObserver((mutationsList, observer) => {
    mutationsList.forEach(mutation => {
        if (mutation.addedNodes && mutation.addedNodes.length > 0) {
            if (Array.from(mutation.addedNodes).some(node => node.id === 'id_subject_to')) {
                setListeners();
            }
        }
    });
});

const config = {childList: true, subtree: true};
observer.observe(document, config);

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
            teacherId: document.getElementById('teacherId').value
        },
        success: function (response) {
            response['array'].forEach(function (elem) {
                subject = elem.subject;
                classes = elem.classes;
                selectedClasses = elem.selectedClassesId;

                var pElement = $('<p id="p-select-' + subject.id + '" name="p-select-' + subject.id + '">');
                var labelElement = $('<label for="select-' + subject.id + '">' + subject.id + '</label>');
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

                $('#form').append(pElement);
                SelectFilter.init("id_select-" + subject.id, "классы для "+subject.str, 0, "/static/admin/");
            });
        },
        error: function (err) {
            console.error('Произошла ошибка при получении данных из базы данных');
        }
    });
}


// Основная функция программы
function setListeners() {
    const selectorTo = document.querySelector('#id_subject_to');

    oldOptions = selectorTo.querySelectorAll('option');
    oldOptions = Array.from(oldOptions);

    // Обработчик выбора предметов в списке
    function handleSelectTo(mutationsList, observer) {
        newOptions = selectorTo.querySelectorAll('option');
        newOptions = Array.from(newOptions);

        const addedOptions = [];
        const removedOptions = [];

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
            addOptions(addedOptions);
        }
        if (removedOptions.length > 0) {
            removedOptions.forEach(option => {
                document.getElementById("p-select-" + option.value).remove();
            });
        }
        oldOptions = newOptions;
    }

    const observerTo = new MutationObserver(handleSelectTo);
    observerTo.observe(selectorTo, {childList: true});

    document.querySelectorAll('#id_subject_to').forEach(function (selectorTo) {
        addOptions(selectorTo);
    });
}

// обработчик формы, отправляет дополнительные поля
function handleFormSubmit(event) {
    // event.preventDefault(); // Предотвращение стандартного поведения отправки формы
    var selects = document.body.querySelectorAll('select[id^="id_select-"][id$="to"]');
    var selectOptions = [];

    selects.forEach(function (select) {
        var options = Array.from(select.options).map(function (option) {
            return option.value;
        });

        selectOptions.push({
            'id_subject': parseInt(select.id.match(/\d+/)[0]),
            'classes': options
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
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log('AJAX request successful');
        }
    };

    xhr.send(JSON.stringify(data));
}
