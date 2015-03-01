/*liveplant tessel js controller file
Darren Cattle
github.com/liveplant
*/
var tessel = require('tessel');
var servo = require('servo-pca9685')
  .use(tessel.port['A']);
  
var position = 0;
setInterval(function () {
  servo.move(1, position);
  position = position == 0 ? 1 : 0;
}, 500);