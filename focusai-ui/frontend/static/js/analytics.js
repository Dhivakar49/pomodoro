async function loadAnalytics() {
  try {
    const response = await fetch('/api/analytics/');
    const data = await response.json();
    
    document.getElementById('totalSessions').innerText = data.total_sessions || 0;
    document.getElementById('totalMinutes').innerText = data.total_minutes || 0;
    document.getElementById('tasksCompleted').innerText = data.tasks_completed || 0;
    
    // You can add chart rendering here using a library like Chart.js
    // For now, just display basic stats
  } catch (error) {
    console.error('Analytics error:', error);
  }
}

loadAnalytics();
