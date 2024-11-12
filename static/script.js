// Start audio playback from 34 seconds
const audio = document.getElementById("backgroundMusic");
audio.currentTime = 34;  // Set start time to 0:34
audio.play();

// Define the sequence of screens with their durations in milliseconds
const sequence = [
    { id: 'screen1', duration: 2000 },
    { id: 'screen2', duration: 2000 },
    { id: 'black-screen1', duration: 2000 },
    { id: 'screen4', duration: 3000 },
    { id: 'black-screen2', duration: 2000 },
    { id: 'screen5', duration: 3000 },
    { id: 'black-screen3', duration: 2000 },
    { id: 'screen6', duration: 4000 },
    { id: 'black-screen4', duration: 2000 },
    { id: 'screen7', duration: 4000 },
    { id: 'black-screen5', duration: 2000 },
    { id: 'credits-roll', duration: 45000 },
];

let currentStep = 0;

function showNextScreen() {
    if (currentStep > 0) {
        // Fade out the previous screen
        document.getElementById(sequence[currentStep - 1].id).classList.remove('visible');
    }

    if (currentStep < sequence.length) {
        // Fade in the current screen
        const screen = document.getElementById(sequence[currentStep].id);
        screen.classList.add('visible');
        setTimeout(showNextScreen, sequence[currentStep].duration);
        currentStep++;
    }
}

// Start the sequence on page load
window.onload = function () {
    showNextScreen();

    // Start audio playback at specified time after it loads
    audio.addEventListener("canplay", function () {
        audio.currentTime = 34; // Start at 0:34
        audio.play();
    });
};