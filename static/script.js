document.getElementById('messageForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value.replace('@', '').trim();
    const message = document.getElementById('message').value;

    fetch('/send-message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: username, message: message })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('response').innerText = data.response;
        document.getElementById('username').value = ''; // Очистить поле ввода
        document.getElementById('message').value = ''; // Очистить поле ввода
    });
});
