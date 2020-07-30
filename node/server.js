const express = require('express')
const app = express()
const port = 3000

var arDrone = require('ar-drone');
var client = arDrone.createClient();

//Make drone takeoff
app.get('/takeoff', function(req, res){
  client.takeoff()
})

//Make drone land
app.get('/land', function(req, res){
  client.land()
})


//Start ExpressJS server
app.listen(port, () => console.log(`Example app listening at http://localhost:${port}`))


/*
var PaVEParser = require('ar-drone/lib/video/PaVEParser');
var output = require('fs').createWriteStream('./vid.h264');

var video = arDrone.createClient().getVideoStream();
var parser = new PaVEParser();

parser
  .on('data', function(data) {
    output.write(data.payload);
  })
  .on('end', function() {
    output.end();
  });

video.pipe(parser);
*/