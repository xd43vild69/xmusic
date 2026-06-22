from ..entities.node import Node
from ..entities.note import Note
from ..instrument import Instrument


class Manager:

    def __init__(self, Tool):

        self.strings = []
        self.instrument = []
        self.tool_strings = []

        self.notes = [
            Note('A'),
            Note('A#'),
            Note('B'),
            Note('C'),
            Note('C#'),
            Note('D'),
            Note('D#'),
            Note('E'),
            Note('F'),
            Note('F#'),
            Note('G'),
            Note('G#'),
            Note('A'),
        ]

        if Tool == Instrument.Guitar:
            self.instrument = ['E', 'A', 'D', 'G', 'B', 'E']
        elif Tool == Instrument.GuitarDropD:
            self.instrument = ['D', 'A', 'D', 'G', 'B', 'E']
        elif Tool == Instrument.GuitarHalfStepDown:
            self.instrument = ['D#', 'G#', 'C#', 'F#', 'A#', 'D#']
        elif Tool == Instrument.GuitarDStandard:
            self.instrument = ['D', 'G', 'C', 'F', 'A', 'D']
        elif Tool == Instrument.GuitarDropC:
            self.instrument = ['C', 'G', 'C', 'F', 'A', 'D']
        elif Tool == Instrument.GuitarDADGAD:
            self.instrument = ['D', 'A', 'D', 'G', 'A', 'D']
        elif Tool == Instrument.GuitarOpenG:
            self.instrument = ['D', 'G', 'D', 'G', 'B', 'D']
        elif Tool == Instrument.GuitarOpenD:
            self.instrument = ['D', 'A', 'D', 'F#', 'A', 'D']
        elif Tool == Instrument.Bass4:
            self.instrument = ['E', 'A', 'D', 'G']
        elif Tool == Instrument.Bass4DropD:
            self.instrument = ['D', 'A', 'D', 'G']
        elif Tool == Instrument.Bass4DropC:
            self.instrument = ['C', 'G', 'C', 'F']
        elif Tool == Instrument.Bass5:
            self.instrument = ['B', 'E', 'A', 'D', 'G']

    def set_strings_tool(self):

        for s in self.instrument:
            self.tool_strings.append(self.set_string(s))

        return self.tool_strings

    def set_string(self, initial_note):
        notes_string = []

        for n in self.notes:
            notes_string.append(n)

        found_index = -1

        for index, note in enumerate(self.notes):
            if note.name == initial_note:
                found_index = index
                break

        for i in range(0, 13):
            notes_string[i] = self.notes[found_index]
            found_index = found_index + 1
            if (found_index > 11):
                found_index = 0

        return notes_string

    def get_steps(self, interval_type):
        steps = 0

        if interval_type == 'H':
            steps = 1
        elif interval_type == 'W':
            steps = 2
        elif interval_type == 'WH':
            steps = 3
        else:
            try:
                steps = int(interval_type)
            except ValueError:
                pass

        return steps

    def set_scale(self, note_key, scale):        
        for s in self.tool_strings:  # for each string in tool
            is_completed = False
            interval = 1
            index_key_note = -1
            next_position = 0

            # Find the index of the root note in the string
            index_key_note = next(
                (index for index, note in enumerate(s) if note.name == note_key), -1)

            interval_map = {
                0: '1', 1: 'b2', 2: '2', 3: 'b3', 4: '3', 5: '4',
                6: 'b5', 7: '5', 8: 'b6', 9: '6', 10: 'b7', 11: '7'
            }

            s[index_key_note].root = True
            s[index_key_note].step = interval
            s[index_key_note].interval = '1'
            i = index_key_note
            semitones_from_root = 0

            while not is_completed:
                next_position = self.get_steps(scale[interval])
                semitones_from_root += next_position
                interval += 1
                i = i + next_position

                if i > 12:
                    i = i % 12

                s[i].root = (s[i].name == note_key)
                s[i].step = interval if interval < len(scale) else 1
                s[i].interval = interval_map[semitones_from_root % 12]

                if interval == len(scale):
                    is_completed = True
                    continue

                if s[i].name != note_key and i == 12:  # restart array
                    i = 0
                    s[i].root = (s[i].name == note_key)
                    s[i].step = interval if interval < 8 else 1