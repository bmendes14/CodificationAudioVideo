import argparse
import wave
import os.path

parser = argparse.ArgumentParser()


parser.add_argument("input", help="set input file")
parser.add_argument("output", help="set output file")

args = parser.parse_args()

def main():
	# Input validation
	if not args.input:
		print ("Input file not set!")
		return

	if not args.output:
		print ("Output file not set!")
		return

	if os.path.isfile(args.output):
		print('Output file exists. Deleting...')
		os.remove(args.output)

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
		print("No Channels:\t", nchannels)
		print("Sample Width:\t", sampwidth)
		print("Framerate:\t", framerate)
		print("No frames:\t", nframes)
		print("Comp Type:\t", comptype)
		print("Comp Name:\t", compname)
		print("Bit-depth:\t", bit_depth)

		# Open target file with same params (conversion of channel or similar would be here)
		output_file = wave.open(args.output, 'wb')
		output_file.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname ))
		data = file.readframes(1)

		counter = 0
		while data != b'':
			print (str.format('\rPercentage: {:.1f}%', counter*1.0/nframes*100.0), end='')
			counter += 1
			output_file.writeframes(data)
			data = file.readframes(1)

		output_file.close()

main()
	
