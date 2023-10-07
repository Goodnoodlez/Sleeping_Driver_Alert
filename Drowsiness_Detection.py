import dlib
import sys
import cv2
import time
import numpy as np
from scipy.spatial import distance as dist
from threading import Thread
import queue
import pygame

# Pygame initialization
pygame.init()

FACE_DOWNSAMPLE_RATIO = 1.5
RESIZE_HEIGHT = 460

thresh = 0.27
modelPath = "models/shape_predictor_70_face_landmarks.dat"
sound_path = "alarm.wav"

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(modelPath)

leftEyeIndex = [36, 37, 38, 39, 40, 41]
rightEyeIndex = [42, 43, 44, 45, 46, 47]

blinkCount = 0
drowsy = 0
state = 0
blinkTime = 0.15 #150ms
drowsyTime = 1.5  #1200ms
ALARM_ON = False
GAMMA = 1.5
threadStatusQ = queue.Queue()

invGamma = 1.0/GAMMA
table = np.array([((i / 255.0) ** invGamma) * 255 for i in range(0, 256)]).astype("uint8")

# ... [rest of your auxiliary functions]

# For playing the alarm sound using pygame
def soundAlert(path, threadStatusQ):
    pygame.mixer.music.load(path)
    while True:
        if not threadStatusQ.empty():
            FINISHED = threadStatusQ.get()
            if FINISHED:
                pygame.mixer.music.stop()
                break
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely

def main():
    capture = cv2.VideoCapture(0)

    # Initial frame capture to get the size for pygame screen
    ret, frame = capture.read()
    if not ret:
        print("Error capturing frame.")
        return

    # Set up a pygame screen (window) for display
    screen = pygame.display.set_mode((frame.shape[1], frame.shape[0]))
    pygame.display.set_caption("Blink Detection Demo")

    # ... [rest of your code before the while loop]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            # Handle keypresses with pygame
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    state = 0
                    drowsy = 0
                    ALARM_ON = False
                    threadStatusQ.put(not ALARM_ON)
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

        # Continuously read frames from the capture device
        ret, frame = capture.read()
        if not ret:
            print("Failed to grab frame.")
            break

        try:
            # ... [rest of your code in the main loop]

            # Convert the OpenCV image format (BGR) to RGB for pygame
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert the OpenCV image to a format pygame can use
            frame_surf = pygame.surfarray.make_surface(frame_rgb.swapaxes(0,1))

            # Draw the frame onto the pygame window
            screen.blit(frame_surf, (0, 0))
            pygame.display.flip()

        except Exception as e:
            print(e)

    capture.release()

if __name__ == "__main__":
    main()
