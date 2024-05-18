// function addSubject() {
//     const selectedSubjects = document.getElementById("selected-subjects");
//     const newSubject = document.createElement("div");
//     // const selectedSubject = document.getElementById("subjects").value;
//     const subjectsDropdown = document.getElementById("subjects");
//
//     newSubject.innerHTML = `
//         <span>${subjectsDropdown.value}</span>
//         <button class="remove-subject" onclick="this.parentNode.remove()">Удалить</button>
//     `;
//     selectedSubjects.appendChild(newSubject);
//     subjectsDropdown.remove(subjectsDropdown.selectedIndex);
// }

window.onload = baseFunction;
// Функция для обновления верхнего отступа основного содержимого
function updateMainMarginTop() {
    const header = document.querySelector('header');
    const headerHeight = header.offsetHeight;
    const mainContent = document.querySelector('section.section');
    mainContent.style.marginTop = headerHeight + 'px';
}
function baseFunction() {
    updateMainMarginTop();
    window.addEventListener('load', updateMainMarginTop);
    window.addEventListener('resize', updateMainMarginTop);
}
