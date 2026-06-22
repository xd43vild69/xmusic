const AudioSystem = (function() {
    let audioContext = null;
    let currentOscillator = null;
    let currentGainNode = null;

    // Tunings defined from top string (highest pitch) to bottom string (lowest pitch)
    const tunings = {
        "bass4": [43, 38, 33, 28],
        "bass4_drop_d": [43, 38, 33, 26],
        "bass4_drop_c": [41, 36, 31, 24],
        "bass5": [43, 38, 33, 28, 23],
        "guitar": [64, 59, 55, 50, 45, 40],
        "guitar_drop_d": [64, 59, 55, 50, 45, 38],
        "guitar_half_step_down": [63, 58, 54, 49, 44, 39],
        "guitar_d_standard": [62, 57, 53, 48, 43, 38],
        "guitar_drop_c": [62, 57, 53, 48, 43, 36],
        "guitar_dadgad": [62, 57, 55, 50, 45, 38],
        "guitar_open_g": [62, 59, 55, 50, 43, 38],
        "guitar_open_d": [62, 57, 54, 50, 45, 38]
    };

    function getAudioContext() {
        if (!audioContext) {
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
        if (audioContext.state === 'suspended') {
            audioContext.resume();
        }
        return audioContext;
    }

    function midiToFreq(midiNote) {
        return 440 * Math.pow(2, (midiNote - 69) / 12);
    }

    function stopCurrentNote() {
        if (currentOscillator && currentGainNode) {
            const ctx = getAudioContext();
            const releaseTime = 0.5;
            
            // Apply release envelope
            currentGainNode.gain.cancelScheduledValues(ctx.currentTime);
            currentGainNode.gain.setValueAtTime(currentGainNode.gain.value, ctx.currentTime);
            currentGainNode.gain.linearRampToValueAtTime(0.001, ctx.currentTime + releaseTime);
            
            // Stop and clean up after release
            const osc = currentOscillator;
            const gain = currentGainNode;
            
            osc.stop(ctx.currentTime + releaseTime);
            
            setTimeout(() => {
                osc.disconnect();
                gain.disconnect();
            }, releaseTime * 1000 + 50);

            currentOscillator = null;
            currentGainNode = null;
        }
    }

    function playNote(instrument, stringIndex, fretIndex) {
        // Monophonic setup: stop previous note
        stopCurrentNote();

        const ctx = getAudioContext();
        
        // Calculate frequency
        const instrumentTuning = tunings[instrument] || tunings["guitar"];
        const baseMidiNote = instrumentTuning[stringIndex];
        if (baseMidiNote === undefined) return;
        
        const midiNote = baseMidiNote + fretIndex;
        const freq = midiToFreq(midiNote);

        // Create nodes
        const osc = ctx.createOscillator();
        const gainNode = ctx.createGain();

        // Configure oscillator
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, ctx.currentTime);

        // Configure ADSR envelope
        const attackTime = 0.05;
        const decayTime = 0.1;
        const sustainLevel = 0.5;

        gainNode.gain.setValueAtTime(0.001, ctx.currentTime);
        gainNode.gain.linearRampToValueAtTime(1.0, ctx.currentTime + attackTime);
        gainNode.gain.linearRampToValueAtTime(sustainLevel, ctx.currentTime + attackTime + decayTime);

        // Route audio graph
        osc.connect(gainNode);
        gainNode.connect(ctx.destination);

        // Start oscillator
        osc.start(ctx.currentTime);

        currentOscillator = osc;
        currentGainNode = gainNode;
    }

    return {
        play: playNote,
        stop: stopCurrentNote
    };
})();

document.addEventListener("DOMContentLoaded", () => {
    // We need to retrieve the currently selected instrument from the DOM
    const instrumentSelect = document.getElementById('instrument');
    let currentInstrument = "guitar";
    if (instrumentSelect) {
        currentInstrument = instrumentSelect.value;
        if (currentInstrument === "-1") {
            currentInstrument = "guitar";
        }
    }

    const circles = document.querySelectorAll('.circle');
    const dots = document.querySelectorAll('.dot');
    
    function attachEvents(elements) {
        elements.forEach(el => {
            el.style.cursor = 'pointer';
            
            el.addEventListener('mousedown', function(e) {
                const stringIndex = parseInt(this.getAttribute('data-string'));
                const fretIndex = parseInt(this.getAttribute('data-fret'));
                
                if (!isNaN(stringIndex) && !isNaN(fretIndex)) {
                    AudioSystem.play(currentInstrument, stringIndex, fretIndex);
                }
            });

            // Stop on mouse up or mouse leave to allow for ADSR release phase
            el.addEventListener('mouseup', function(e) {
                AudioSystem.stop();
            });
            el.addEventListener('mouseleave', function(e) {
                // If a mouseleave fires while mousedown was active on this element
                if (e.buttons > 0) {
                    AudioSystem.stop();
                }
            });
        });
    }

    attachEvents(circles);
    attachEvents(dots);
});
