const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');

function appendMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `${sender}-message`);
    
    if (sender === 'klaude') {
        messageDiv.innerHTML = marked.parse(text);
    } else {
        messageDiv.textContent = text;
    }
    
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight; // Keep chat scrolled to bottom
}
async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    appendMessage(text, 'user');
    userInput.value = '';

    try {
        const response = await fetch("http://127.0.0.1:8000/chat" ,{
            method : 'POST',
            headers : {
                'Content-Type' : 'application/json'
            },
            body : JSON.stringify({message : text})
        })
        const data = await response.json();
        appendMessage(data.response, 'klaude');
    }
    catch (error) {
        appendMessage("Error: Could not connect to backend.", 'klaude');
        console.error(error);
    }
}
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}