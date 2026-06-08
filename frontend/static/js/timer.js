let time = 1500, interval;
let isRunning = false;

// Check if there's an active task from localStorage
window.addEventListener('DOMContentLoaded', () => {
  // Load tasks into dropdown
  loadTasksDropdown();
  
  const taskId = localStorage.getItem('activeTaskId');
  const taskTitle = localStorage.getItem('activeTaskTitle');
  
  if (taskId && taskTitle) {
    const taskInfo = document.createElement('div');
    taskInfo.style.cssText = 'text-align: center; margin: 1rem 0; padding: 1rem; background: #f8f9fa; border-radius: 10px;';
    taskInfo.innerHTML = `<strong>🎯 Working on:</strong> ${taskTitle}`;
    document.querySelector('.container').insertBefore(taskInfo, document.getElementById('timer'));
  }
});

async function loadTasksDropdown() {
  try {
    const response = await fetch('/api/tasks/');
    const tasks = await response.json();
    
    const select = document.getElementById('taskSelect');
    select.innerHTML = '<option value="">Select a task (optional)</option>';
    
    tasks.forEach(task => {
      if (!task.completed) {
        const option = document.createElement('option');
        option.value = task.id;
        option.textContent = task.title;
        select.appendChild(option);
      }
    });
    
    // Set selected task if there's an active one
    const activeTaskId = localStorage.getItem('activeTaskId');
    if (activeTaskId) {
      select.value = activeTaskId;
    }
    
    // Handle task selection
    select.addEventListener('change', (e) => {
      if (e.target.value) {
        const selectedTask = tasks.find(t => t.id == e.target.value);
        if (selectedTask) {
          localStorage.setItem('activeTaskId', selectedTask.id);
          localStorage.setItem('activeTaskTitle', selectedTask.title);
        }
      } else {
        localStorage.removeItem('activeTaskId');
        localStorage.removeItem('activeTaskTitle');
      }
    });
  } catch (error) {
    console.error('Error loading tasks:', error);
  }
}

function start() {
  if (isRunning) return; // Prevent starting if already running
  isRunning = true;
  
  // Disable start button while running
  document.querySelector('button[onclick="start()"]').disabled = true;
  
  interval = setInterval(() => {
    time--;
    document.getElementById("timer").innerText =
      Math.floor(time/60) + ":" + String(time%60).padStart(2,'0');

    if(time <= 0) complete();
  }, 1000);
}

function pause() { 
  if (!isRunning) return;
  clearInterval(interval); 
  isRunning = false;
  
  // Re-enable start button
  document.querySelector('button[onclick="start()"]').disabled = false;
}

function reset() { 
  clearInterval(interval); 
  isRunning = false;
  location.reload(); 
}

async function complete() {
  clearInterval(interval);
  isRunning = false;
  
  // Re-enable buttons
  document.querySelector('button[onclick="start()"]').disabled = false;
  document.querySelector('button[onclick="pause()"]').disabled = false;
  document.querySelector('button[onclick="reset()"]').disabled = false;
  
  try {
    // Save pomodoro session - only when timer completes naturally
    await fetch("/api/pomodoro/save/", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ duration: 25 })
    });
    
    // Increment task pomodoro count if there's an active task
    const taskId = localStorage.getItem('activeTaskId');
    if (taskId) {
      // Get current task data
      const response = await fetch("/api/tasks/");
      const tasks = await response.json();
      const currentTask = tasks.find(t => t.id == taskId);
      
      if (currentTask) {
        // Increment completed pomodoros
        await fetch(`/api/tasks/${taskId}/`, {
          method: 'PATCH',
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({ 
            completed_pomodoros: (currentTask.completed_pomodoros || 0) + 1 
          })
        });
      }
    }
    
    alert('🎉 Pomodoro completed! Great work!');
    localStorage.removeItem('activeTaskId');
    localStorage.removeItem('activeTaskTitle');
    
    // Auto reload to reset
    setTimeout(() => location.reload(), 1000);
  } catch (error) {
    console.error('Error completing pomodoro:', error);
  }
}

