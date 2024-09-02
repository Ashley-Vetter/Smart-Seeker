from djitellopy import Tello

class DroneControl:
    def __init__(self):
        self.tello = Tello()

    def connect(self):
        print("Attempting to connect to the drone...")
        self.tello.connect()
        print(f"Battery level: {self.tello.get_battery()}%")

    def takeoff(self):
        self.tello.takeoff()

    def land(self):
        self.tello.land()

    def move_up(self, distance):
        self.tello.move_up(distance)

    def move_down(self, distance):
        self.tello.move_down(distance)

    def move_forward(self, distance):
        self.tello.move_forward(distance)

    def move_back(self, distance):
        self.tello.move_back(distance)

    def rotate_clockwise(self, angle):
        self.tello.rotate_clockwise(angle)

    def rotate_counter_clockwise(self, angle):
        self.tello.rotate_counter_clockwise(angle)
