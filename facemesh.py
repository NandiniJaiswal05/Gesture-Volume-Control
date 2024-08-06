import cv2
import mediapipe as mp
import time

class FaceMeshDetector:
    def __init__(self, max_num_faces=3, thickness=1, circle_radius=1):
        self.cap = cv2.VideoCapture(0)
        self.pTime = 0

        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(max_num_faces=max_num_faces)
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=thickness, circle_radius=circle_radius)

    def detect_face_mesh(self):
        while True:
            r, frame = self.cap.read()
            if not r:
                break

            f_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.faceMesh.process(f_rgb)
            if results.multi_face_landmarks:
                for faceLms in results.multi_face_landmarks:
                    self.mpDraw.draw_landmarks(frame, faceLms, self.mpFaceMesh.FACEMESH_CONTOURS, self.drawSpec, self.drawSpec)
                    for id, lm in enumerate(faceLms.landmark):
                        fh, fw, fc = frame.shape
                        x, y = int(lm.x * fw), int(lm.y * fh)
                        # print(id, x, y)

            cTime = time.time()
            fps = 1 / (cTime - self.pTime)
            self.pTime = cTime
            cv2.putText(frame, f'FPS:{int(fps)}', (20, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)
            cv2.imshow("FaceMesh", frame)

            if cv2.waitKey(25) & 0xff == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    detector = FaceMeshDetector()
    detector.detect_face_mesh()
