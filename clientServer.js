var express = require('express'); //function handler for server
var app = express();
var http = require('http').Server(app);
var commmandEndpoint = '';
const port = 4200;

app.use(express.static(__dirname + '/public'));
const request = require('request');
const SerialPort = require('serialport');
//opnes port to arduino
const IRPort = new SerialPort('COM3', {baudRate: 9600});
const Readline = SerialPort.parsers.Readline;

const parser = new Readline('\n');
IRPort.pipe(parser);
const {spawn} = require('child_process');
var trackingString = '';
var entryLength = 0;
var totalLength = 0;
global.outputString = '';

function commandRequest(command) {
    request.post(commmandEndpoint, {
        json: {
            todo: command
        }
    }, (error, res, body) => {
        if (error) {
            console.error(error)
            return
        }
        console.log(`statusCode: ${res.statusCode}`)
        console.log(body)
    })
}

app.use((req,res,next)=>{
 console.log(req.path);  
next();
});

parser.on('data', function(data){
    dataString = data.replace(/(\r\n|\n|\r)/gm,"");
    if(dataString == 'fly' || dataString == 'feed' || dataString == 'land') {
        commandRequest(dataString);
    } else if (dataString == "feedVoice") {
        commandRequest('feed');
    }
});

//defines a route handler and sends file
app.get('/', function(req,res){ 
	res.sendFile(__dirname + '/public/Home.html');
});

app.post('/fly',function(req,res){
    commandRequest('fly');
    res.sendFile(__dirname + '/public/Running.html');
});

app.post('/feed',function(req,res){
    commandRequest('feed');
	res.sendFile(__dirname + '/public/Running.html');
});

app.post('/land',function(req,res){
    commandRequest('land');
	res.sendFile(__dirname + '/public/Home.html');
});

app.post('/face',function(req,res){
    res.sendFile(__dirname + '/public/Running.html');
    // spawn and collect data from script
    const python = spawn('python', ['facialTracking.py']);
    python.stdout.on('data', function (data) {
        data = data.toString().replace(/(\r\n|\n|\r)/gm,"");
        entryLength = data.length;
        trackingString += data;
    });
    python.on('close', (code) => {
        totalLength = trackingString.length;
        console.log(`child process exited with code ${code}`);
        outputString = trackingString.substring(totalLength-4,totalLength);
        outputString = outputString.replace(/\d+/g,'');
        console.log(outputString);
        commandRequest(outputString);
      });

});


http.listen(port,function()
{
	console.log('listening on :', port);
});

