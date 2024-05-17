function myFunction2(slug) {
    var isValid = confirm('Are you sure?'+slug);
    if (isValid) {
        window.location.replace("{% url 'subject_delete' slug=form.instance.slug %}");
        // window.location = "{% url 'subject_delete' slug=form.instance.slug %}";
    } else {
        alert("It won't delete. Yay!");
    }
}
// балуемся с хэдером
const header = document.querySelector('header');

function adjustHeaderHeight() {
    const contentHeight = header.scrollHeight;
    const minHeight = parseInt(getComputedStyle(header).getPropertyValue('--top-height'));

    header.style.minHeight = Math.max(contentHeight, minHeight) + 'px';
}

// Вызовите функцию при загрузке страницы и изменении размеров окна
window.addEventListener('load', adjustHeaderHeight);
window.addEventListener('resize', adjustHeaderHeight);