document.getElementById('uploadForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const formData = new FormData();
  const fileInput = document.getElementById('fileInput');
  
  if (!fileInput.files[0]) {
    alert('Please select a file to upload');
    return;
  }
  
  formData.append('file', fileInput.files[0]);
  
  // Show loading state
  const uploadButton = document.querySelector('#uploadForm button[type="submit"]');
  const originalText = uploadButton.textContent;
  uploadButton.textContent = 'Uploading...';
  uploadButton.disabled = true;
  
  try {
    const response = await fetch('/api/documents/upload/', {
      method: 'POST',
      body: formData
    });
    
    const data = await response.json();
    
    if (response.ok) {
      displayResults(data);
      loadDocuments();
      fileInput.value = '';
    } else {
      alert('Upload failed: ' + (data.error || 'Unknown error'));
    }
  } catch (error) {
    console.error('Upload error:', error);
    alert('Upload error: ' + error.message);
  } finally {
    uploadButton.textContent = originalText;
    uploadButton.disabled = false;
  }
});

async function loadDocuments() {
  try {
    const response = await fetch('/api/documents/');
    const documents = await response.json();
    
    const documentList = document.getElementById('documentList');
    documentList.innerHTML = '';
    
    documents.forEach(doc => {
      const div = document.createElement('div');
      div.className = 'document-item';
      div.innerHTML = `
        <span>${doc.title}</span>
        <button onclick="deleteDocument(${doc.id})">Delete</button>
      `;
      documentList.appendChild(div);
    });
  } catch (error) {
    console.error('Load documents error:', error);
  }
}

async function deleteDocument(id) {
  try {
    await fetch(`/api/documents/${id}/`, {
      method: 'DELETE'
    });
    loadDocuments();
  } catch (error) {
    console.error('Delete error:', error);
  }
}

function displayResults(data) {
  let resultsDiv = document.getElementById('analysisResults');
  if (!resultsDiv) {
    resultsDiv = document.createElement('div');
    resultsDiv.id = 'analysisResults';
    resultsDiv.className = 'analysis-results';
    // Insert after the upload form
    const form = document.getElementById('uploadForm');
    form.parentNode.insertBefore(resultsDiv, form.nextSibling);
  }
  
  // Store quiz data for later
  window.currentQuizData = data.quiz;
  
  // Format summary with better styling (preserve formatting)
  const formattedSummary = data.summary.replace(/\n/g, '<br>');
  
  resultsDiv.innerHTML = `
    <div class="result-section summary-section">
      <h3>📚 Document Analysis</h3>
      <div class="summary-content">${formattedSummary}</div>
      <button class="next-btn" onclick="showQuiz(); return false;">Next: Take Quiz ➡️</button>
    </div>
    <div class="result-section quiz-section" id="quizSection" style="display: none;">
      <h3>📝 Interactive Quiz</h3>
      <div id="quizContent"></div>
    </div>
    <div class="result-info">
      <small>Extracted ${data.extracted_text_length} characters | Provider: ${data.ai_provider}</small>
    </div>
  `;
  resultsDiv.style.display = 'block';
}

function showQuiz() {
  const quizSection = document.getElementById('quizSection');
  const summarySection = document.querySelector('.summary-section');
  const quizContent = document.getElementById('quizContent');
  
  // Hide summary and show quiz
  summarySection.style.display = 'none';
  quizSection.style.display = 'block';
  
  // Smooth scroll to quiz section
  quizSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
  
  // Generate quiz HTML
  const data = { quiz: window.currentQuizData };
  let quizHTML = '';
  
  // Check if quiz is an array (JSON format) or string
  if (Array.isArray(data.quiz)) {
    quizHTML = '<form id="quizForm">';
    data.quiz.forEach((q, index) => {
      quizHTML += `
        <div class="quiz-question">
          <h4>${index + 1}. ${q.question}</h4>
          <div class="quiz-options">
            ${q.options.map((option, optIndex) => `
              <label class="quiz-option">
                <input type="radio" name="question${index}" value="${option}" data-correct="${q.correct}">
                <span>${option}</span>
              </label>
            `).join('')}
          </div>
        </div>
      `;
    });
    quizHTML += '<button type="button" class="submit-quiz" onclick="checkAnswers()">Submit Answers</button>';
    quizHTML += '<button type="button" class="back-btn" onclick="backToSummary(); return false;">← Back to Summary</button>';
    quizHTML += '</form>';
    quizHTML += '<div id="quizResults"></div>';
  } else {
    // Fallback for string format
    quizHTML = `<pre>${data.quiz}</pre>`;
    quizHTML += '<button type="button" class="back-btn" onclick="backToSummary(); return false;">← Back to Summary</button>';
  }
  
  quizContent.innerHTML = quizHTML;
}

function backToSummary() {
  const quizSection = document.getElementById('quizSection');
  const summarySection = document.querySelector('.summary-section');
  
  quizSection.style.display = 'none';
  summarySection.style.display = 'block';
  
  // Smooth scroll to summary section
  summarySection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function checkAnswers() {
  const form = document.getElementById('quizForm');
  const questions = form.querySelectorAll('.quiz-question');
  let score = 0;
  let total = questions.length;
  
  questions.forEach((questionDiv, index) => {
    const selectedRadio = form.querySelector(`input[name="question${index}"]:checked`);
    const allOptions = questionDiv.querySelectorAll('.quiz-option');
    
    if (selectedRadio) {
      const userAnswer = selectedRadio.value;
      const correctAnswer = selectedRadio.dataset.correct;
      
      allOptions.forEach(label => {
        const radio = label.querySelector('input');
        label.classList.remove('correct', 'incorrect');
        
        if (radio.value === correctAnswer) {
          label.classList.add('correct');
        }
        
        if (radio.checked && radio.value !== correctAnswer) {
          label.classList.add('incorrect');
        }
      });
      
      if (userAnswer === correctAnswer) {
        score++;
      }
    }
  });
  
  const resultsDiv = document.getElementById('quizResults');
  const percentage = Math.round((score / total) * 100);
  resultsDiv.innerHTML = `
    <div class="quiz-score ${percentage >= 60 ? 'pass' : 'fail'}">
      <h3>Your Score: ${score}/${total} (${percentage}%)</h3>
      <p>${percentage >= 80 ? '🌟 Excellent!' : percentage >= 60 ? '✅ Good job!' : '📚 Keep studying!'}</p>
    </div>
  `;
  
  // Disable form after submission
  form.querySelectorAll('input').forEach(input => input.disabled = true);
  document.querySelector('.submit-quiz').disabled = true;
}

loadDocuments();loadDocuments();
