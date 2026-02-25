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

//main()


async function login() {
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  const response = await login_user(username, password)
  if (response["login"]) {
    document.getElementById('login_signup_form').style.display = 'none';
    document.getElementById('boards').style.display = 'block';
    display_boards(response["id"])
  } else {
    // error meldung
  }
}

async function sign_up() {
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  console.log(username)
  console.log(password)

   const response = await register_user(username, password)
   if (response["status"] == "User erstellt") { // Besseren Check bei Gelgenheit
    document.getElementById('login_signup_form').style.display = 'none';
    document.getElementById('boards').style.display = 'block';
    display_boards(response["id"])
  } else {
    // error meldung
  }

}

async function display_boards(user_id) {
  const board_container = document.getElementById("board_container");
  board_container.innerHTML = "";

  // Add Board button
  const addBoardBtn = document.createElement("button");
  addBoardBtn.className = "btn_add_board";
  addBoardBtn.textContent = "+ Add Board";
  addBoardBtn.addEventListener("click", function () {
    // add board function
  });
  board_container.appendChild(addBoardBtn);

  const all_boards = []
  const response = ""
  try {
    response = await get_user_boards_notes(user_id)
  } catch {
    console.log("no notes")
  }


  if (response["eigene"]) {
    for (let i = 0; i < response["eigene"].length; i++) {
      all_boards.append(response["eigene"][i])
    }
  }
  if (response["geteilte"]) {
    for (let i = 0; i < response["geteilte"].length; i++) {
      all_boards.append(response["geteilte"][i])
    }
  }


  for (let i = 0; i < all_boards.length; i++) {
    
    const board_element = document.createElement("div");
    board_element.className = "board";
    board_element.dataset.boardId = all_boards[i].id;

    // Header: title + edit user button
    const header = document.createElement("div");
    header.className = "board_header";

    const title = document.createElement("h2");
    title.className = "board_title";
    title.textContent = all_boards[i].name;

    const edit_user_button = document.createElement("button");
    edit_user_button.className = "btn_edit_user";
    edit_user_button.textContent = "Edit User";
    edit_user_button.addEventListener("click", function () {
      // Add function edit User
    });

    header.appendChild(title);
    header.appendChild(edit_user_button);
    board_element.appendChild(header);

    // Element wo Notes reingeladen werden
    const notes_list = document.createElement("div");
    notes_list.className = "notes-list";

    // Notes aus Boards laden

    for (let j = 0; j < all_boards[i].notes.length; j++) {

      const note = document.createElement("div");
      note.className = "note";

      const note_title = document.createElement("div");
      note_title.className = "note_title";
      note_title.textContent = all_boards[i].notes[j].title;

      const note_content = document.createElement("div");
      note_content.className = "note_content";
      note_content.textContent = all_boards[i].notes[j].content;

      note.appendChild(note_title);
      note.appendChild(note_content);
      notesList.appendChild(note);

    }

    board_element.appendChild(notes_list);

    // Add Note button
    const add_note_button = document.createElement("button");
    add_note_button.className = "btn_add_note";
    add_note_button.textContent = "Add Note";
    add_note_button.addEventListener("click", function () {
      // Add note function
    });

    board_element.appendChild(add_note_button);

    board_container.appendChild(board_element);

  }
}