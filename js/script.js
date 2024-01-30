document.addEventListener('DOMContentLoaded', () => {
    const sounds = document.querySelectorAll('.sound');
    const meanderToggle = document.getElementById('meanderToggle');
    let meanderActive = false; // Keeps track of whether meandering is active
    let meanderTimeout; // Will store the timeout for the meander function

    sounds.forEach(sound => {
        const playButton = sound.querySelector('.playButton');
        const volumeSlider = sound.querySelector('.volumeSlider');
        const audio = sound.querySelector('audio');

        playButton.addEventListener('click', () => {
            if (audio.paused) {
                audio.play();
                playButton.textContent = 'Pause';
            } else {
                audio.pause();
                playButton.textContent = 'Play';
            }
        });

        volumeSlider.addEventListener('input', () => {
            audio.volume = volumeSlider.value;
        });
    });
	



    meanderToggle.addEventListener('click', () => {
        meanderActive = !meanderActive; // Toggle meander state
        if (meanderActive) {
            meander(); // Start meandering if toggled on
            meanderToggle.textContent = 'Disable Meander';
        } else {
            clearTimeout(meanderTimeout); // Stop meandering if toggled off
            meanderToggle.textContent = 'Enable Meander';
        }
    });

    function meander() {
        if (!meanderActive) return; // Exit if meandering was disabled

        sounds.forEach(sound => {
            if (!sound.querySelector('audio').paused) {
                let currentVolume = sound.querySelector('audio').volume;
                let change = (Math.random() - 0.5) * 0.1;
                let newVolume = Math.min(Math.max(currentVolume + change, 0), 1);
                sound.querySelector('audio').volume = newVolume;
                sound.querySelector('.volumeSlider').value = newVolume;
            }
        });

        meanderTimeout = setTimeout(meander, 2000); // Continue meandering
    }
});
