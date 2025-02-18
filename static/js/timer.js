let timerSeconds = 2700; //45min 60*45=2700
let timerInterval;

function updateTimerDisplay() {
    const minutes = Math.floor(timerSeconds / 60);
    const seconds = timerSeconds % 60;
    document.getElementById("timer").textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

function startTimer() {
    timerInterval = setInterval(function() {
        if (timerSeconds > 0) {
            timerSeconds--;
            updateTimerDisplay();
        } else {
            clearInterval(timerInterval);  
            alert("Timer is finished!");
            document.getElementById('quiz-form').submit()
        }
    }, 1000);  
}


window.onload = function() {
  updateTimerDisplay();
  startTimer();
};