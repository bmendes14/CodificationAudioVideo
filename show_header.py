import argparse
import wave
import os.path

parser = argparse.ArgumentParser()
parser.add_argument("input", help="set input file")

args = parser.parse_args()

def main():
	# Input validation
	if not args.input:
		print ("Input file not set!")
		return

	# Open source file
	with wave.open(args.input, 'rb') as file:
		# Read input file params
		nchannels, sampwidth, framerate, nframes, comptype, compname =  file.getparams()

		bit_depth = sampwidth/nchannels*8

		if bit_depth % 8 != 0:
			print('Bit depth is not a multiple of 8. Ma come?!')
			return

		bit_depth = int(bit_depth)
		print("Input file:\t", args.input)
		print("Bit-depth:\t", bit_depth)
		print("No Channels:\t", nchannels)
		print("Sample Width:\t", sampwidth)
		print("Framerate:\t", framerate)
		print("No frames:\t", nframes)
		print("Comp Type:\t", comptype)
		print("Comp Name:\t", compname)


main()