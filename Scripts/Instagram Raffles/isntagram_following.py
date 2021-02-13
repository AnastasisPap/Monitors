from login import login

username = 'username'
password = 'password'
csrf_token, session_id = login(username, password)
print("csrf_token: ", csrf_token)
print("session_id: ", session_id)
