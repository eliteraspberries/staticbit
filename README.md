Staticbit is a collection of scripts to encode data as static noise.


## Requirements

The staticbit scripts require Python and [NumPy][].

To install these on a Debian GNU/Linux system:

    $ sudo apt-get install python python-numpy


## staticbit.py

Encode a file as static noise:

    $ python staticbit.py -e foo.wav < staticbit.py

The script prompts for a key (a 32-bit number), reads from standard input,
and outputs a WAVE file.  Decode it:

    $ python staticbit.py -d foo.wav


## staticbyte.py

The staticbyte script is similar to staticbit but encodes bytes not bits.
Its output is smaller but decoding takes much longer.


## Puzzles

### Puzzle 1

I have encoded two files of equal length:

    $ python staticbit.py -e a.wav < README.md
    $ wc README.md
           4      23     151 README.md
    $ python -c "print('\x00' * 150)" | python staticbit.py -e b.wav

Download the files from the release named [Puzzle 1][].

Determine which file is which and prove it.

### Puzzle 2

There is a message in the file puzzle2.wav. What does it say?

Download the file from the release named [Puzzle 2][].

Hint: The noise is the message and the message is the noise.

### Puzzle 3

Like Puzzle 2 but using staticbyte instead of staticbit.

Download the file from the release named [Puzzle 3][].


[Python]: <https://www.python.org/>
[NumPy]: <http://www.numpy.org/>
[Puzzle 1]: https://github.com/eliteraspberries/staticbit/releases/tag/puzzle1
[Puzzle 2]: https://github.com/eliteraspberries/staticbit/releases/tag/puzzle2
[Puzzle 3]: https://github.com/eliteraspberries/staticbit/releases/tag/puzzle3
