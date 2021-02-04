import requests

def login(email, password):
    session = requests.session()
    payload = {'email': email, 'password': password}
    # inside post is the url which is posted when logging in, this url is for my website
    response = session.post('https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=AIzaSyA4q2iXN4mC98wDVqt-St6FoHNzC_ymM2c', data=payload)
    print(response.status_code)
    # Print the HTML code of the page: print(response.content)


# email = "email"
# password = "password"
# login(email, password)
