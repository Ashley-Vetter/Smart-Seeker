import cv2
import cvzone
import numpy as np
import time

class TelloObjectRecognition:
    def __init__(self, drone, classFile, configPath, weightsPath, thres=0.70, nmsThres=0.2):
        # Load the class names
        self.classNames = []
        with open(classFile, 'rt') as f:
            self.classNames = f.read().split('\n')

        # Set thresholds
        self.thres = thres
        self.nmsThres = nmsThres

        # Load the detection model
        self.net = cv2.dnn_DetectionModel(weightsPath, configPath)
        self.net.setInputSize(320, 320)
        self.net.setInputScale(1.0 / 127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)

        # Use the drone instance passed from DroneControl
        self.drone = drone

    def detect_objects(self, img):
        # Detect objects in the frame
        classIds, confs, bbox = self.net.detect(img, confThreshold=self.thres, nmsThreshold=self.nmsThres)
        return classIds, confs, bbox

    import numpy as np

    def display_detections(self, img, classIds, confs, bbox):
        detected_objects = []  # List to hold detected object descriptions
        frame_height, frame_width = img.shape[:2]

        # Convert classIds, confs, and bbox to NumPy arrays if they are not already
        if isinstance(classIds, tuple):
            classIds = np.array(classIds)
        if isinstance(confs, tuple):
            confs = np.array(confs)
        if isinstance(bbox, tuple):
            bbox = np.array(bbox)

        if classIds is not None:
            for classId, conf, box in zip(classIds, confs, bbox):
                # Convert classId to string to get the class name
                className = self.classNames[classId - 1] if classId - 1 < len(self.classNames) else "Unknown"
                
                # Calculate the center position of the bounding box
                box_center_x = box[0] + box[2] // 2  # X center of the bounding box
                box_center_y = box[1] + box[3] // 2  # Y center of the bounding box
                
                # Create a description string for the detected object
                description = f"{className} is located at positions ({box_center_x}, {box_center_y})"
                detected_objects.append(description)

                # Draw detection box on the image
                cvzone.cornerRect(img, box)
                cv2.putText(img, f'{className.upper()} {round(conf * 100, 2)}%',
                            (box[0] + 10, box[1] + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)

        # Combine all detected objects into a single string
        all_detected_objects = ' | '.join(detected_objects) if detected_objects else "No objects detected."
        
        return all_detected_objects


    def start_recognition(self):
        print("Starting object recognition...")
        self.drone.camera(True)
        stop = False
        try:
            while stop!=True:
                # Capture frame from Tello's camera
                img = self.drone.getframe()
                classIds, confs, bbox = self.detect_objects(img)

                # Display detected objects and get the result
                detected_objects = self.display_detections(img, classIds, confs, bbox)
                if detected_objects != "No objects detected.":
                    print(f"Detected Objects: {detected_objects}")

                # Show the result frame
                cv2.imshow("Tello Object Detection", img)
                
                # Convert img to PNG format and ensure it's properly encoded
                success, encoded_img = cv2.imencode(".png", img)
                if success:
                    png_img = encoded_img.tobytes()  # Convert to bytes if needed for functions that need raw PNG data

                    # Pass the PNG image to the control_drone function
                    message = self.drone.control_drone(detected_objects, png_img)
                    if message != "":
                        print(message)
                        stop = True
                else:
                    print("Failed to convert image to PNG format.")
                    stop = True
                    break

                # Exit on 'q' key
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
                
        finally:
            cv2.destroyAllWindows()
            self.drone.camera(False)
        
    def start_depthMap(self):
        print("Starting depth map simulation...")
        self.drone.camera(True)
        
        try:
            while True:
                # Capture frame from Tello's camera
                img = self.drone.getframe()
                
                # Convert the frame to grayscale (simulate depth information)
                gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # Apply a color map to simulate a depth map
                depth_map = cv2.applyColorMap(gray_img, cv2.COLORMAP_JET)

                # Show the depth map
                cv2.imshow("Tello Depth Map Simulation", depth_map)

                # Exit on 'q' key
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
                self.drone.control_drone()
        finally:
            cv2.destroyAllWindows()
            self.drone.camera(False)


