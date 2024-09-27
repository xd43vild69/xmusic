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
            if(found_index > 11):
                found_index = 0        

        return notes_string

    def set_scale(self, note_key):        
        # loop through each string on tool_strings to enable notes

        scale_mayor = ['H','W','W','H','W','W','W','H']

        for s in self.tool_strings: # for each string in tool                            
            is_completed = False
            interval = 1
            is_active = False

            index_key_note = -1

            for index, n1 in enumerate(s):
                if n1.name == note_key:
                    index_key_note = index
                    s[index].root = True
                    #n[index].step = scale_mayor[interval]
                    s[index].step = interval
                    break

            i = index_key_note
            j = 0
            next_position = 0

            while not is_completed:
                next_interval = scale_mayor[interval]
                
                if next_interval == 'H':
                    next_position = 1
                elif next_interval == 'W':
                    next_position = 2
                
                i = i + next_position
                j += next_position
                interval += 1                   
                
                if i + next_position > len(s):
                    s[0 + i].root = False
                    s[0 + i].step = interval
                else:
                    if s[i].name == note_key:
                        s[i].root = True
                    else:
                        s[i].root = False                        
                    
                    s[i].step = interval
                
                if j >= 12:
                    is_completed = True
                    
                if i >= 12:
                    i = 0
            
            print("ok")

            


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
