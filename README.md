Staticbit is a script to encode a bitstream as static noise.

    $ python staticbit.py -e foo.wav < staticbit.py
    $ python staticbit.py -d foo.wav

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

[Puzzle 1]: https://github.com/eliteraspberries/staticbit/releases/tag/puzzle1

### Puzzle 2

There is a message in the file puzzle2.wav. What does it say?

Download the file from the release named [Puzzle 2][].

[Puzzle 2]: https://github.com/eliteraspberries/staticbit/releases/tag/puzzle2

Hint: The noise is the message and the message is the noise.
