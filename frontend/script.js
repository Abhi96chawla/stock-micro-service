import { API_URL } from './env.js';

document.getElementById('showLogin').addEventListener('click', () => {
    document.getElementById('loginForm').style.display = 'flex';
    document.getElementById('signupForm').style.display = 'none';
});

document.getElementById('showSignup').addEventListener('click', () => {
    document.getElementById('signupForm').style.display = 'flex';
    document.getElementById('loginForm').style.display = 'none';
});

document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    try {
        const response = await fetch(`${API_URL}/api/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });
        const data = await response.json();
        document.getElementById('content').innerHTML = `<p>${data.message}</p>`;
        
        // If login is successful, redirect to the welcome page
        if (data.redirect) {
            window.location.href = '/welcome.html'; // Assuming you have a welcome.html page
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('content').innerHTML = '<p>Error logging in</p>';
    }
});

document.getElementById('signupForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const firstName = document.getElementById('signupFirstName').value;
    const lastName = document.getElementById('signupLastName').value;
    const email = document.getElementById('signupEmail').value;
    const password = document.getElementById('signupPassword').value;
    const address = document.getElementById('signupAddress').value;
    const postalCode = document.getElementById('signupPostalCode').value;
    
    try {
        const response = await fetch(`${API_URL}/api/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ firstName, lastName, email, password, address, postalCode }),
        });
        const data = await response.json();
        document.getElementById('content').innerHTML = `<p>${data.message}</p>`;
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('content').innerHTML = '<p>Error signing up</p>';
    }
});