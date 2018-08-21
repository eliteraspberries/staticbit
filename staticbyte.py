#!/usr/bin/env python -u

"""staticbyte.py - encode a stream of bytes as static noise

Usage:
    python -u staticbyte.py (-e | -d) <FILE> [-s <N>]
    python -u staticbyte.py -h

Options:
    -s  Set the chip size (default: 4096)
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
    z *= 1.0 / n
    return z


class Chip(object):

    def __init__(self, size, seed=None):
        self.size = size
        numpy.random.seed(seed)

    def codes(self, n):
        return numpy.float32(numpy.random.normal(0.0, 0.2, self.size * n))


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
            size = 2 ** 12
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
        for byte in readbytes(sys.stdin):
            codes = chip.codes(2 ** 8)
            i = byte * chip.size
            j = i + chip.size
            pcm = PCM_DTYPE(codes[i:j] * PCM_MAX)
            frames = pcm.tostring()
            wav.writeframes(frames)
    else:
        while True:
            frames = wav.readframes(chip.size)
            if len(frames) == 0:
                break
            pcm = numpy.fromstring(frames, dtype=PCM_DTYPE)
            data = numpy.float32(pcm)
            data = data / (PCM_MAX + 1.0)
            codes = chip.codes(2 ** 8)
            xc = xcor(codes, data)
            i = numpy.argmax(xc ** 2)
            byte = i / chip.size
            if sys.stdout.isatty():
                byte &= 127
            sys.stdout.write(chr(byte))

    wav.close()
