from drone_control import DroneControl
from vision_system import VisionSystem
from chat_interface import ChatInterface

def main():
    api_key = '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'
    drone_manager = DroneControl()
    vision_system = VisionSystem(drone_manager.tello)
    chat_interface = ChatInterface(api_key)

    drone_manager.connect()
    #drone_manager.takeoff()
    vision_system.start_video_stream()
    vision_system.detect_objects()

if __name__ == "__main__":
    main()
