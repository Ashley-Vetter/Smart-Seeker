import cv2
import cvzone
import numpy as np
import time

class TelloObjectRecognition:
    def __init__(self, drone, classFile, configPath, weightsPath, thres=0.70, nmsThres=0.2):
        self.classNames = []
        with open(classFile, 'rt') as f:
            self.classNames = f.read().split('\n')

        self.thres = thres
        self.nmsThres = nmsThres

        self.net = cv2.dnn_DetectionModel(weightsPath, configPath)
        self.net.setInputSize(320, 320)
        self.net.setInputScale(1.0 / 127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)

        self.drone = drone

    def detect_objects(self, img):
        classIds, confs, bbox = self.net.detect(img, confThreshold=self.thres, nmsThreshold=self.nmsThres)
        return classIds, confs, bbox

    import numpy as np

    def display_detections(self, img, classIds, confs, bbox):
        detected_objects = []  
        frame_height, frame_width = img.shape[:2]

        #sometimes the values comes in tuples, if it is in a tuple we convert it to a numpy array
        if isinstance(classIds, tuple):
            classIds = np.array(classIds)
        if isinstance(confs, tuple):
            confs = np.array(confs)
        if isinstance(bbox, tuple):
            bbox = np.array(bbox)

        if classIds is not None:
            for classId, conf, box in zip(classIds, confs, bbox):
                className = self.classNames[classId - 1] if classId - 1 < len(self.classNames) else "Unknown"
                
                #gets the center of the box containing the item
                box_center_x = box[0] + box[2] // 2  
                box_center_y = box[1] + box[3] // 2 
                
                #creates an appropriate description
                description = f"{className} is located at positions ({box_center_x}, {box_center_y})"
                detected_objects.append(description)

                cvzone.cornerRect(img, box)
                cv2.putText(img, f'{className.upper()} {round(conf * 100, 2)}%',
                            (box[0] + 10, box[1] + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)

        all_detected_objects = ' | '.join(detected_objects) if detected_objects else "No objects detected."
        
        return all_detected_objects

    #main logic
    def start_recognition(self):
        print("Starting object recognition...")
        self.drone.camera(True)
        stop = False
        try:
            while stop!=True:
                
                img = self.drone.getframe()
                #object detection start
                classIds, confs, bbox = self.detect_objects(img)

                detected_objects = self.display_detections(img, classIds, confs, bbox)
                if detected_objects != "No objects detected.":
                    print(f"Detected Objects: {detected_objects}")
                #object detection end

                #shows us the image
                cv2.imshow("Tello Object Detection", img)
                
                #tries to encode the image as a base64, if successful it does the drone control call else it dies
                success, encoded_img = cv2.imencode(".png", img)
                if success:
                    #encodes to bytes
                    png_img = encoded_img.tobytes()  

                    message = self.drone.control_drone(detected_objects, png_img)
                    #control_drone will return a message once its completed, it will then go down and land
                    if message != "":
                        print(message)
                        stop = True
                else:
                    print("Failed to convert image to PNG format.")
                    stop = True
                    break

                #press q to stop
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
                
        finally:
            cv2.destroyAllWindows()
            self.drone.camera(False)
        
    #does a depthmap, doesn't work as great since it just applies a filter
    def start_depthMap(self):
        print("Starting depth map simulation...")
        self.drone.camera(True)
        
        try:
            while True:
                img = self.drone.getframe()
                
                gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                depth_map = cv2.applyColorMap(gray_img, cv2.COLORMAP_JET)

                cv2.imshow("Tello Depth Map Simulation", depth_map)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
                self.drone.control_drone()
        finally:
            cv2.destroyAllWindows()
            self.drone.camera(False)


