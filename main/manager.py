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
            #self.instrument = ['B']
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
        scale_mayor = ['H','W','W','H','W','W','W','H']

        for s in self.tool_strings: # for each string in tool                            
            is_completed = False
            interval = 1

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
                elif next_interval == 'WH':
                    next_position = 3
                
                i = i + next_position

                if i > 12:
                    i = 12 - i + next_position 

                j += next_position
                interval += 1                   
                
                if s[i].name == note_key:
                    s[i].root = True
                else:
                    s[i].root = False                        
                    
                if interval == 8:
                    s[i].step = 1
                    is_completed = True
                    continue
                else:
                    s[i].step = interval
                
                if j >= 12:  # End when a full octave is reached
                    is_completed = True
                    continue
                    
                if s[i].name != note_key and i == 12 :
                    i = 0
                    if s[i].name == note_key:
                        s[i].root = True
                    else:
                        s[i].root = False                        
                        
                    s[i].step = interval                    
              


            


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
