import matplotlib.pyplot as plt
import wave
import argparse
import numpy as np
from pathlib import Path

parser = argparse.ArgumentParser()

parser.add_argument("input", help="set input file")
parser.add_argument("--separate", help="separate wave file into channels. Output files format: [Filename]-ch[Channel "
                                       "Number].wave (Ex: song-ch1.wav)", action='store_true')

args = parser.parse_args()


# Params should be of form:
def write_wav(file_name, data, params):
    with wave.open(file_name, 'wb') as file:
        file.setparams(params)
        file.writeframes(bytes(data))


def main():
    # Input validation
    if not args.input:
        print("Input file not set!")
        return

    spf = wave.open(args.input, 'r')

    # Read input file params
    nchannels, sampwidth, framerate, nframes, comptype, compname = spf.getparams()

    print("Input file:\t", args.input)
    print("No Channels:\t", nchannels)
    print("Sample Width:\t", sampwidth)
    print("Framerate:\t", framerate)
    print("No frames:\t", nframes)
    print("Comp Type:\t", comptype)
    print("Comp Name:\t", compname)
    print("Bit-depth:\t", sampwidth / nchannels * 8)

    # Extract Raw Audio from Wav File
    signal = spf.readframes(-1)
    signal = np.frombuffer(signal, np.int16)
    # fs = spf.getframerate()

    channels_data = []
    for i in range(0, nchannels):
        # Get interleaved channel samples from sample frame
        channels_data.append(signal[i::nchannels])

    # Write separated channels only if asked for
    if args.separate:
        # Write only if all channels are retrieved successfully
        for i, ch_data in zip(range(0, nchannels), channels_data):
            write_wav(
                str.format('{}-ch{}.wav', Path(args.input).stem, i + 1),
                ch_data,
                (1, sampwidth, framerate, nframes, comptype, compname))

    # Plot charts
    avg_signal = []

    for i in range(0, nframes):
        total = 0

        for ch in channels_data:
            total = total + ch[i]

        avg_signal.append(total / len(channels_data))

    time1 = np.linspace(0, len(channels_data[0]) / framerate, num=len(channels_data[0]))

    for i in range(0, nchannels):
        plt.figure(i)
        plt.title('Channel No:' + str(i + 1))
        plt.plot(time1, channels_data[i])

    plt.figure(nchannels)
    plt.title('Average of channels')
    plt.plot(time1, avg_signal)

    plt.show()


main()
