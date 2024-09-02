from drone_control import DroneControl
from vision_system import VisionSystem
from chat_interface import ChatInterface

def main():
    api_key = 'sk-XNyK3X5f1Z1V1JhiwQva--oyHGVtqgFU7kXrlCABzaT3BlbkFJ09eRS0fmY65c_7uqObTokzeHOpfD3G99FaoYuhGb4A'
    drone_manager = DroneControl()
    vision_system = VisionSystem(drone_manager.tello)
    chat_interface = ChatInterface(api_key)

    drone_manager.connect()
    while True:
        prompt = "Please provide a drone command: "
        instruction = chat_interface.get_instruction(prompt)
        print(f"Command received: {instruction}")
        # We can add more conditions here based on the instructions
        if instruction == "take off":
            drone_manager.takeoff()
        elif instruction == "land":
            drone_manager.land()

if __name__ == "__main__":
    main()
