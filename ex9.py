import numpy 
import math
import cv2
import sys

original = cv2.VideoCapture(sys.argv[1])
contrast = cv2.VideoCapture(sys.argv[2])
snr = 0.0
max_error = 0.0

while original.isOpened() and contrast.isOpened():
    ret, frame = original.read()
    ret2, frame2 = contrast.read()

    if cv2.waitKey(1) & 0xFF == ord('q') or ret == False:
        break

    error = numpy.mean(frame - frame2)
    if error > max_error:
        max_error = error

    ori = math.sqrt(numpy.mean(frame) ** 2)
    mse = math.sqrt(error ** 2)

    if mse != 0:
        snr += 10 * math.log10(ori / mse)


print("SNR:", snr)
print("Max error:", max_error)
original.release()
contrast.release()
cv2.destroyAllWindows()
