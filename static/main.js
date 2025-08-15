

console.log('static/main.js is being loaded!');


// Wait until DOM is ready before continuing
(async () => {
  if (document.readyState === 'loading') {
    await new Promise(resolve => {
      document.addEventListener('DOMContentLoaded', resolve, { once: true });
    });
  }
})();

console.log('static/main.js has been loaded!');

function appendToDiv(msg,divId, messageId=0, color='white'){
    let msgDiv = document.createElement("div");
    msgDiv.setAttribute('settled','false');
    msgDiv.id = messageId;
    msgDiv.style.color = color;
    console.log(`Debug: color: ${color}`)
    let msgContainer = document.getElementById(divId);
    msgDiv.textContent = msg || "Error: No response";
    //msgDiv.style.background = "rgb(50,0,0)";
    /*msgDiv.style.padding = "8px 12px";
    msgDiv.style.borderRadius = "10px";
    msgDiv.style.marginBottom = "8px";
    msgDiv.style.maxWidth = "80%";
     */

    msgContainer.appendChild(msgDiv);
    msgContainer.scrollTop = msgContainer.scrollHeight;
}

function roundToSigFigs(num, sigFigs) {
  if (num === 0) return 0;
  const magnitude = Math.floor(Math.log10(Math.abs(num)));
  const factor = Math.pow(10, sigFigs - 1 - magnitude);
  return Math.round(num * factor) / factor;
}

function genMessageId(){
    let timestamp = new Date().toLocaleString('en-US', { hour12: false }).replace(/[^0-9]/g, '');
    timestamp = parseInt(timestamp)
    let random = Math.round(Math.random() * 99999)
    return timestamp + random
}

function genTimestamp(){
    const now = new Date();
    const pad = n => n.toString().padStart(2, '0');
    const hours = pad(now.getHours());
    const minutes = pad(now.getMinutes());
    const seconds = pad(now.getSeconds());
    return `${hours}:${minutes}:${seconds}`;
}


// true if you own message
function resolveMessage(message, messageId, div='messages'){
    if (document.getElementById(messageId)){
        targetMessage = document.getElementById(messageId).remove()
        appendToDiv(message, div, messageId=messageId)
        console.log(`Resolved message ${messageId}`)
        return true
    }else{
        appendToDiv(message, div, messageId=messageId)
        return false
    }
}

fetch('/io/prefix')
  .then(response => response.text())
  .then(data => {
    window.prefix = data;
    console.log('prefix set globally:', window.prefix);
  })
  .catch(err => console.error(err));
prefix = window.prefix

const form = document.getElementById("inputForm");
const messageContainer = document.getElementById("messages");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    let input = document.getElementById("messageInput");
    let message = input.value.trim();
    let messageId = genMessageId();
    if (!prefix){
        console.error("Error: No prefix apparently. wait till prefix loads?");
        appendToDiv('!!!WORNING: No prefix apparently. Ur shit will still work, but might look nasty')
        let prefix = 'unknown'
    }
    if (!message){
        console.log("Error: no message aparently. Message:"+message);
        return;
    }
    let messageToShow = genTimestamp()+':'+`[${prefix}]:`+message
    appendToDiv(messageToShow, 'messages', messageId=messageId, color='rgb(150, 75, 0)')
    console.log('message:'+message);


    // Send JSON to server
    try {
        const response = await fetch("/io/form", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message, messageId: messageId })
        });

        const data = await response.json();

        // add server response above the form
        // appendToDiv(data.response, 'messages')

        input.value = "";
        input.focus();
} catch (err) {
    console.error("Error:", err);
}
});




console.log('starting fetch block');
async function fetch_message(url){
    try {
        let response = await fetch(url);
        if (!response.ok){
            console.log('HTTP error fetching ${url}');
            throw new Error('HTTP error! Status: ${response.status}');
        }
        let data = await response.json();
        console.log('fetch_message returning response.json')
        //return JSON.stringify({data});
        msg = data.response;
        console.log(`fetch_message: msg: ${msg}`);
        console.log('appending to div');
        appendToDiv(msg, 'messages');
        fetch_message(url);




    } catch (error){
        console.error(`Error fetching json:${error}`)
        return null;
    }
};

// socket magik starts
let socket = io();
socket.on('connect',() => {
    console.log('connected to socket');
})
socket.on('disconnect', () =>{
    console.log('disconnected from socket');
})
socket.on('new_data', (data) => {
    console.log('Received from server:', data);
});

socket.on('new_message', (data) =>{
    console.log(`receved message: >${data}<`)
    console.log('data.message',data.message)
    console.log('Id:', data.messageId)
    id = data.messageId
    message = data.message
    resolveMessage(message, id)

})

function send_message(msg){
    socket.emit('event', { message: msg})
};

