import requests

def takeoff():
    requests.get('http://localhost:3000/takeoff')

def land():
    requests.get('http://localhost:3000/land')

def left():
    requests.get('http://localhost:3000/left')

def right():
    requests.get('http://localhost:3000/right')

def forward():
    requests.get('http://localhost:3000/forward')

def back():
    requests.get('http://localhost:3000/back')

def up():
    requests.get('http://localhost:3000/up')

def down():
    requests.get('http://localhost:3000/down')

def stop():
    requests.get('http://localhost:3000/stop')