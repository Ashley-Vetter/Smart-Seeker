from drone_control import DroneControl
from ObjectRecognition.TelloObjectRecognition import TelloObjectRecognition
from chat_interface import ChatInterface

#The main logic, essentially it creates the drone and the object recognition objects and starts the recognitions
def findObject(chatInterface):
    try:
        drone_manager = DroneControl(chatInterface)

        drone_manager.connect()

        classFile = 'Code/ObjectRecognition/ss.names'
        configPath = 'Code/ObjectRecognition/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
        weightsPath = 'Code/ObjectRecognition/frozen_inference_graph.pb'

        drone_recognition = TelloObjectRecognition(drone_manager, classFile, configPath, weightsPath)
        
        drone_recognition.start_recognition()
        #drone_recognition.start_depthMap() ###This doesn't really work as intended, still looks kinda cool
    except Exception as e:
        print(e)
        #does an emergency landing in case there is issues
        drone_manager.Emergency()

def main():
    chat_interface = ChatInterface(api_key="your_api_key_here")#add your API key here

    while True:
        user_input = input("Good day, can I assist in helping you find something: ")
        
        chat_interface.findSimiliarKeywords(user_input)#finds any similiar keywords the user might have listed
        
        findObject(chat_interface)
        print("Search Done")


if __name__ == "__main__":
    main()
