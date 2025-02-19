# import cv2
#
#
#
# cameras = []
#
# for i in range(10):
#     cap = cv2.VideoCapture(i)
#     if cap.isOpened():
#         print(i)
#         cameras.append(i)
#         cap.release()
#
# if cameras:
#     print(f"Connected cameras: {cameras}")
# else:
#     print("No cameras detected.")

import pygame
import time

pygame.mixer.init()
pygame.mixer.music.load(r"C:\Users\petro\Downloads\file_example_MP3_700KB.mp3")
pygame.mixer.music.play()
time.sleep(10)