// Ожидание появление списка предметов на странице
const targetElement = document.getElementById('id_subject_to');

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
    $.ajax({
        type: 'GET',
        url: '/teachers/getDataFromDB/',
        data: {
            selectedValue: options[0].value,
        },
        success: function (response) {
            // console.log(response);
            response['array'].forEach(function (elem) {
                subject = elem.subject;
                classes = elem.classes;

                var pElement = $('<p id="p-select-' + subject.id + '">');
                var labelElement = $('<label for="select-' + subject.id + '">' + subject.str + '</label>');
                var selectElement = $('<select name="select-' + subject.id + '" multiple id="id_select-' + subject.id + '">');

                classes.forEach(function (classObj) {
                    var optionElement = $('<option value="' + classObj.id + '">' + classObj.str + '</option>');
                    selectElement.append(optionElement);
                });

                container = document.getElementById("form");

                pElement.append(labelElement);
                pElement.append(selectElement);

                $('#form').append(pElement);
                SelectFilter.init("id_select-" + subject.id, "select-" + subject.id, 0, "/static/admin/");
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



