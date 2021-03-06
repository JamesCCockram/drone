const express = require('express')
const app = express()
const port = 3000

var arDrone = require('ar-drone');
var client = arDrone.createClient();

//Make drone takeoff
app.get('/takeoff', function(req, res){
  client.takeoff()
  res.send('Drone has Taken Off!')
})

//Make drone land
app.get('/land', function(req, res){
  client.land()
  res.send('Drone has Landed!')
})

//Make drone go left
app.get('/left', function(req, res){
  client.left(0.25)
  res.send('Drone is moving to the left')
})

//Make drone go right
app.get('/right', function(req, res){
  client.right(0.25)
  res.send('Drone is moving to the right')
})

//Make drone go forward
app.get('/forward', function(req, res){
  client.front(0.25)
  res.send('Drone is moving forward')
})

//Make drone go back
app.get('/back', function(req, res){
  client.back(0.25)
  res.send('Drone is moving back')
})

//Make drone go up
app.get('/up', function(req, res){
  client.up(0.25)
  res.send('Drone is going up')
})

//Make drone go down
app.get('/down', function(req, res){
  client.down(0.25)
  res.send('Drone is going down')
})

//Make drone stop
app.get('/stop', function(req, res){
  client.stop()
  res.send('Drone has Stopped!')
})

//Start ExpressJS server
app.listen(port, () => console.log(`Example app listening at http://localhost:${port}`))