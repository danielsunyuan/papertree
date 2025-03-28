window.onload = function() {
    // Get the chat area and form elements
    const chatArea = document.querySelector("#chat-area");
    const form = document.querySelector("#chat-form");
    const input = document.querySelector("#user-input");

    // Get the summary element and store its text content in a variable
    const summaryElement = document.querySelector(".paper-summary");
    const summary = summaryElement.textContent;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const userInput = input.value;
        // clear the user's input
        input.value = "";
        // Append the user's input to the chat area
        chatArea.insertAdjacentHTML('beforeend', `<p id="human">${userInput}</p>`);
        // Insert a div element for spacing
        chatArea.insertAdjacentHTML('beforeend', `<div class="spacer"></div>`);
        // Scroll to the bottom of the chat area
        chatArea.scrollTop = chatArea.scrollHeight;


        try {
            const response = await fetch("/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ user_input: userInput, paper_summary: summary }),
            });
            const data = await response.json();
            // Append the AI's response to the chat area
            chatArea.insertAdjacentHTML('beforeend', `<p id="ai">${data.AIresponse}</p>`);
            // Insert a div element for spacing
            chatArea.insertAdjacentHTML('beforeend', `<div class="spacer"></div>`);
            // Scroll to the bottom of the chat area
            chatArea.scrollTop = chatArea.scrollHeight;
        } catch (err) {
            console.error("Error:", err);
        }
    });
    
    $(document).ready(function(){
        $("#chatbox").hide();
        $("#chatbox").fadeIn(3000);
    }); 
}

