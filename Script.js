// Esempio di script JavaScript utilizzando Fetch API
document.addEventListener("DOMContentLoaded", function() {
    // Fai una chiamata all'API per ottenere i messaggi
    fetch("http://localhost:5000/messages/nome_streamer")
        .then(response => response.json())
        .then(messages => {
            // Manipola i messaggi come desiderato, ad esempio aggiungi al DOM
            const chatContainer = document.getElementById("chat-messages");

            messages.forEach(message => {
                const messageElement = document.createElement("p");
                messageElement.textContent = message;
                chatContainer.appendChild(messageElement);
            });
        })
        .catch(error => {
            console.error("Errore nella chiamata all'API:", error);
        });
});
