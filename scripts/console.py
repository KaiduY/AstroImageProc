import shutil
import psutil
import subprocess
import os
import numpy as np
class console:

    def __init__(self):
        self.size = self._getTerminalSize() # (width, collumns)
        self.counter = 0
        self.read = True
        self.buffer = []
        subprocess.run(["printf", "\033[9999H"]) # Disable autoscrolling

    def _clear(self):
        # This method is not relible
        #print("\033[H\033[J", end="") # Magic line to clear the screen
        subprocess.call('clear' if os.name=='posix' else 'cls')

    def _getTerminalSize(self) -> tuple:
        size = shutil.get_terminal_size()
        return tuple(size)

    def _makeMemoryLine(self) -> str:
        line = '\033[94m'
        size = self.size[0] + len(line) # Substract the color tag length
        line += 'Memory usage '

        # Get memory information
        mem = dict(psutil.virtual_memory()._asdict())
        mem_str = f" {mem['used']/(1024**3):.1f} GB / {mem['total']/(1024**3):.1f} GB ({mem['percent']:.1f} %)"
        
        sep = '='*(size-len(line)-len(mem_str))
        line += sep
        line += mem_str
        return line

    def _makeTerminal(self) -> str:
        w, h = self.size
        h -= 1
        screen = np.full(h,'\033[95m\n', dtype=object)
        cnt = self.get_counter()
        mem = self._makeMemoryLine()
        

        buffer = np.array(self.buffer)
        buffer_length = buffer.size
        screen[1] = str(cnt) + '\n'
        screen[2:2+buffer_length] = buffer
        screen[-1] = mem
        return ''.join(screen)

    def update(self):
        self._clear()
        terminal = self._makeTerminal()
        print(terminal)
        if self.read:
            command = input('>>')
            self._execute(command)

    
    def get_counter(self):
        self.counter += 1
        return self.counter

    def _execute(self, com: str):
        split = com.split(' ')
        command = split[0]
        args = split[1:]

        self.buffer = []
        if command == 'help':
            self.buffer.append('Help will be coming soon!')
        else:
            self.buffer.append('Unknown command!')
    
if __name__ == '__main__':
    from time import sleep
    console = console()

    #TODO make this a general str statement in a different file
    print('This is an internal script, did something went wrong?')
    sleep(1)

    while True:
        console.update()
        sleep(0.1)