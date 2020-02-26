import cv2

cam = cv2.VideoCapture(0+cv2.CAP_DSHOW)

retval, frame = cam.read()

print(frame)
cv2.imshow('frame', frame)
 