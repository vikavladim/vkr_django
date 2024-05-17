// function myFunction2(slug) {
//     var isValid = confirm('Are you sure?' + slug);
//     if (isValid) {
//         window.location.replace("{% url 'subject_delete' slug=form.instance.slug %}");
//         // window.location = "{% url 'subject_delete' slug=form.instance.slug %}";
//     } else {
//         alert("It won't delete. Yay!");
//     }
// }

// балуемся с хэдером
// window.onload = baseFunction;
//
// function adjustHeaderHeight() {
//     const contentHeight = header.scrollHeight;
//     const minHeight = parseInt(getComputedStyle(header).getPropertyValue('--top-height'));
//
//     header.style.minHeight = Math.max(contentHeight, minHeight) + 'px';
// }
//
// function checkHeaderOverflow() {
//     if (headerContent.scrollWidth > header.clientWidth) {
//         showMoreButton.style.display = 'inline-block';
//     } else {
//         showMoreButton.style.display = 'none';
//     }
// }
//
// function baseFunction() {
//     const header = document.querySelector('header');
//
//
// // Вызовите функцию при загрузке страницы и изменении размеров окна
//     window.addEventListener('load', adjustHeaderHeight);
//     window.addEventListener('resize', adjustHeaderHeight);
//
// //сворачивание хэдера
//     const headerContent = document.getElementById('headerContent');
//     const showMoreButton = document.getElementById('showMoreButton');
//
//
//     showMoreButton.addEventListener('click', function () {
//         header.classList.toggle('expanded');
//     });
//
//     window.addEventListener('resize', checkHeaderOverflow);
//     checkHeaderOverflow();
// }
// window.onload = baseFunction;
// // Функция для обновления верхнего отступа основного содержимого
// function updateMainMarginTop() {
//     const header = document.querySelector('header');
//     const headerHeight = header.offsetHeight;
//     const mainContent = document.querySelector('div.content');
//     mainContent.style.marginTop = headerHeight + 'px';
// }
// function baseFunction() {
//     window.addEventListener('load', updateMainMarginTop);
//     window.addEventListener('resize', updateMainMarginTop);
// }
