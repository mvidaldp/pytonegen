import os

FADE_IN = 0.1
FADE_OUT = 0.1
COMMAND = 'play --no-show-progress -n synth sine %s fade q %s %s %s'
RECORD = 'sox --norm=-0.01 -n -c 1 -b 16 -r 44100 %s synth sine %s fade q %s %s 0 fade l 0 %s %s'

class PyToneGen(object):
    """docstring for ."""
    # Constants
    RIGHT_SCORES = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
    WRONG_FLAT = ('C', 'F')
    WRONG_SHARP = ('B', 'E')

    def __init__(self, note, duration=1.0, tuning=440):
        # super(Tone, self).__init__()
        if len(note) in range(2, 4):  # score entered musst have 2-3 characters
            self.key = note
            self.score = self.check_letter(note[0])
            try:
                self.octave = self.check_octave(int(note[-1:]))
            except:
                print("Error")

            if len(note) == 3:  # then it must include an accidental
                self.accidental = note[1]
            else:  # if len(note) == 2:
                self.accidental = None
        else:
            # Throw error
            print('The inputted note is invalid (e.g. C3, A#5, Bb2).')
        if self.accidental == '#' or 'b':
            if self.accidental == '#' and self.score in self.WRONG_SHARP:
                # Throw error
                print("Wrong accidental: {} does not exist. Please enter a "
                      "valid one.".format(self.score + self.accidental))
            elif self.accidental == 'b' and self.score in self.WRONG_FLAT:
                # Throw error
                print("Wrong accidental: {} does not exist. Please enter a "
                      "valid one.".format(self.score + self.accidental))
        else:
            # Throw error
            print("Wrong accidental. Only 'b' and '#' allowed.")
        self.duration = duration
        self.tuning = tuning
        self.frequency = self.calculate_frequency()

    def check_letter(self, letter):
        # can only be from A to G (lowercase inc)
        if type(letter) is str:
            letter = letter.upper()  # from lower to uppercase if needed
            if letter in self.RIGHT_SCORES:  # can only be from A to G
                return letter
            else:
                # Throw error
                print("Error: The inputted letter must be A-G.")
        else:
            # Throw error
            print("The inputted note is invalid (e.g. C3, A#5, Bb2).")

    def check_octave(self, num):
        # Octaves allowed only from 0 to 8 (both inclusive)
        if num in range(0, 9):
            return num

    def calculate_frequency(self):
        '''
            The basic formula for the frequencies of the notes of the equal
            tempered scale is given by fn = f0 * (a)n where f0 = the frequency
            of one fixed note which must be defined. A common choice is setting
            the A above middle C (A4) at f0 = 440 Hz.
            n = the number of half steps away from the fixed note you are. If
            you are at a higher note, n is positive. If you are on a lower
            note, n is negative.
            fn = the frequency of the note n half steps away.
            a = (2)1/12 = the twelth root of 2 = the number which when
            multiplied by itself 12 times equals 2 = 1.059463094359...
            https://pages.mtu.edu/~suits/NoteFreqCalcs.html
            https://pages.mtu.edu/~suits/notefreqs.html
        '''
        def steps(oct):
            diff = oct - 4
            if oct > 4:
                diff = 12 * (diff - 1)
                return {
                    'C': 3 + diff,
                    'D': 5 + diff,
                    'E': 7 + diff,
                    'F': 8 + diff,
                    'G': 10 + diff,
                    'A': 12 + diff,
                    'B': 14 + diff,
                }[self.score]
            else:
                diff = 12 * diff
                return {
                    'C': -9 + diff,
                    'D': -7 + diff,
                    'E': -5 + diff,
                    'F': -4 + diff,
                    'G': -2 + diff,
                    'A': 0 + diff,
                    'B': 2 + diff
                }[self.score]
        n = steps(self.octave)
        if self.accidental == '#':
            n += 1
        elif self.accidental == 'b':
            n -= 1
        a = 2 ** (1 / 12)
        f = self.tuning * a ** n
        return round(f, 2)

    def play(self):
        os.system(COMMAND % (self.frequency, FADE_IN, self.duration, FADE_OUT))

    def record(self):
        fname = 'output/' + self.key + '.wav'
        os.system(RECORD % (fname, self.frequency, FADE_IN, self.duration, self.duration, FADE_OUT))
