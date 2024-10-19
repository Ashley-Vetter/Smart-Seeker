import cv2
import numpy as np
import torch  
import time

class VisionSystem:
    def __init__(self, drone):
        self.drone = drone
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

    def start_video_stream(self, target_object=None):
        self.drone.streamon()
        while True:
            frame = self.drone.get_frame_read().frame
            frame = cv2.resize(frame, (720, 480))
            cv2.imshow("Tello Camera", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
        self.drone.streamoff()

    def detect_objects(self, frame, target_object):
        
        results = self.model(frame)
        detections = results.pandas().xyxy[0]  

        
        if target_object in detections['name'].values:
            print(f"Target object '{target_object}' found!")
            
            self.drone.hover(3)
            return True
        else:
            print(f"Target object '{target_object}' not found.")
            return False