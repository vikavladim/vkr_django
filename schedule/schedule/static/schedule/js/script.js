function addSubject() {
    const selectedSubjects = document.getElementById("selected-subjects");
    const newSubject = document.createElement("div");
    const selectedSubject = document.getElementById("subjects").value;

    newSubject.innerHTML = `
        <span>${selectedSubject}</span>
        <button class="remove-subject" onclick="this.parentNode.remove()">Удалить</button>
    `;
    selectedSubjects.appendChild(newSubject);
}
