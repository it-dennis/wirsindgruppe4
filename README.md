# Projektname: Backend-Gruppenarbeit

Eine kurze Beschreibung eures Backends (wird ergänzt, sobald das Thema feststeht).

## 🚀 Projekt-Status

- [x] Repository erstellt
- [x] Dokumentation initialisiert
- [ ] Architektur-Design
- [ ] API-Implementierung

## 🛠 Tech Stack (Beispiele)

* **Sprache:** [z.B. JavaScript / TypeScript]
* **Framework:** [z.B. Express.js / FastAPI]
* **Datenbank:** [z.B. PostgreSQL / MongoDB]

## 📥 Installation & Setup

Um das Projekt lokal auszuführen, folge diesen Schritten:

1. Repository klonen:

```bash
git clone https://github.com/it-dennis/wirsindgruppe4.git


```

---

cd frontend

python3 -m venv venv

source .venv/bin/activate

pip3 install -r requirements.txt

---

Neues Terminal:

cd backend

python3 -m venv venv

source .venv/bin/activate

pip3 install -r requirements.txt

TEAM

[Muhammed] (@MKaracam90)
[Felix] (@flxnsn)
[Patrick] (@skpatrickue-73)
[Dennis] (@it-dennis)

---

## fastapi install

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip
pip install jupyter ipykernel

python -m ipykernel install --user --name venv --display-name "Python (venv)"

pip install requests

fastapi dev main.py = startet

control + c = beenden

---

Passwortbereich einrichten bcrypt:

pip install bcrypt

---

## Probleme beim pullen?

Mit diesen Commands überschreibt man alle lokalen Änderungen! Also nur für den Notfall!

git fetch origin  
git reset --hard origin/main

## fastapi install

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip
pip install jupyter ipykernel

pip install "fastapi[standard]"

pip install pydantic

python -m ipykernel install --user --name venv --display-name "Python (venv)"

pip install requests

fastapi dev main.py = startet

---

## Frontend und Backend lokal hosten

Im ordner des Backends:  
fastapi dev main.py  

im Ordener des Frontends:  
python3 -m http.server 8080  

Dann im Browser:  
http://localhost:8080/index.html  
