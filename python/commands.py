import requests

def takeoff():
    r = requests.get('http://localhost:3000/takeoff')
    print(r.text)

def land():
    r = requests.get('http://localhost:3000/land')
    print(r.text)

def left():
    r = requests.get('http://localhost:3000/left')
    print(r.text)

def right():
    r = requests.get('http://localhost:3000/right')
    print(r.text)

def forward():
    r = requests.get('http://localhost:3000/forward')
    print(r.text)

def back():
    r = requests.get('http://localhost:3000/back')
    print(r.text)

def up():
    r = requests.get('http://localhost:3000/up')
    print(r.text)

def down():
    r = requests.get('http://localhost:3000/down')
    print(r.text)

def stop():
    r = requests.get('http://localhost:3000/stop')
    print(r.text)