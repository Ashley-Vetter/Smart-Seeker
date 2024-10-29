from drone_control import DroneControl
from ObjectRecognition.TelloObjectRecognition import TelloObjectRecognition
from chat_interface import ChatInterface

def findObject(chatInterface):
    try:
        drone_manager = DroneControl(chatInterface)

        drone_manager.connect()

        classFile = 'Code/ObjectRecognition/ss.names'
        configPath = 'Code/ObjectRecognition/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
        weightsPath = 'Code/ObjectRecognition/frozen_inference_graph.pb'

        drone_recognition = TelloObjectRecognition(drone_manager, classFile, configPath, weightsPath)
        
        drone_recognition.start_recognition()
        #drone_recognition.start_depthMap() ###eeeeeeeeeeeeeeeeeeeeeeeeeeh
    except Exception as e:
        print(e)
        drone_manager.Emergency()

def main():
    chat_interface = ChatInterface(api_key="your_api_key_here")

    while True:
        user_input = input("Good day, can I assist in helping you find something: ")
        
        chat_interface.findSimiliarKeywords(user_input)
        
        findObject(chat_interface)
        print("Search Done")


if __name__ == "__main__":
    main()
