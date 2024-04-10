function addSubject() {
    const selectedSubjects = document.getElementById("selected-subjects");
    const newSubject = document.createElement("div");
    // const selectedSubject = document.getElementById("subjects").value;
    const subjectsDropdown = document.getElementById("subjects");

    newSubject.innerHTML = `
        <span>${subjectsDropdown.value}</span>
        <button class="remove-subject" onclick="this.parentNode.remove()">Удалить</button>
    `;
    selectedSubjects.appendChild(newSubject);
    subjectsDropdown.remove(subjectsDropdown.selectedIndex);
}
