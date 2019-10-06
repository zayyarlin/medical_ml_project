const button = document.getElementById("send-button");
const text = document.getElementById("send-text");
const chat = document.getElementById("chat");
const id = document.getElementById("hidden-bot").value

function addMyChat(msg){
  const message = `<div class="container darker">
  <img src="/w3images/avatar_g2.jpg" alt="Avatar" class="right">
  <p>${msg}</p>
  <span class="time-left">11:01</span>
  </div>`
  chat.innerHTML += message;
}

function addBotChat(msg){
  const message = `<div class="container">
    <img src="/w3images/bandmember.jpg" alt="Avatar">
    <p>${msg}</p>
    <span class="time-right">11:00</span>
  </div>`
  chat.innerHTML += message;
}

async function postData(url = '', data = {}) {
  // Default options are marked with *
  const response = await fetch(url, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    credentials: 'same-origin', // include, *same-origin, omit
    headers: {
      'Content-Type': 'application/json'
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    redirect: 'follow', // manual, *follow, error
    body: JSON.stringify(data) // body data type must match "Content-Type" header
  });
  return await response.json(); // parses JSON response into native JavaScript objects
}

