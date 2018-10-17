#!/usr/bin/env python

"""staticbit.py - encode a bitstream as static noise

Usage:
    python staticbit.py (-e | -d) <FILE> [-s <N>]
    python staticbit.py -h

Options:
    -s  Set the chip size (default: 1024)
    -h  Print this help
"""


from __future__ import print_function

import numpy
import os
import sys
import wave


__author__ = 'Mansour Moufid'
__email__ = 'mansourmoufid@gmail.com'
__license__ = 'ISC'
__status__ = 'Development'
__version__ = '0.1'


PCM_DTYPE = numpy.int16

PCM_MAX = 2.0 ** (16 - 1) - 1.0


def readbytes(f):
    while True:
        char = f.read(1)
        if char == '':
            break
        byte = ord(char)
        yield byte


def tobits(bytes):
    for byte in bytes:
        for i in range(8):
            yield (byte >> i) & 1


def tobyte(bits):
    return sum(2 ** i * bit for i, bit in enumerate(bits))


def xcor(x, y):
    x = numpy.copy(x)
    y = numpy.copy(y[::-1])
    n = x.size + y.size
    x.resize(n)
    y.resize(n)
    X = numpy.fft.rfft(x)
    Y = numpy.fft.rfft(y)
    Z = X * Y
    z = numpy.fft.irfft(Z, n=n)
    return z


def modxcor(x, y):
    z = xcor(x, y)
    n = y.size
    return z[(n // 2):-(n // 2)]


class Chip(object):

    def __init__(self, size, seed=None):
        self.size = size
        numpy.random.seed(seed)

    def code(self):
        return numpy.float32(numpy.random.normal(0.0, 0.2, self.size))


if __name__ == '__main__':

    if len(sys.argv) == 2 and sys.argv[1] == '-h':
        print(__doc__)
        sys.exit(0)
    try:
        encode = '-e' in sys.argv
        i = sys.argv.index('-e' if encode else '-d')
        filename = sys.argv[i + 1]
        if '-s' in sys.argv:
            i = sys.argv.index('-s')
            size = int(sys.argv[i + 1])
        else:
            size = 2 ** 10
    except:
        print(__doc__)
        sys.exit(os.EX_USAGE)

    tty = os.ctermid()
    prompt = '\xF0\x9F\x94\x91  '
    with open(tty, 'w') as f:
        f.write(prompt)
    with open(tty, 'r') as f:
        line = f.readline()
    key = line.rstrip('\n')
    key = int(key)

    chip = Chip(size, seed=key)

    FS = 44100
    SAMPWIDTH = 2
    NCHANNELS = 1

    if encode:
        wav = wave.open(filename, 'wb')
        wav.setframerate(FS)
        wav.setsampwidth(SAMPWIDTH)
        wav.setnchannels(NCHANNELS)
    else:
        wav = wave.open(filename, 'rb')
        sampwidth = wav.getsampwidth()
        nchannels = wav.getnchannels()
        nframes = wav.getnframes()
        fs = wav.getframerate()
        assert fs == FS
        assert sampwidth == SAMPWIDTH
        assert nchannels == NCHANNELS

    if encode:
        for bit in tobits(readbytes(sys.stdin)):
            code = chip.code()
            one = PCM_DTYPE(code * PCM_MAX)
            zero = one * -1
            if bit == 1:
                pcm = one
            else:
                pcm = zero
            frames = pcm.tostring()
            wav.writeframes(frames)
    else:
        bits = []
        while True:
            frames = wav.readframes(chip.size)
            if len(frames) == 0:
                break
            pcm = numpy.fromstring(frames, dtype=PCM_DTYPE)
            data = numpy.float32(pcm)
            data = data / (PCM_MAX + 1.0)
            one = chip.code()
            xc = modxcor(data, one)
            i = numpy.argmax(xc ** 2)
            if xc[i] > 0:
                bit = 1
            else:
                bit = 0
            bits.append(bit)
            if len(bits) == 8:
                byte = tobyte(bits)
                if sys.stdout.isatty():
                    byte &= 127
                sys.stdout.write(chr(byte))
                bits = []

    wav.close()
