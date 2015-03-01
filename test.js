var port = require('tessel').port.GPIO,
    pin = port.pwm[0];
port.pwmFrequency(50);
console.log(pin);
pin.pwmDutyCycle(0.6);