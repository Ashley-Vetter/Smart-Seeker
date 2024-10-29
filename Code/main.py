from drone_control import DroneControl
from ObjectRecognition.TelloObjectRecognition import TelloObjectRecognition
from chat_interface import ChatInterface
<<<<<<< Updated upstream

def main():
    api_key = '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'
    drone_manager = DroneControl()
    vision_system = VisionSystem(drone_manager.tello)
    chat_interface = ChatInterface(api_key)

    drone_manager.connect()
    #drone_manager.takeoff()
    vision_system.start_video_stream()
    vision_system.detect_objects()
=======

def findObject(chatInterface):
    try:
        # Initialize DroneControl to manage the drone
        drone_manager = DroneControl(chatInterface)

        # Connect to the drone
        drone_manager.connect()

        # Define the paths to the object detection files
        classFile = 'Code/ObjectRecognition/ss.names'
        configPath = 'Code/ObjectRecognition/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
        weightsPath = 'Code/ObjectRecognition/frozen_inference_graph.pb'

        # Initialize TelloObjectRecognition with the shared drone instance
        drone_recognition = TelloObjectRecognition(drone_manager, classFile, configPath, weightsPath)
        
        # Start the object recognition process
        drone_recognition.start_recognition()
        #drone_recognition.start_depthMap() ###eeeeeeeeeeeeeeeeeeeeeeeeeeh
    except Exception as e:
        print(e)
        drone_manager.Emergency()

def main():
    # Create an instance of ChatInterface
    chat_interface = ChatInterface(api_key="your_api_key_here")

    while True:
        user_input = input("Good day, can I assist in helping you find something: ")
        
        # Call the method using the instance
        chat_interface.findSimiliarKeywords(user_input)
        
        findObject(chat_interface)
        print("Search Done")

>>>>>>> Stashed changes

if __name__ == "__main__":
    main()
