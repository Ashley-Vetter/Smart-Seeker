from djitellopy import Tello
import keyboard
from chat_interface import ChatInterface
import math
import re


manual = False
fullAutomatic = True
halfAutomatic = False
count = 0



class DroneControl:
    rotation = 0
    count = 0
    
    def __init__(self,chatbot):
        self.tello = Tello()
        self.chatter  = chatbot

    def connect(self):
        print("Attempting to connect to the drone...")
        self.tello.connect()
        print(f"Battery level: {self.tello.get_battery()}%")

    def takeoff(self):
        self.tello.takeoff()

    def land(self):
        self.tello.land()

    def move_up(self, distance=20):
        self.tello.move_up(distance)

    def move_down(self, distance=20):
        self.tello.move_down(distance)

    def move_forward(self, distance=75):
        self.tello.move_forward(distance)

    def move_back(self, distance=75):
        self.tello.move_back(distance)

    def rotate_clockwise(self, angle=45):
        self.rotation += angle
        self.tello.rotate_clockwise(angle)

    def rotate_counter_clockwise(self, angle=45):
        self.rotation -= angle
        self.tello.rotate_counter_clockwise(angle)
        
    def getframe(self):
        return self.tello.get_frame_read().frame
        
    def camera(self, camera_Status):
        if camera_Status == True:
            self.tello.streamon()
        else:
            self.tello.streamoff()
        
    def control_drone(self,logic = "", img = ""):
        responseMessage = ""
        if manual == True:
            if keyboard.is_pressed('t'):
                self.takeoff()
            elif keyboard.is_pressed('w'):
                self.move_forward()
            elif keyboard.is_pressed('s'):
                self.move_back()
            elif keyboard.is_pressed('a'):
                self.rotate_counter_clockwise()
            elif keyboard.is_pressed('d'):
                self.rotate_clockwise()
            elif keyboard.is_pressed('space'):
                self.move_up()
            elif keyboard.is_pressed('ctrl'):
                self.move_down()
            elif keyboard.is_pressed('l'):
                print("Landing...")
                self.land()
            elif keyboard.is_pressed('esc'):
                print("Exiting without landing...") 
        elif halfAutomatic == True:
            if self.tello.is_flying:
                if abs(self.rotation) == 360:
                    self.land()
                    self.rotation = 0
                    responseMessage = "I could not find the object, sorry"
                elif (logic == "No objects detected." or logic == ""):
                    self.rotate_clockwise(30)
                elif (logic != "No objects detected."):
                    success, message = self.chatter.checkIfImageContainsSearchKeyword(logic)
                    if success == True:
                        responseMessage = self.chatter.findObject(img)
                        self.land()
                    else:
                        self.rotate_clockwise(30)
                        
            elif self.tello.is_flying == False:
                self.takeoff()
        elif fullAutomatic == True:
            if self.count<=25:
                if self.tello.is_flying:
                    commandToExecute = self.chatter.autoSearch(img)
                    self.execute_command(commandToExecute)
                    self.count+=1
                            
                elif self.tello.is_flying == False:
                    self.takeoff()
                
            else:
                self.land()
                responseMessage = "sadge"
            
        return responseMessage
                
            
    def Emergency(self):
        try:
            if self.tello.get_battery() > 0 and self.tello.is_flying:  
                print("Emergency landing...")
                self.land()
            else:
                print("Drone is not in the air or battery is dead.")
        except Exception as e:
            print(f"Error during emergency landing: {e}")
            
            

    def execute_command(self, rough_string):
        command_map = {
            "up": self.move_up,
            "down": self.move_down,
            "forward": self.move_forward,
            "back": self.move_back,
            "clockwise": self.rotate_clockwise,
            "counter": self.rotate_counter_clockwise
        }

        numbers = re.findall(r'\d+', rough_string)
        
        distance_or_angle = int(numbers[0]) if numbers else None

        for keyword, command in command_map.items():
            if keyword in rough_string.lower():
                if distance_or_angle is not None:
                    command(distance_or_angle)  
                else:
                    command()  
                break  


                    
                
