from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib
import json
from tello import Tello
import sys
from datetime import datetime
import time

hostAddress = ""
hostPort = 8000
#global object for interfacing with Tello drone
tello = Tello()

def commandExecution(maneuver):
    # start_time = str(datetime.now()) #prob wont need
    file_name = maneuver
    f = open(file_name, "r")
    commands = f.readlines()
    global tello
    for command in commands:
        if command != '' and command != '\n':
            command = command.rstrip()

            if command.find('delay') != -1:
                sec = float(command.partition('delay')[2])
                print('delay %s' % sec)
                time.sleep(sec)
                pass
            else:
                tello.send_command(command)

class RequestHandler(BaseHTTPRequestHandler):
    
    def send_response(self, code, message=None):
        self.log_request(code)
        self.send_response_only(code)
        self.send_header('Server','python server')     
        self.send_header('Date', self.date_time_string())
        self.end_headers()  

    def do_POST(self):
        """ response for a POST """
        content_length = int(self.headers['Content-Length'])
        value = self.rfile.read(content_length)
        action = json.loads(value)
        # print(action["todo"])
        if action["todo"] == "fly" :
            print("Taking Off, Please Stay Clear")
            commandExecution("maneuver1.txt")
        elif action["todo"] == "feed":
            print("Performing Feeding Routine")
            commandExecution("maneuver2.txt")
        elif action["todo"] == "land":
            print("Landing Drone")
            commandExecution("maneuver3.txt")

def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = (hostAddress, hostPort)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == '__main__':
    run(handler_class=RequestHandler)