function addNewQuestion() {
  const newQuestionId = document.getElementById('newQuestionId').value;
  const newQuestionText = document.getElementById('newQuestionText').value;

  fetch('/add_question', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({
          id: newQuestionId,
          question: newQuestionText,
      }),
  })
  .then(response => response.json())
  .then(data => {
      if (data.success) {
          // Update the table with the new question
          updateQuestionsTable(newQuestionId, newQuestionText);

          // Clear input fields
          document.getElementById('newQuestionId').value = '';
          document.getElementById('newQuestionText').value = '';
      } else if (data.error) {
          console.error("Error:", data.error);  // Log server error
      }
  })
  .catch((error) => {
      console.error('Error:', error);  // Log fetch error
  });
}

function updateQuestionsTable(id, question) {
  const tbody = document.querySelector('#CharacterQuestionsTable > tbody');
  const newRow = tbody.insertRow(tbody.rows.length-1); 
  newRow.innerHTML = `
      <td>${id}</td>
      <td>${question}</td>
      <td><button type="button" onclick="deleteQuestion(this, '${id}')">Delete</button></td>
  `;
}


function addNewDisQuestion() {
  const newQuestionId = document.getElementById('newDisQuestionId').value;
  const newQuestionText = document.getElementById('newDisQuestionText').value;

  fetch('/add_Disquestions', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({
          id: newQuestionId,
          question: newQuestionText,
      }),
  })
  .then(response => response.json())
  .then(data => {
      if (data.success) {
          // Update the table with the new question
          updateQuestionsTable(newQuestionId, newQuestionText);

          // Clear input fields
          document.getElementById('newDisQuestionId').value = '';
          document.getElementById('newDisQuestionText').value = '';
      } else if (data.error) {
          console.error("Error:", data.error);  // Log server error
      }
  })
  .catch((error) => {
      console.error('Error:', error);  // Log fetch error
  });
}

function updateQuestionsTable(id, question) {
  const tbody = document.querySelector('#DisorderQuestionsTable > tbody');
  const newRow = tbody.insertRow(tbody.rows.length-1); 
  newRow.innerHTML = `
      <td>${id}</td>
      <td>${question}</td>
      <td><button type="button" onclick="deleteQuestion(this, '${id}')">Delete</button></td>
  `;
}


// Helper function to append a new row to the table
function addNewRowToTable(question) {
  const tbody = document.querySelector('#questionsTable tbody');
  const newRow = tbody.insertRow(tbody.rows.length-1);
  newRow.innerHTML = `
    <td>${question.id}</td>
    <td>${question.question}</td>
    <td><button type="button" onclick="deleteQuestion(this, '${question.id}')">Delete</button></td>
  `;
}



// Function to delete a question
function deleteQuestion(buttonElement, questionId) {
    fetch(`/delete_question/${questionId}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            var row = buttonElement.closest('tr');
            row.remove();
        } else if (data.error) {
            console.error(data.error);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function deleteDisQuestion(buttonElement, questionId) {
  fetch(`/deleteDis_question/${questionId}`, {
      method: 'DELETE',
  })
  .then(response => response.json())
  .then(data => {
      if (data.message) {
          var row = buttonElement.closest('tr');
          row.remove();
      } else if (data.error) {
          console.error(data.error);
      }
  })
  .catch((error) => {
      console.error('Error:', error);
  });
}


function deleteRow(buttonElement, userId) {
    fetch(`/delete_user/${userId}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            var row = buttonElement.closest('tr');
            row.remove();
        } else if (data.error) {
            console.error(data.error);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

