// Start audio playback from 34 seconds
const audio = document.getElementById("backgroundMusic");
audio.currentTime = 34; 
audio.play();

// Define the sequence of screens with their durations in milliseconds
const sequence = [
    { id: 'black-screen0', duration: 200 },
    { id: 'screen2', duration: 4000 },
    { id: 'black-screen1', duration: 200 },
    { id: 'screen4', duration: 4000 },
    { id: 'black-screen2', duration: 200 },
    { id: 'screen5', duration: 4000 },
    { id: 'black-screen3', duration: 200 },
    { id: 'screen6', duration: 4000 },
    { id: 'black-screen4', duration: 200 },
    { id: 'screen7', duration: 4000 },
    { id: 'black-screen5', duration: 200 },
    { id: 'screen8', duration: 4000 },
    { id: 'black-screen6', duration: 200 },
    { id: 'screen9', duration: 8000 },
    { id: 'black-screen7', duration: 200 },
    { id: 'screen10', duration: 8000 },
    { id: 'black-screen8', duration: 200 },
    { id: 'screen11', duration: 8000 },
    { id: 'black-screen9', duration: 200 },
    { id: 'screen-credits', duration: 600000 }
];

let currentStep = 0;

function showNextScreen() {
    if (currentStep > 0) {
        document.getElementById(sequence[currentStep - 1].id).classList.remove('visible');
    }
    if (currentStep < sequence.length) {
        const screen = document.getElementById(sequence[currentStep].id);
        screen.classList.add('visible');
        
        // If this is the credits screen, ensure the animation starts properly
        if (sequence[currentStep].id === 'screen-credits') {
            restartCredits();
        }
        
        setTimeout(showNextScreen, sequence[currentStep].duration);
        currentStep++;
    }
}

// Improved audio handling
document.addEventListener("DOMContentLoaded", function() {
    const audio = document.getElementById("backgroundMusic");
    
    // Create a promise to handle audio loading
    const audioReady = new Promise((resolve, reject) => {
        audio.addEventListener("canplaythrough", resolve);
        audio.addEventListener("error", reject);
    });

    // Handle audio playback
    audioReady
        .then(() => {
            // Remove controls after loading (if you don't want them visible)
            audio.removeAttribute("controls");
            
            // Set volume to ensure it's not muted
            audio.volume = 0.75;
            
            // Set the time and play
            audio.currentTime = 34;
            
            // Play with error handling
            const playPromise = audio.play();
            
            if (playPromise !== undefined) {
                playPromise
                    .then(() => {
                        console.log("Audio playback started successfully");
                    })
                    .catch(error => {
                        console.error("Audio playback failed:", error);
                    });
            }
        })
        .catch(error => {
            console.error("Audio loading failed:", error);
        });
});

// Start the sequence on page load
window.onload = function() {
    showNextScreen();
};

function restartCredits() {
    const credits = document.querySelector('.credits');
    credits.style.animation = 'none';
    credits.offsetHeight; // Trigger reflow
    credits.style.animation = 'scrollCredits 600s linear forwards';
}