var arDrone = require('ar-drone');
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