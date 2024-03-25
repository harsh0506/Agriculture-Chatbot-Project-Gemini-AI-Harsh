// Function to send a message
function sendMessage() {
    var messageInput = document.getElementById("message-input");
    var imageInput = document.getElementById("image-input");

    var message = messageInput.value;
    var image = imageInput.files[0];

    // Create message element
    var messageElement = document.createElement("div");
    messageElement.classList.add("message");

    if (message.trim() !== "") {
        messageElement.innerText = message;
        // Create message element
        var messageElement = document.createElement("div");
        messageElement.classList.add("message");
        messageElement.innerText = message;

        // Append message to chat container
        document.getElementById("chat-container").appendChild(messageElement);

        // Send message to API
        sendTextMessage(message);

        // Save chat to localStorage
        //localStorage.setItem("chat", document.getElementById("chat-container").innerHTML);

        // Clear input field
        messageInput.value = "";
    }

    if (image) {
        var reader = new FileReader();
        reader.onload = function(event) {
            var img = document.createElement("img");
            img.src = event.target.result;
            messageElement.appendChild(img);
        };
        reader.readAsDataURL(image);
    }

    // Clear input fields
    messageInput.value = "";
    imageInput.value = "";
}

async function sendTextMessage(message) {
    let req_body = {
        "user_id": "1234",
        "question": message
    };

    try {
        const response = await fetch("http://localhost:5000/text_res", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(req_body)
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const responseData = await response.json();
        const answer = responseData.answer;

        // Create response message element
        var responseElement = document.createElement("div");
        responseElement.classList.add("message");
        responseElement.innerText = answer;

        // Append response to chat container
        document.getElementById("chat-container").appendChild(responseElement);

        // Save chat to localStorage
        // localStorage.setItem("chat", document.getElementById("chat-container").innerHTML);
    } catch (error) {
        console.error('Error:', error);
    }
}

// Load chat history from localStorage
window.onload = function() {
    var chatContainer = document.getElementById("chat-container");
    var savedChat = localStorage.getItem("chat");
    if (savedChat) {
        chatContainer.innerHTML = savedChat;
    }
};