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

    // Hover logic for interval codex
    const intervalItems = document.querySelectorAll('.interval-item');
    
    intervalItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            const interval = this.getAttribute('data-interval');
            if (interval) {
                // Highlight matching elements on fretboard
                const matchingElements = document.querySelectorAll(`.circle[data-interval="${interval}"], .dot[data-interval="${interval}"]`);
                matchingElements.forEach(el => {
                    el.classList.add('highlight-interval');
                });
            }
        });

        item.addEventListener('mouseleave', function() {
            const interval = this.getAttribute('data-interval');
            if (interval) {
                // Remove highlight
                const matchingElements = document.querySelectorAll(`.circle[data-interval="${interval}"], .dot[data-interval="${interval}"]`);
                matchingElements.forEach(el => {
                    el.classList.remove('highlight-interval');
                });
            }
        });

        item.addEventListener('click', function() {
            const interval = this.getAttribute('data-interval');
            if (!interval) return;

            const roots = document.querySelectorAll('.circle[data-interval="1"]');
            if (roots.length === 0) return;
            
            // Usamos una tónica que esté en las cuerdas más graves (últimos elementos en el DOM)
            const rootEl = roots[roots.length - 1]; 
            const rootString = parseInt(rootEl.getAttribute('data-string'));
            const rootFret = parseInt(rootEl.getAttribute('data-fret'));

            const intervalElements = document.querySelectorAll(`.circle[data-interval="${interval}"], .dot[data-interval="${interval}"]`);
            if (intervalElements.length === 0) return;

            // Elegimos un elemento de intervalo. Al tomar el [0], normalmente es de cuerdas agudas.
            let intervalEl = intervalElements[0];
            
            // Si el intervalo es la octava (1), tratar de que no sea la misma tónica
            if (interval === "1" && intervalElements.length > 1) {
                intervalEl = Array.from(intervalElements).find(el => el !== rootEl) || intervalEl;
            }

            const intString = parseInt(intervalEl.getAttribute('data-string'));
            const intFret = parseInt(intervalEl.getAttribute('data-fret'));

            // Reproducir tónica
            AudioSystem.play(currentInstrument, rootString, rootFret);
            
            // Luego de 600ms reproducir el intervalo
            setTimeout(() => {
                AudioSystem.play(currentInstrument, intString, intFret);
                
                // Detener después de 800ms adicionales
                setTimeout(() => {
                    AudioSystem.stop();
                }, 800);
            }, 600);
        });
    });
});
