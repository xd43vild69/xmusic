from .node import Node
from .note import Note
from .instrument import Instrument

class Manager:

    # 1 Guitar Standar
    # 2 Bass 4
    # 3 Bass 5

    def __init__(self, Instrument):
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

        self.instrument = []

        if Instrument == Instrument.Guitar:
            self.instrument = ['E', 'A', 'D', 'G', 'B', 'E']
        elif Instrument == Instrument.Bass4:
            self.instrument = ['E', 'A', 'D', 'G']
        elif Instrument == Instrument.Bass4:
            self.instrument = ['B', 'E', 'A', 'D', 'G']        

    
    def display_info(self):
        print(f"Display info")

    def scale_mayor(self):
        print(f"scale mayor")

        # create 7 notes
        # define scale pattern on 12 spaces 1 string
        # display on scren

        scale_notes = []

        names = ['G','A','B','C','D','E','F','G']

        steps = ['h','w','w','h','w','w','w','h']

        root = True

        for i in range(8):

            if (i == 0):
                root = True
            else:
                root = False

            n = Node(i + 1, names[i], steps[i], root)
            
            scale_notes.append(n)

        for n in scale_notes:
            print(f'name: {n.name} interval: {n.interval} step: {n.step}')

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
            if(found_index > 11):
                found_index = 0        

        return notes_string
