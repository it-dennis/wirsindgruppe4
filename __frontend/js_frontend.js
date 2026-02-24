// ausführbar zB mit "node js_frontend.js" in bash
// JS Version des python Codes im Kommentar
// encodeURIComponent convertiert einige Zeichen in Zeichen, die in eine URL passen, zB " " zu "%20"
// Nicht so gut für Passwörter dieser Code hier

let url = "http://127.0.0.1:8000"
let data = ""
logging = true

// Notiz erstellen
async function create_note(board_id, title, content) {
  const response = await fetch(`${url}/notes/?title=${encodeURIComponent(title)}&content=${encodeURIComponent(content)}&board_id=${board_id}`, {
    method: "POST",
  });
  data = await response.json();
  if (logging) {console.log(data);}
  return data
}

async function delete_note(note_id) {
  const response = await fetch(`${url}/notes/${note_id}/`, {
    method: "DELETE"
  });
  data = await response.json();
  if (logging) {console.log(data);}
  return data
}

async function get_user_boards(user_id) {
  const response = await fetch(`${url}/users/${user_id}/boards`);
  data = await response.json();
  if (logging) {console.log(data);}
  return data
}

async function get_user_boards_notes(user_id) {
  const response = await fetch(`${url}/users/${user_id}/notes`);
  data = await response.json();
  if (logging) {console.log(data);}
  return data
}

// Sign up
async function register_user(username, password) {
  const response = await fetch(url + `/users/register?username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`, {
  method: "POST",
  });
  data = await response.json();
  if (logging) {console.log(data);}
  return data
}

// login
async function login_user(username, password) {
  const response = await fetch(url + `/users/login?username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`, {
  method: "GET",
  });
  data = await response.json();
  if (logging) {console.log(data);}
  return data
}

async function delete_user(user_id) {
  const response = await fetch(`${url}/users/${user_id}`, {
    method: "DELETE"
  });
  data = await response.json();
  if (logging) {console.log(data);}
  return data
}

// Board erstellen
async function create_board(name, user_id) {
  const response = await fetch(`${url}/boards?name=${encodeURIComponent(name)}&owner_id=${user_id}`, {
    method: "POST",
  });
  data = await response.json();
  if (logging) {console.log(data);}
  return data
}

// Board update add user

// Board update remove user

async function clear_database() {
  const response = await fetch(`${url}/clear/`, {
    method: "DELETE"
  });
  data = await response.json();
  if (logging) {console.log(data);}
  return data
}

// Beispiel Code:
// Muss in asyn Function gesteckt werden, damit await functioniert

async function main() {

  username = "JS_user"
  password = "123456"

  // login Versuch, wenn login nicht true, stattdessen registrieren

  response = await login_user(username, password)

  if (response["login"]) {
    console.log("login")
    
  } else {
    response = await register_user(username, password)
    console.log("sign up")
  }

  user_id = response["id"]
  console.log(user_id)
  
  // Board posten

  response = await create_board("Gruppenarbeit", user_id)

  gruppenarbeit_board = response

  response = await create_note(gruppenarbeit_board["id"], "Erste Notiz", "Content")

  console.log(response)
}

main()