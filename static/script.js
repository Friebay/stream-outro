document.addEventListener('DOMContentLoaded', function() {
    const audio = document.getElementById("backgroundMusic");
    let audioStarted = false;

    // Define the sequence of screens with their durations in milliseconds
    const sequence = [
        { id: 'black-screen0', duration: 200 },
        { id: 'screen2', duration: 400 },
        { id: 'black-screen1', duration: 200 },
        { id: 'screen4', duration: 400 },
        { id: 'black-screen2', duration: 200 },
        { id: 'screen5', duration: 400 },
        { id: 'black-screen3', duration: 200 },
        { id: 'screen6', duration: 400 },
        { id: 'black-screen4', duration: 200 },
        { id: 'screen7', duration: 400 },
        { id: 'black-screen5', duration: 200 },
        { id: 'screen8', duration: 400 },
        { id: 'black-screen6', duration: 200 },
        { id: 'screen9', duration: 400 },
        { id: 'black-screen7', duration: 200 },
        { id: 'screen10', duration: 400 },
        { id: 'black-screen8', duration: 200 },
        { id: 'screen11', duration: 400 },
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

            if (sequence[currentStep].id === 'screen-credits') {
                restartCredits();
            }

            setTimeout(showNextScreen, sequence[currentStep].duration);
            currentStep++;
        }
    }

    function restartCredits() {
        const credits = document.querySelector('.credits');
        credits.style.animation = 'none';
        credits.offsetHeight; // Trigger reflow
        credits.style.animation = 'scrollCredits 600s linear forwards';
    }

    // Function to start everything
    function startSequence() {
        if (!audioStarted) {
            audioStarted = true;

            // Set initial time and ensure it's loaded
            audio.currentTime = 34;

            // Start playing when the audio is ready
            audio.addEventListener('canplaythrough', function startPlayback() {
                audio.play().catch(error => {
                    console.error("Audio playback failed:", error);
                });
                // Remove the event listener after it fires
                audio.removeEventListener('canplaythrough', startPlayback);
            }, { once: true });

            // Start the visual sequence immediately
            showNextScreen();
        }
    }

    // Start automatically after a short delay to ensure everything is loaded
    setTimeout(startSequence, 500);

    // Error handling for audio
    audio.addEventListener('error', function(e) {
        console.error('Audio error:', e);
        if (!audioStarted) {
            showNextScreen();
        }
    });
});