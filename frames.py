
import cv2

capture = cv2.VideoCapture('tomate.mp4')
capturas = 0
path = 'D:/Felipe/Codigo/Img/'
max_frames = 500
frame_count = 0

while (capture.isOpened() and frame_count < max_frames):
    ret, frame = capture.read()
    if (ret == True):
        cv2.imwrite(path + 'IMG_%04d.jpg' % capturas, frame)    
        capturas += 1
        frame_count += 1
    else:
        break

capture.release()
cv2.destroyAllWindows()