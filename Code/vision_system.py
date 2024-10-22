import cv2
import numpy as np
import torch  
import time

class VisionSystem:
    def __init__(self, drone):
        self.drone = drone
        self.color_to_track = (0, 255, 0)
        self.tracking_start_time = None
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

    def start_video_stream(self, target_object=None):
        self.drone.streamon()
        lower_bound = np.array([40, 40, 40])  
        upper_bound = np.array([80, 255, 255])  

        while True:
            frame = self.drone.get_frame_read().frame
            frame = cv2.resize(frame, (720, 480))
            cv2.imshow("Tello Camera", frame)
            
            if target_object:
                if self.detect_objects(frame, target_object):
                    break  

            
            frame = self.detect_color(frame, lower_bound, upper_bound)
            cv2.imshow("Tello Camera", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
        self.drone.streamoff()

    def detect_objects(self, frame, target_object):
        
        results = self.model(frame)
        detections = results.pandas().xyxy[0]  
        print(detections) 
        
        if target_object in detections['name'].values:
            print(f"Target object '{target_object}' found!")
            
            #self.drone.hover(3)
            return True
        else:
            print(f"Target object '{target_object}' not found.")
            return False
    
    def detect_color(self, frame, lower_bound, upper_bound):
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            if self.tracking_start_time is None:
                self.tracking_start_time = time.time()
            elif time.time() - self.tracking_start_time >= 3:
                self.drone.move_forward(20)  
        else:
            self.tracking_start_time = None
        return frame