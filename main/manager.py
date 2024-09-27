from .node import Node
from .note import Note
from .instrument import Instrument


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

        if Tool == Tool.Guitar:
            self.instrument = ['E', 'A', 'D', 'G', 'B', 'E']
            # self.instrument = ['E']
        elif Tool == Tool.Bass4:
            self.instrument = ['E', 'A', 'D', 'G']
        elif Tool == Tool.Bass4:
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

            s[index_key_note].root = True
            s[index_key_note].step = interval
            i = index_key_note

            while not is_completed:
                next_position = self.get_steps(scale[interval])
                interval += 1
                i = i + next_position

                if i > 12:
                    i = 12 - i + next_position

                s[i].root = (s[i].name == note_key)
                s[i].step = interval if interval < 8 else 1

                if interval == 8:
                    is_completed = True
                    continue

                if s[i].name != note_key and i == 12:  # restart array
                    i = 0
                    s[i].root = (s[i].name == note_key)
                    s[i].step = interval if interval < 8 else 1