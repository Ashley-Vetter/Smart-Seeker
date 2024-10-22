from drone_control import DroneControl
from vision_system import VisionSystem
from chat_interface import ChatInterface
from ObjectRecognition.Tello_OBJ_Recognition import Tello_OBJ_Recognition

def main():
    api_key = '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'
    drone_manager = DroneControl()
    vision_system = VisionSystem(drone_manager.tello)
    chat_interface = ChatInterface(api_key)
    obj = Tello_OBJ_Recognition.tello.Tello()

    drone_manager.connect()
    #drone_manager.streamon()
    #drone_manager.takeoff()
    #vision_system.start_video_stream()
    #vision_system.detect_objects() # - Not Working

if __name__ == "__main__":
    main()


# Current Error
# -------------------------------
## non-existing PPS 0 referenced
## non-existing PPS 0 referenced
## decode_slice_header error
## no frame!