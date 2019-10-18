import wave
import sys
import math
import struct

obj = wave.open(sys.argv[1], 'r')
obj2 = wave.open(sys.argv[2], 'r')

signal_ori_left = 0.0
signal_err_left = 0.0
signal_ori_right = 0.0
signal_err_right = 0.0
max_error_left = 0
max_error_right = 0
SNR_left = 0
SNR_right = 0

for i in range(0, obj.getnframes()):
    #print("Frame:", i)
    ori = struct.unpack("<2h", obj.readframes(1))
    enc = struct.unpack("<2h", obj2.readframes(1))

    error_left = int(ori[0]) - int(enc[0])
    if error_left > max_error_left:
        max_error_left = error_left
    
    error_right = int(ori[1]) - int(enc[1])
    if error_right > max_error_right:
        max_error_right = error_right

    signal_ori_left += pow(int(ori[0]), 2)
    signal_err_left += pow(int(ori[0]) - int(enc[0]), 2)

    signal_ori_right += pow(int(ori[1]), 2)
    signal_err_right += pow(int(ori[1]) - int(enc[1]), 2)

if signal_err_left != 0:
    SNR_left = 10 * math.log10(signal_ori_left / signal_err_left)
else:
    SNR_left = 0

if signal_err_right != 0:
    SNR_right = 10 * math.log10(signal_ori_right / signal_err_right)
else:
    SNR_left = 0

print("SNR left:", SNR_left)
print("SNR right:", SNR_right)
print("SNR all:", (SNR_left + SNR_right ) / 2)
print("Max left:", max_error_left)
print("Max right:", max_error_right)
print("Max all:", (max_error_left + max_error_right) / 2)
obj.close()
obj2.close()
