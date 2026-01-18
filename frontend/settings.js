const BACKEND_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:8000'
    : 'https://coding-practice.com/api';

let isUpdating = false;

const sliders = {
    new: document.getElementById('newSlider'),
    attempted: document.getElementById('attemptedSlider'),
    completed: document.getElementById('completedSlider')
};

const displays = {
    new: document.getElementById('newPercent'),
    attempted: document.getElementById('attemptedPercent'),
    completed: document.getElementById('completedPercent')
};

const bars = {
    new: document.getElementById('newBar'),
    attempted: document.getElementById('attemptedBar'),
    completed: document.getElementById('completedBar')
};

const totalDisplay = document.getElementById('totalDisplay');

function updateDisplay() {
    if (isUpdating) return;

    const values = {
        new: parseInt(sliders.new.value),
        attempted: parseInt(sliders.attempted.value),
        completed: parseInt(sliders.completed.value)
    };

    const total = values.new + values.attempted + values.completed;

    // Update percentage displays
    displays.new.textContent = values.new + '%';
    displays.attempted.textContent = values.attempted + '%';
    displays.completed.textContent = values.completed + '%';

    // Update visual bar
    bars.new.style.width = values.new + '%';
    bars.attempted.style.width = values.attempted + '%';
    bars.completed.style.width = values.completed + '%';

    // Update total display
    if (total === 100) {
        totalDisplay.innerHTML = '<span class="valid">Total: 100%</span>';
    } else {
        totalDisplay.innerHTML = `<span class="invalid">Total: ${total}% (Must equal 100%)</span>`;
    }
}

function balanceSliders(changedSlider) {
    if (isUpdating) return;
    isUpdating = true;

    const values = {
        new: parseInt(sliders.new.value),
        attempted: parseInt(sliders.attempted.value),
        completed: parseInt(sliders.completed.value)
    };

    const total = values.new + values.attempted + values.completed;
    const excess = total - 100;

    if (excess !== 0) {
        const others = Object.keys(values).filter(key => key !== changedSlider);
        const otherTotal = others.reduce((sum, key) => sum + values[key], 0);

        if (otherTotal > 0) {
            others.forEach(key => {
                const proportion = values[key] / otherTotal;
                const newValue = Math.max(0, Math.round(values[key] - (excess * proportion)));
                values[key] = newValue;
                sliders[key].value = newValue;
            });

            // Fine-tune to ensure exactly 100%
            const newTotal = values.new + values.attempted + values.completed;
            if (newTotal !== 100) {
                const diff = 100 - newTotal;
                const firstOther = others[0];
                values[firstOther] = Math.max(0, values[firstOther] + diff);
                sliders[firstOther].value = values[firstOther];
            }
        }
    }

    isUpdating = false;
    updateDisplay();
}

function setPreset(newVal, attemptedVal, completedVal) {
    isUpdating = true;
    sliders.new.value = newVal;
    sliders.attempted.value = attemptedVal;
    sliders.completed.value = completedVal;
    isUpdating = false;
    updateDisplay();
}

async function saveSettings() {
    const settings = {
        percentages: {
            new: parseInt(sliders.new.value),
            attempted: parseInt(sliders.attempted.value),
            completed: parseInt(sliders.completed.value)
        },
        timing: {
            attemptedDelay: parseInt(document.getElementById('attemptedTime').value),
            completedDelay: parseInt(document.getElementById('completedTime').value)
        },
        difficulty: {
            easy: document.getElementById('easyBtn').classList.contains('active'),
            medium: document.getElementById('mediumBtn').classList.contains('active'),
            hard: document.getElementById('hardBtn').classList.contains('active')
        }
    };

    const total = settings.percentages.new + settings.percentages.attempted + settings.percentages.completed;

    if (total !== 100) {
        alert('Please ensure percentages add up to 100%');
        return;
    }

    // Check that at least one difficulty is selected
    if (!settings.difficulty.easy && !settings.difficulty.medium && !settings.difficulty.hard) {
        alert('Please select at least one difficulty level');
        return;
    }

    try {
        const response = await fetch(`${BACKEND_URL}/user/settings`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(settings)
        });

        if (response.ok) {
            window.location.href = 'index.html';
        } else {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
    } catch (error) {
        console.error('Error saving settings:', error);
        alert('Failed to save settings. Please try again.');
    }
}

async function loadSettings() {
    try {
        const response = await fetch(`${BACKEND_URL}/user/settings`);

        if (response.ok) {
            const settings = await response.json();

            // Update sliders
            isUpdating = true;
            sliders.new.value = settings.percentages.new;
            sliders.attempted.value = settings.percentages.attempted;
            sliders.completed.value = settings.percentages.completed;
            isUpdating = false;

            // Update timing controls
            document.getElementById('attemptedTime').value = settings.timing.attemptedDelay;
            document.getElementById('completedTime').value = settings.timing.completedDelay;

            // Update difficulty buttons
            if (settings.difficulty) {
                document.getElementById('easyBtn').classList.toggle('active', settings.difficulty.easy);
                document.getElementById('mediumBtn').classList.toggle('active', settings.difficulty.medium);
                document.getElementById('hardBtn').classList.toggle('active', settings.difficulty.hard);
            }

            // Update display
            updateDisplay();

            console.log('Settings loaded:', settings);
        } else if (response.status === 404) {
            console.log('No saved settings found, using defaults');
        } else {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
    } catch (error) {
        console.error('Error loading settings:', error);
        console.log('Using default settings');
    }
}

function toggleDifficulty(difficulty) {
    const btn = document.getElementById(difficulty + 'Btn');
    const allBtns = document.querySelectorAll('.difficulty-btn');
    const activeBtns = document.querySelectorAll('.difficulty-btn.active');

    // If trying to deactivate the last active button, prevent it
    if (btn.classList.contains('active') && activeBtns.length === 1) {
        return;
    }

    btn.classList.toggle('active');
}

// Event listeners
sliders.new.addEventListener('input', () => balanceSliders('new'));
sliders.attempted.addEventListener('input', () => balanceSliders('attempted'));
sliders.completed.addEventListener('input', () => balanceSliders('completed'));

// Load settings on page load
window.addEventListener('load', loadSettings);

// Initialize display
updateDisplay();