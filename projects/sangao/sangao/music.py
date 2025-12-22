import pygame, time
import numpy as np

notes_dct = {
        'c': -9.0, 'c#': -8.0, 'db': -8.0, 'd': -7.0, 'd#': -6.0, 'eb': -6.0,
        'e': -5.0, 'f': -4.0, 'f#': -3.0, 'gb': -3.0, 'g': -2.0, 'g#': -1.0,
        'ab': -1.0, 'a': 0.0, 'a#': 1.0, 'bb': 1.0, 'b': 2.0,
        }

def getExponent(note):
    """ Returns a float needed to obtain the frequency in Hz based on
        'note', which is a string with note name defaulting to 'A', and
        an optional trailing octave value, defaulting to 4; each octave
        begins at the C tone.

        Examples:
            # np is short for numpy
            GetExponent('A4') returns a value 'v' where
                2 ** (np.log2(440) + v) == 440.0  # in Hz

            GetExponent('C') (or C4) returns v where
                2 ** (np.log2(440) + v) == 261.6  # approximate;
                                                  # note that C4 is below A4

            GetExponent('Gb-1') (or G flat, octave -1) returns v where
                2 ** (np.log2(440) + v) == 11.6  # below usual hearing range
    """

    i = 0
    while i < len(note) and note[i] not in '1234567890-':
        i += 1

    if i == 0:
        name = 'a'
    else:
        name = note[: i].lower()

    if i == len(note):
        octave = 4
    else:
        octave = int(note[i: ])

    return notes_dct[name] / 12.0 + octave - 4


def generateTone(freq=440.0, vol=1.0, shape='sine'):
    """ GenerateTone( shape='sine', freq=440.0, vol=1.0 )
            returns pygame.mixer.Sound object

        shape:  string designating waveform type returned; one of
                'sine', 'sawtooth', or 'square'
        freq:  frequency; can be passed in as int or float (in Hz),
               or a string (see GetExponent documentation above for
               string usage)
        vol:  relative volume of returned sound; will be clipped into
              range 0.0 to 1.0
    """

    # Get playback values that mixer was initialized with.
    (pb_freq, pb_bits, pb_chns) = pygame.mixer.get_init()

    if type(freq) == str:
        # Set freq to frequency in Hz; GetExponent(freq) is exponential
        # difference from the exponent of note A4: log2(440.0).
        freq = 2.0 ** (np.log2(440.0) + getExponent(freq))

    # Clip range of volume.
    vol = np.clip(vol, 0.0, 1.0)

    # multiplier and length pan out the size of the sample to help
    # keep the mixer busy between calls to channel.queue()
    multiplier = int(freq / 24.0)
    length = max(1, int(float(pb_freq) / freq * multiplier))
    # Create a one-dimensional array with linear values.
    lin = np.linspace(0.0, multiplier, num=length, endpoint=False)
    if shape == 'sine':
        # Apply a sine wave to lin.
        ary = np.sin(lin * 2.0 * np.pi)
    elif shape == 'sawtooth':
        # sawtooth keeps the linear shape in a modded fashion.
        ary = 2.0 * ((lin + 0.5) % 1.0) - 1.0
    elif shape == 'square':
        # round off lin and adjust to alternate between -1 and +1.
        ary = 1.0 - np.round(lin % 1.0) * 2.0
    else:
        print("shape param should be one of 'sine', 'sawtooth', 'square'.")
        print()
        return None

    # If mixer is in stereo mode, double up the array information for
    # each channel.
    if pb_chns == 2:
        ary = np.repeat(ary[..., np.newaxis], 2, axis=1)

    if pb_bits == 8:
        # Adjust for volume and 8-bit range.
        snd_ary = ary * vol * 127.0
        return pygame.sndarray.make_sound(snd_ary.astype(np.uint8) + 128)
    elif pb_bits == -16:
        # Adjust for 16-bit range.
        snd_ary = ary * vol * float((1 << 15) - 1)
        return pygame.sndarray.make_sound(snd_ary.astype(np.int16))
    else:
        print("pygame.mixer playback bit-size unsupported.")
        print("Should be either 8 or -16.")
        print()
        return None
