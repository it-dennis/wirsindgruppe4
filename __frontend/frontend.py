import requests

# URL definieren
url = "http://127.0.0.1:8000/"

print("Get Root:")
response = requests.get(url)
print(response.json())