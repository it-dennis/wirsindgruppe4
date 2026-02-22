from passlib.context import CryptContext

#Passwort anlegen und verifizieren, passlib sorgt dafür, dass die Passwörter sicher gehasht werden 
#und nicht im Klartext in der Datenbank liegen. 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hilfsfunktionen für Passwort-Hashing und -Verifizierung
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
