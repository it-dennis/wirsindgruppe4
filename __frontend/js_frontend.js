// ausführbar zB mit "node js_frontend.js" in bash
// JS Version des python Codes im Kommentar

let url = "http://127.0.0.1:8000"
let data = ""
logging = true

// Basiert auf alter api.py

async function create_note(board_id, title, content) {

  const payload = {"title": title, "content": content}

  const response = await fetch(`${url}/boards/${board_id}/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
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

async function create_user(username, password) {

  const payload = {"username": username, "password": password}

  const response = await fetch(url+"/users/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
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

async function create_board(user_id, name, user_id) {

  const payload = {"name": name, "user_id": user_id}

  const response = await fetch(`${url}/users/${user_id}/boards/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(board)
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

async function create_user_get_id() {
  create_user("JSUser", "Password")
  return 
}

// Code zum Testen muss in asyn Function gesteckt werden, damit await functioniert
// Sonst kann man zB die userID nicht auslesen

async function main() {
  clear_database()
  user = await create_user("JSUser", "Password")
  console.log(user["id"])
  
}

main()