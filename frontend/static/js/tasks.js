async function addTask() {
  const taskName = document.getElementById('taskName');
  const taskPomodoros = document.getElementById('taskPomodoros');
  const taskPriority = document.getElementById('taskPriority');
  const taskDueDate = document.getElementById('taskDueDate');
  
  if (!taskName.value.trim()) {
    alert('Please enter a task name');
    return;
  }
  
  try {
    const taskData = {
      title: taskName.value,
      required_pomodoros: parseInt(taskPomodoros.value) || 1,
      priority: taskPriority.value,
      due_date: taskDueDate.value || null
    };
    
    const response = await fetch("/api/tasks/", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(taskData)
    });
    
    if (response.ok) {
      taskName.value = '';
      taskPomodoros.value = '1';
      taskPriority.value = 'medium';
      taskDueDate.value = '';
      loadTasks();
    } else {
      const error = await response.json();
      alert('Error: ' + (error.error || 'Failed to add task'));
    }
  } catch (error) {
    console.error('Error adding task:', error);
    alert('Error adding task: ' + error.message);
  }
}

async function loadTasks() {
  try {
    const response = await fetch("/api/tasks/");
    const data = await response.json();
    
    const taskList = document.getElementById('taskList');
    taskList.innerHTML = "";
    
    if (data.length === 0) {
      taskList.innerHTML = '<li style="color: #999;">No tasks yet. Add your first task above!</li>';
      return;
    }
    
    data.forEach(task => {
      const li = document.createElement('li');
      const completedPomodoros = task.completed_pomodoros || 0;
      const requiredPomodoros = task.required_pomodoros || 1;
      const progress = (completedPomodoros / requiredPomodoros) * 100;
      
      // Priority badge
      const priorityColors = {
        high: '#ff4444',
        medium: '#ff9800',
        low: '#4caf50'
      };
      const priorityColor = priorityColors[task.priority] || priorityColors.medium;
      
      // Due date display
      let dueDateHTML = '';
      if (task.due_date) {
        const dueDate = new Date(task.due_date);
        const today = new Date();
        const isOverdue = dueDate < today && !task.completed;
        dueDateHTML = `<span style="color: ${isOverdue ? '#ff4444' : '#666'}; font-size: 0.9em;">
          📅 ${dueDate.toLocaleDateString()}
        </span>`;
      }
      
      li.innerHTML = `
        <div style="flex: 1;">
          <div style="display: flex; align-items: center; gap: 10px;">
            <span class="${task.completed ? 'completed' : ''}" style="font-weight: bold;">${task.title}</span>
            <span style="background: ${priorityColor}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.8em;">
              ${task.priority.toUpperCase()}
            </span>
            ${dueDateHTML}
          </div>
          
          <div style="margin-top: 8px;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 5px;">
              <span style="font-size: 0.9em; color: #666;">
                ${completedPomodoros}/${requiredPomodoros} Pomodoros
              </span>
              ${!task.completed ? `<button onclick="incrementPomodoro(${task.id}, ${completedPomodoros})" 
                style="padding: 2px 8px; font-size: 0.8em;">+1</button>` : ''}
            </div>
            <div class="progress-bar-container">
              <div class="progress-bar" style="width: ${progress}%"></div>
            </div>
          </div>
        </div>
        
        <div style="display: flex; gap: 8px;">
          <button onclick="startTimer(${task.id}, '${task.title.replace(/'/g, "\\'")}')" 
            class="start-timer-btn" ${task.completed ? 'disabled' : ''}>
            🍅 Start Timer
          </button>
          <button onclick="toggleTask(${task.id}, ${!task.completed})">
            ${task.completed ? 'Undo' : 'Complete'}
          </button>
          <button onclick="deleteTask(${task.id})">Delete</button>
        </div>
      `;
      taskList.appendChild(li);
    });
  } catch (error) {
    console.error('Error loading tasks:', error);
    document.getElementById('taskList').innerHTML = 
      '<li style="color: red;">Error loading tasks. Please refresh the page.</li>';
  }
}

async function toggleTask(taskId, completed) {
  try {
    const response = await fetch(`/api/tasks/${taskId}/`, {
      method: 'PATCH',
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ completed: completed })
    });
    
    if (response.ok) {
      loadTasks();
    }
  } catch (error) {
    console.error('Error toggling task:', error);
  }
}

async function deleteTask(taskId) {
  try {
    const response = await fetch(`/api/tasks/${taskId}/`, {
      method: 'DELETE'
    });
    
    if (response.ok) {
      loadTasks();
    }
  } catch (error) {
    console.error('Error deleting task:', error);
    alert('Error deleting task');
  }
}

async function incrementPomodoro(taskId, currentPomodoros) {
  try {
    const response = await fetch(`/api/tasks/${taskId}/`, {
      method: 'PATCH',
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ completed_pomodoros: currentPomodoros + 1 })
    });
    
    if (response.ok) {
      loadTasks();
    }
  } catch (error) {
    console.error('Error incrementing pomodoro:', error);
  }
}

function startTimer(taskId, taskTitle) {
  // Store task info in localStorage
  localStorage.setItem('activeTaskId', taskId);
  localStorage.setItem('activeTaskTitle', taskTitle);
  // Navigate to dashboard/timer page
  window.location.href = '/';
}

loadTasks();
