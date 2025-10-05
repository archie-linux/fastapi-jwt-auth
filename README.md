### JWT-Based Authentication API

- python -m venv myvenv
- source myvenv/bin/activate
- pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt] pydantic email-validator
- uvicorn main:app --reload


### Testing the API

- Register a User

<pre>
curl -X 'POST' 'http://127.0.0.1:8000/register' -H 'Content-Type: application/json' -d '{"username": "testuser", "password": "testpassword"}'

{"message":"User registered successfully"}

DB File: cat users.json

{
    "users": [
        {
            "username": "testuser",
            "password": "$2b$12$EQoe2btTi/nuYAQf3PriKOQFQmoKchYgTk9oLMUX6fSUvgh7SdPSC"
        }
    ]
}

</pre>

- Login & Get Token

<pre>
1. Valid User

curl -X 'POST' 'http://127.0.0.1:8000/token' -H 'Content-Type: application/json' -d '{"username": "testuser", "password": "testpassword"}'

{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsInJvbGUiOiJ1c2VyIiwiZXhwIjoxNzM5ODAzNjUxfQ.LgQ1OMa838IDgeCLPYOQKGQ-PhVwIaeESCpavCBga-k","token_type":"bearer"}

2. Invalid User

curl -X 'POST' 'http://127.0.0.1:8000/token' -H 'Content-Type: application/json' -d '{"username": "testuser1", "password": "testpassword"}'

{"detail":"Invalid credentials"}

3. Invalid Password

curl -X 'POST' 'http://127.0.0.1:8000/token' -H 'Content-Type: application/json' -d '{"username": "testuser", "password": "testpassword1"}'

{"detail":"Invalid credentials"}
</pre>

- Access protected resources.

<pre>
1. Valid Token

curl -X 'GET' 'http://127.0.0.1:8000/protected' -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsInJvbGUiOiJ1c2VyIiwiZXhwIjoxNzM5ODAzNjUxfQ.LgQ1OMa838IDgeCLPYOQKGQ-PhVwIaeESCpavCBga-k'

{"message":"Protected data","access_token":{"sub":"testuser","role":"user","exp":1739803651}}

2. Invalid Token

 curl -X 'GET' 'http://127.0.0.1:8000/protected' -H 'Authorization: Bearer wildwest'

{"detail":"Invalid token"}
</pre>


- API Logs

<pre>
(myvenv) MacBook-Air-2:fastapi-jwt-auth anish$ uvicorn main:app --reload
INFO:     Will watch for changes in these directories: ['/Users/anish/anpa6841/github-projects/fastapi-jwt-auth']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [93564] using StatReload
INFO:     Started server process [93584]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
(trapped) error reading bcrypt version
Traceback (most recent call last):
  File "/Users/anish/anpa6841/github-projects/fastapi-jwt-auth/myvenv/lib/python3.10/site-packages/passlib/handlers/bcrypt.py", line 620, in _load_backend_mixin
    version = _bcrypt.__about__.__version__
AttributeError: module 'bcrypt' has no attribute '__about__'
INFO:     127.0.0.1:56197 - "POST /register HTTP/1.1" 200 OK
INFO:     127.0.0.1:56217 - "POST /token HTTP/1.1" 200 OK
INFO:     127.0.0.1:56234 - "GET /protected HTTP/1.1" 200 OK
INFO:     127.0.0.1:56322 - "POST /token HTTP/1.1" 401 Unauthorized
INFO:     127.0.0.1:56346 - "POST /token HTTP/1.1" 401 Unauthorized
INFO:     127.0.0.1:56370 - "GET /protected HTTP/1.1" 401 Unauthorized
</pre>



### Testing Role-Based Access Control (RBAC)

- Register an Admin User

<pre>
curl -X 'POST' 'http://127.0.0.1:8000/register' -H 'Content-Type: application/json' -d '{"username": "admin", "password": "adminpass"}'

{"message":"User registered successfully"}

cat users.json

{
    "users": [
        {
            "username": "admin",
            "password": "$2b$12$k80Y9jWJAdm89BU.WDuK9.mLSkVdSZ0BZyMeoq4HrjooLcehhzHeu",
            "role": "user"
        }
    ]
}

(Manually change the role in users.json to "admin")
</pre>

- Login & Get Token

<pre>
curl -X 'POST' 'http://127.0.0.1:8000/token' -H 'Content-Type: application/json' -d '{"username": "admin", "password": "adminpass"}'

{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTczOTgwMzIzMH0.GhUuWER8tWJqfKaBrzxh3k45jljJe0jUtnOA-0iAIqs","token_type":"bearer"}

</pre>

- Access Admin Route (Allowed)

<pre>
curl -X 'GET' 'http://127.0.0.1:8000/admin' -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTczOTgwMzIzMH0.GhUuWER8tWJqfKaBrzxh3k45jljJe0jUtnOA-0iAIqs'

{"message":"Welcome, Admin!"}
</pre>

- Access Admin Route as a Normal User (Forbidden)


<pre>
curl -X 'GET' 'http://127.0.0.1:8000/admin' -H 'Authorization: Bearer USER_ACCESS_TOKEN

{"detail":"Invalid token"}
</pre>


- App Logs

<pre>
(myvenv) MacBook-Air-2:fastapi-jwt-auth anish$ uvicorn main:app --reload
INFO:     Will watch for changes in these directories: ['/Users/anish/anpa6841/github-projects/fastapi-jwt-auth']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [2146] using StatReload
INFO:     Started server process [2163]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
(trapped) error reading bcrypt version
Traceback (most recent call last):
  File "/Users/anish/anpa6841/github-projects/fastapi-jwt-auth/myvenv/lib/python3.10/site-packages/passlib/handlers/bcrypt.py", line 620, in _load_backend_mixin
    version = _bcrypt.__about__.__version__
AttributeError: module 'bcrypt' has no attribute '__about__'
INFO:     127.0.0.1:56838 - "POST /register HTTP/1.1" 200 OK
INFO:     127.0.0.1:56945 - "POST /token HTTP/1.1" 200 OK
INFO:     127.0.0.1:57009 - "GET /admin HTTP/1.1" 200 OK
INFO:     127.0.0.1:57020 - "GET /admin HTTP/1.1" 401 Unauthorized
</pre>
