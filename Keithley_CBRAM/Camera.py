import cv2

cam = cv2.VideoCapture(-1)

retval, frame = cam.read()

print(frame)
cv2.imshow('frame', frame)
 