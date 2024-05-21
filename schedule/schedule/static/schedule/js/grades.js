const observer = new MutationObserver((mutationsList, observer) => {
    mutationsList.forEach(mutation => {
        if (mutation.addedNodes && mutation.addedNodes.length > 0) {
            if (Array.from(mutation.addedNodes).some(node => node.id === 'id_subject')) {
                    SelectFilter.init("id_subject", "предметы", 0, "/static/admin/");
                    swapDivLabel(document.querySelector('div.selector'));
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