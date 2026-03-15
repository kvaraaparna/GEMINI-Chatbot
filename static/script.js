async function sendMessage(){

let input = document.getElementById("userInput");

let message = input.value;

if(message.trim() === "") return;


addMessage("user",message);

input.value = "";


/* API REQUEST */

let response = await fetch("/chat",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
message:message
})

});

let data = await response.json();

addMessage("bot",data.reply);

addHistory(message,data.reply);

}


/* ADD MESSAGE TO CHAT BOX */

function addMessage(sender,text){

let chatBox = document.getElementById("chatBox");

let msg = document.createElement("div");

msg.classList.add("message");

msg.classList.add(sender);

msg.innerText = text;

chatBox.appendChild(msg);

chatBox.scrollTop = chatBox.scrollHeight;

}


/* ADD HISTORY */

function addHistory(user,bot){

let history = document.getElementById("historyBox");

let item = document.createElement("div");

item.innerHTML = `
<b>User:</b> ${user}<br>
<b>Bot:</b> ${bot}
<hr>
`;

history.appendChild(item);

}