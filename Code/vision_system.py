import cv2

class VisionSystem:
    def __init__(self, drone):
        self.drone = drone

    def start_video_stream(self):
        self.drone.streamon()
        while True:
            frame = self.drone.get_frame_read().frame
            frame = cv2.resize(frame, (720, 480))
            cv2.imshow("Tello Camera", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
        self.drone.streamoff()
