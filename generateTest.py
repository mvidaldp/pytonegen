
from PyToneGen import PyToneGen

PERIOD = 0.5  # duration of the tone
letters = ['c', 'c#', 'db', 'd', 'd#', 'eb', 'e', 'f', 'f#', 'gb', 'g', 'g#', 'ab', 'a', 'a#', 'bb', 'b']
# letters = ['C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#', 'Gb', 'G', 'G#', 'Ab', 'A', 'A#', 'Bb', 'B']

def num_to_key(num):
    return {
        0: 'C',
        1: 'C#',
        2: 'D',
        3: 'D#',
        4: 'E',
        5: 'F',
        6: 'F#',
        7: 'G',
        8: 'G#',
        9: 'A',
        10: 'A#',
        11: 'B',
    }[num]

for o in range(9):
    for l in range(12):
        key = num_to_key(l)
        tone = PyToneGen(key + str(o), PERIOD)
        if tone.accidental:
            print("{}{}{} = {}".format(tone.score, tone.accidental, str(tone.octave), tone.frequency))
        else:
            print("{}{} = {}".format(tone.score, str(tone.octave), tone.frequency))
        tone.record()
