// ausführbar zB mit "node js_frontend.js" in bash
// JS Version des python Codes im Kommentar

/*
import requests

url = "http://127.0.0.1:8000"

response = requests.delete(f"{url}/clear/")
print(response.json())

payload = {"username": "Testnutzer", "password": "Passwort"}

response = requests.post(f"{url}/users/", json=payload)
print(response.json())
*/


let url = "http://127.0.0.1:8000"
let payload = {"username": "JSnutzer", "password": "JSwort"}
let response = ""
let data = ""

response = await fetch(url+"/clear/", {
  method: "DELETE"
});

data = await response.json();
console.log(data);

response = await fetch(url+"/users/", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(payload)
});

data = await response.json();
console.log(data);