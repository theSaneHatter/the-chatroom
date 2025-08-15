<!DOCTYPE html>
<html>
<head>
  <title>Scrollable Messages</title>
  <style>
    html, body {
      margin: 0;
      padding: 0;
      height: 100%;
      font-family: Arial, sans-serif;
      background-color: black;
      color: white;
    }

    body {
      display: flex;
      flex-direction: column;
    }

    #messages {
      flex: 1; /* 👈 fill remaining vertical space */
      overflow-y: auto; /* 👈 scroll if content overflows */
      padding: 10px;
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
      align-items: flex-start;
      box-sizing: border-box;
      border-top: 1px solid white;
    }

    #messages > div {
      width: 100%;
      margin-bottom: 4px;
      color: white;
      text-align: left;
      white-space: pre-wrap;
      overflow-wrap: break-word;
    }

    #inputForm {
      display: flex;
      padding: 10px;
      background: #111;
      border-top: 1px solid white;
    }

    #inputForm input {
      flex: 1;
      font-size: 1rem;
      padding: 5px;
      border: 1px solid red;
      background-color: black;
      color: white;
    }

    #inputForm button {
      padding: 5px 10px;
      background-color: green;
      color: white;
      border: none;
      margin-left: 5px;
    }
  </style>
</head>
<body>

  <div id="messages">
    <div>Initial message</div>
  </div>

  <form id="inputForm">
    <input type="text" id="messageInput" placeholder="Type a message" />
    <button type="submit">Send</button>
  </form>

  <script>
    const form = document.getElementById("inputForm");
    const input = document.getElementById("messageInput");
    const messages = document.getElementById("messages");

    function appendToDiv(msg) {
      const div = document.createElement("div");
      div.textContent = msg;
      messages.appendChild(div);
      messages.scrollTop = messages.scrollHeight; // 👈 Scroll to bottom
    }

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const text = input.value.trim();
      if (text) {
        appendToDiv(text);
        input.value = "";
      }
    });

    // Optional: auto-fill some messages for scroll testing
    for (let i = 0; i < 50; i++) {
      appendToDiv("Test message " + (i + 1));
    }
  </script>

</body>
</html>
