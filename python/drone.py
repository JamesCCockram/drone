import requests

def takeoff():
    requests.get('http://localhost:3000/takeoff')

def land():
    requests.get('http://localhost:3000/land')

takeoff()
land()