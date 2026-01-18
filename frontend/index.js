let userId = null;
let BACKEND_URL = ' http://127.0.0.1:8000'

// Generate unique ID and store in localStorage
function initializeUserId() {
    try {
        // Try to get existing ID from localStorage
        userId = localStorage.getItem('practiceUserId');

        if (!userId) {
            // Generate new unique ID if none exists
            userId = 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('practiceUserId', userId);
            console.log('New user ID created:', userId);
        } else {
            console.log('Existing user ID retrieved:', userId);
        }
    } catch (error) {
        // Fallback if localStorage is not available
        console.warn('localStorage not available, using session-only ID');
        userId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
}

// Initialize user ID when page loads
initializeUserId();

async function startPractice() {
    const button = document.getElementById('mainButton');
    const completionButtons = document.getElementById('completionButtons');

    try {
        button.textContent = 'Loading...';
        button.disabled = true;

        const response = await fetch(`${BACKEND_URL}/question`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-User-ID': userId
            }
        });

        if (response.ok) {
            const data = await response.json();

            // Assuming the backend returns a URL to redirect to
            const redirectUrl = `https://leetcode.com/problems/${data.question.name}/description/`;

            // Open in new tab
            window.open(redirectUrl, '_blank');

            // Hide main button and show completion buttons
            button.classList.add('hidden');
            completionButtons.classList.add('show');
        } else {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
    } catch (error) {
        console.error('Error calling /question endpoint:', error);
        alert('Failed to load question. Please try again.');

        // Reset button to original state on error
        button.textContent = 'Practice question';
        button.disabled = false;
    }
}

async function markCompleted(completed) {
    const completionButtons = document.getElementById('completionButtons');
    const mainButton = document.getElementById('mainButton');
    const buttons = completionButtons.querySelectorAll('.completion-btn');

    try {
        // Disable both completion buttons
        buttons.forEach(btn => {
            btn.disabled = true;
            btn.textContent = 'Loading...';
        });

        const response = await fetch(`${BACKEND_URL}/completed`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-User-ID': userId
            },
            body: JSON.stringify({
                status: completed
            })
        });

        if (response.ok) {
            // Hide completion buttons and show main button again
            completionButtons.classList.remove('show');
            mainButton.classList.remove('hidden');
            mainButton.textContent = 'Practice question';
            mainButton.disabled = false;
        } else {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
    } catch (error) {
        console.error('Error calling /completed endpoint:', error);
        alert('Failed to mark as completed. Please try again.');
    } finally {
        // Reset completion buttons
        buttons.forEach((btn, index) => {
            btn.disabled = false;
            btn.textContent = index === 0 ? 'Completed' : 'Attempted';
        });
    }
}

function goToSettings() {
    // Replace with your actual settings page URL
    window.location.href = 'settings.html';
}