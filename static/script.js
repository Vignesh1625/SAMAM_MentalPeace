function editQuestion(buttonElement, questionId, tableId) {
    var row = buttonElement.closest('tr');
    var questionElement = row.querySelector('td:nth-child(2)');
    var questionText = questionElement.textContent;

    var inputElement = document.createElement('input');
    inputElement.type = 'text';
    inputElement.value = questionText;

    questionElement.textContent = '';
    questionElement.appendChild(inputElement);

    var saveButton = document.createElement('button');
    saveButton.textContent = 'Save';

    saveButton.addEventListener('click', function () {
        var newQuestionText = inputElement.value;
        questionElement.textContent = newQuestionText;
        //questionElement.removeChild(inputElement);
        fetch(`/edit_question/${questionId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ questionText: newQuestionText, tableId: tableId }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.message)
                console.log(data.message)
            else if (data.error)
                console.error(data.error);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
        saveButton.innerHTML = 'Edit';
    });
    buttonElement.parentNode.replaceChild(saveButton, buttonElement);
    
}
