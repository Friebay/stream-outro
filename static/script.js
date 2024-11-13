// JavaScript
// Start audio playback from 34 seconds
const audio = document.getElementById("backgroundMusic");
audio.currentTime = 34;
audio.play();

// Define the sequence of screens with their durations in milliseconds
const sequence = [
    { id: 'black-screen0', duration: 2000 },
    { id: 'screen2', duration: 4000 },
    { id: 'black-screen1', duration: 2000 },
    { id: 'screen4', duration: 4000 },
    { id: 'black-screen2', duration: 2000 },
    { id: 'screen5', duration: 4000 },
    { id: 'black-screen3', duration: 2000 },
    { id: 'screen6', duration: 4000 },
    { id: 'black-screen4', duration: 2000 },
    { id: 'screen7', duration: 4000 },
    { id: 'black-screen5', duration: 2000 },
    { id: 'screen8', duration: 4000 },
    { id: 'black-screen6', duration: 2000 },
    { id: 'screen9', duration: 4000 },
    { id: 'black-screen7', duration: 2000 },
    { id: 'screen10', duration: 4000 },
    { id: 'black-screen8', duration: 2000 },
    { id: 'screen11', duration: 4000 },
    { id: 'black-screen9', duration: 2000 },
    { id: 'credits-roll', duration: 0 } // 0 duration, as the credits animation is handled separately
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

        if (sequence[currentStep].id === 'credits-roll') {
            // Start the dynamic credits animation
            startCreditsAnimation();
        } else {
            setTimeout(showNextScreen, sequence[currentStep].duration);
        }

        currentStep++;
    } else {
        // All screens have been shown, start the credits animation
        startCreditsAnimation();
    }
}

function startCreditsAnimation() {
    const creditsScreen = document.getElementById('credits-roll');
    const creditsContainer = document.getElementById('credits-container');

    // Calculate proper duration based on content height
    const contentHeight = creditsContainer.scrollHeight;
    const viewportHeight = window.innerHeight;
    const duration = Math.max(45, (contentHeight / viewportHeight) * 30); // 30 seconds per viewport height

    // Set the animation duration dynamically
    creditsContainer.style.animationDuration = `${duration}s`;

    // Start the animation
    creditsContainer.classList.add('rolling');
}

// Start the sequence on page load
window.onload = function () {
    showNextScreen();

    // Start audio playback at specified time after it loads
    audio.addEventListener("canplay", function () {
        audio.currentTime = 34;
        audio.play();
    });
};

// Optional: Add this if you want to dynamically adjust the layout
document.addEventListener('DOMContentLoaded', function() {
    function updateDotLines() {
        const dotLines = document.querySelectorAll('.dot-line');
        dotLines.forEach(line => {
            const role = line.querySelector('.role');
            const username = line.querySelector('.username');

            // Ensure text doesn't overflow
            if (role.scrollWidth > role.offsetWidth ||
                username.scrollWidth > username.offsetWidth) {
                role.title = role.textContent;
                username.title = username.textContent;
            }
        });
    }

    // Update on load and window resize
    updateDotLines();
    window.addEventListener('resize', updateDotLines);
});
