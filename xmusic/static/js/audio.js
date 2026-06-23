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

    // --- Metronome System ---
    let isPlayingMetronome = false;
    let bpm = 120;
    let nextNoteTime = 0.0;
    let timerWorker = null;
    const lookahead = 25.0; 
    const scheduleAheadTime = 0.1;

    function nextNote() {
        const secondsPerBeat = 60.0 / bpm;
        nextNoteTime += secondsPerBeat;
    }

    function scheduleNote(time) {
        const ctx = getAudioContext();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();

        osc.connect(gain);
        gain.connect(ctx.destination);

        osc.type = 'square';
        osc.frequency.value = 800; // Pitch of the beep

        // Envelope for short beep
        gain.gain.setValueAtTime(0, time);
        gain.gain.linearRampToValueAtTime(0.3, time + 0.002);
        gain.gain.linearRampToValueAtTime(0, time + 0.04);

        osc.start(time);
        osc.stop(time + 0.05);

        // Visual flash sync
        const timeToPlay = time - ctx.currentTime;
        if (timeToPlay > 0) {
            setTimeout(flashLed, timeToPlay * 1000);
        } else {
            flashLed();
        }
    }

    function flashLed() {
        const led = document.getElementById('metro-led');
        if (led) {
            led.classList.add('flash');
            setTimeout(() => led.classList.remove('flash'), 80);
        }
    }

    function scheduler() {
        if (!isPlayingMetronome) return;
        const ctx = getAudioContext();

        while (nextNoteTime < ctx.currentTime + scheduleAheadTime) {
            scheduleNote(nextNoteTime);
            nextNote();
        }

        timerWorker = setTimeout(scheduler, lookahead);
    }

    function startMetronome() {
        if (isPlayingMetronome) return;
        const ctx = getAudioContext();
        isPlayingMetronome = true;
        nextNoteTime = ctx.currentTime + 0.05;
        scheduler();
    }

    function stopMetronome() {
        isPlayingMetronome = false;
        clearTimeout(timerWorker);
    }

    function setBpm(newBpm) {
        bpm = newBpm;
    }

    function isMetronomePlaying() {
        return isPlayingMetronome;
    }

    return {
        play: playNote,
        stop: stopCurrentNote,
        startMetronome: startMetronome,
        stopMetronome: stopMetronome,
        setBpm: setBpm,
        isMetronomePlaying: isMetronomePlaying
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
                AudioSystem.stop();
            });
        });
    }

    attachEvents(circles);
    attachEvents(dots);

    // --- Metronome UI Binding ---
    const metroPlayBtn = document.getElementById('metro-play');
    const metroBpmInput = document.getElementById('metro-bpm');

    if (metroPlayBtn && metroBpmInput) {
        metroPlayBtn.addEventListener('click', () => {
            if (AudioSystem.isMetronomePlaying()) {
                AudioSystem.stopMetronome();
                metroPlayBtn.textContent = '▶';
                metroPlayBtn.classList.remove('active');
            } else {
                AudioSystem.startMetronome();
                metroPlayBtn.textContent = '⬛';
                metroPlayBtn.classList.add('active');
            }
        });

        metroBpmInput.addEventListener('input', (e) => {
            let val = parseInt(e.target.value);
            if (val >= 10 && val <= 300) {
                AudioSystem.setBpm(val);
            }
        });

        AudioSystem.setBpm(parseInt(metroBpmInput.value) || 120);
    }

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
            
            // Usamos una tónica del medio para no ser ni muy aguda ni muy grave
            const middleIndex = Math.floor(roots.length / 2);
            const rootEl = roots[middleIndex]; 
            const rootString = parseInt(rootEl.getAttribute('data-string'));
            const rootFret = parseInt(rootEl.getAttribute('data-fret'));
            const approxRootPitch = -rootString * 5 + rootFret;

            const intervalElements = document.querySelectorAll(`.circle[data-interval="${interval}"], .dot[data-interval="${interval}"]`);
            if (intervalElements.length === 0) return;

            // Elegimos un intervalo que esté lo más cerca posible de la tónica (idealmente un poco más agudo)
            let bestIntervalEl = intervalElements[0];
            let minPitchDiff = Infinity;

            intervalElements.forEach(el => {
                // Si es la octava, preferimos no usar la misma nota exacta
                if (interval === "1" && el === rootEl && intervalElements.length > 1) return;
                
                const s = parseInt(el.getAttribute('data-string'));
                const f = parseInt(el.getAttribute('data-fret'));
                const approxPitch = -s * 5 + f;
                
                let diff = approxPitch - approxRootPitch;
                // Preferimos que sea más agudo (positivo), penalizamos si es más grave
                if (diff < 0) {
                    diff = Math.abs(diff) + 100;
                }
                
                if (diff < minPitchDiff) {
                    minPitchDiff = diff;
                    bestIntervalEl = el;
                }
            });

            const intString = parseInt(bestIntervalEl.getAttribute('data-string'));
            const intFret = parseInt(bestIntervalEl.getAttribute('data-fret'));

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
