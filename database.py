import json
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def read_db():
    with open("users.json", "r") as file:
        return json.load(file)

def write_db(data):
    with open("users.json", "w") as file:
        json.dump(data, file, indent=4)

def get_user(username):
    users = read_db()["users"]
    return next((user for user in users if user["username"] == username), None)

def add_user(username, password):
    users = read_db()
    hashed_password = pwd_context.hash(password)
    users["users"].append({"username": username, "password": hashed_password})
    write_db(users)
