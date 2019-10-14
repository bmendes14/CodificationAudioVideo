import argparse
import wave
import os.path

parser = argparse.ArgumentParser()

parser.add_argument("input", help="set input file")
parser.add_argument("output", help="set output file")

args = parser.parse_args()
# TODO: Make reduction factor a program parameter

def quantize_bit_sequence(data):
	bit_sequence = ''
	for i, byte in zip(range(0, len(data)), data):
		print(str.format('\rProcessing... {:.2f}', i/len(data) * 100), end='')

		nb = byte >> 2
		# Remove '0b' from string
		bin_repr = bin(nb)[2:]

		# Make sure binary sequence representation is 6-bit length
		if len(bin_repr) < 6:
			for j in range(0, 6-len(bin_repr)):
				bin_repr = '0' + bin_repr

		elif len(bin_repr) > 6:
			bin_repr = bin_repr[0:-2]

		# Concatenate (probably should come up with a better way to concatenate)
		bit_sequence += bin_repr

	print('\n', bit_sequence[0:10])

	# TODO: Why BigEndian?! WAVE Data is in little endian!
	# Note: It does not work with byteorder=little, the output wave's data will not be correct
	bytes = int(bit_sequence, 2).to_bytes((len(bit_sequence) + 7) // 8, byteorder='big')
	return bytes

def main():
	# Input validation
	if not args.input:
		print("Input file not set!")
		return

	if not args.output:
		print("Output file not set!")
		return

	if os.path.isfile(args.output):
		print('Output file exists. Deleting...')
		os.remove(args.output)

	# Open source file
	with wave.open(args.input, 'rb') as file:
		# Read input file params
		nchannels, sampwidth, framerate, nframes, comptype, compname = file.getparams()
		bit_depth = sampwidth/nchannels*8

		if bit_depth % 8 != 0:
			print('Bit depth is not a multiple of 8. Ma come?!')
			return

		bit_depth = int(bit_depth)
		print("Input file:\t", args.input)
		print("Output file:\t", args.output)
		print("No Channels:\t", nchannels)
		print("Sample Width:\t", sampwidth)
		print("Framerate:\t", framerate)
		print("No frames:\t", nframes)
		print("Comp Type:\t", comptype)
		print("Comp Name:\t", compname)
		print("Bit-depth:\t", bit_depth)

		# Open target file with same params (this is just to write the header)
		output_file = wave.open(args.output, 'wb')
		output_file.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))
		output_file.close()

		# Read whole file into buffer (TODO: change to chunk by chunk)
		data = file.readframes(-1)

		# Quantize TODO: should also be refactored, since the memory footprint is huge
		# For every bit, 8 bits are used to store it
		reduced_data = quantize_bit_sequence(data)

		# Write actual data now
		output_file = open(args.output, 'wb')
		output_file.seek(44)
		output_file.write(reduced_data)
		output_file.close()

main()
