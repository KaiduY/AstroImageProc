import shutil
import psutil
import subprocess
import os
import numpy as np
from pathlib import Path
import sys
from datetime import datetime
import logging
from typing import Callable

log = logging.getLogger(__name__)
class console:
    """A console class for interacting with the AstroImageProc program."""

    def __init__(self):
        """Initialize the console object."""
        self.size = self._getTerminalSize() # (width, collumns)
        self.counter = 0
        self.read = True
        self.buffer = []
        self.projectPath = self._projectPath()/'MyProject/'
        self.startTime = datetime.now()
        self.functions = {}
        subprocess.run(["printf", "\033[9999H"]) # Disable autoscrolling

    def _clear(self):
        """Clear the console screen."""
        # This method is not relible
        #print("\033[H\033[J", end="") # Magic line to clear the screen
        subprocess.call('clear' if os.name=='posix' else 'cls')

    def _getTerminalSize(self) -> tuple:
        """Get the size of the terminal window.
        
        Returns:
            tuple: A tuple containing the width and height of the terminal window.
        """
        size = shutil.get_terminal_size()
        return tuple(size)

    def _makeMemoryLine(self) -> str:
        """Generate a memory usage information line.
        
        Returns:
            str: A string containing memory usage information.
        """
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
        """Generate the contents of the console screen.
        
        Returns:
            str: A string containing the contents of the console screen.
        """
        w, h = self.size
        h -= 1
        screen = np.full(h,'\033[95m\n', dtype=object)
        mem = self._makeMemoryLine()
        

        buffer = np.array([buf+'\n' for buf in self.buffer]) # Add \n to end of every line
        log.debug(f'Terminal buff: {buffer}') 
        buffer_length = buffer.size
        
        now = datetime.now()
        nowstr = now.strftime("%H:%M:%S")
        startstr = self.startTime.strftime("%H:%M:%S")
        elaptime = now - self.startTime
        screen[0] = f'\033[94mStart: {startstr}, Now: {nowstr}, Elapsed time: {elaptime}\n'
        screen[1:1+buffer_length] = buffer
        screen[-1] = mem
        return ''.join(screen)

    def update(self):
        """Update the console screen and wait for user input."""
        self._flushBuffer()
        if self.read:
            command = input('>>')
            self._execute(command)

        self._clear()
        terminal = self._makeTerminal()
        print(terminal)
    
    def get_counter(self):
        self.counter += 1
        return self.counter

    def _execute(self, com: str):
        """Execute a command provided by the user.
        
        Args:
            com (str): The command string provided by the user.
        """
        split = com.split(' ')
        command = split[0]
        args = split[1:]
        try:
            if command == 'help':
                self._addToBuffer('List of available commands:\n'\
                'cd [\path] --> sets the path of the project\n'\
                'pwd --> returns the current path\n'\
                'exit --> exits the program\n')
            elif command == 'pwd':
                self._addToBuffer(f'Project path: {self.projectPath}')
            elif command == 'cd':
                path = Path(args[0])

                if path.exists():
                    self.projectPath = path
                    self._addToBuffer(f'Project path: {self.projectPath}')
                else:
                    self._addToBuffer('The path does not exist, typo?')
            elif command == 'exit':
                self._addToBuffer('Bye!')
                sys.exit()

            elif command in self.functions:
                func = self.functions[command]
                func(tuple(args))

            else:
                self._addToBuffer('Unknown command!')
        except Exception as e:
            log.error(f'Error while executing command {command}: {e}')
            self._addToBuffer('Something went wrong!')
    
    def _addToBuffer(self, message, color='\033[95m'):
        mes = message.split('\n')
        for line in mes:
            line = line.replace('\n', '')
            #log.debug(f'LINE = {line}')
            self.buffer.append(color+line)
        #log.debug(f'Buffer = {self.buffer}')

    def _flushBuffer(self):
        self.buffer = []
    
    def _projectPath(self) -> Path:
        return Path.cwd()
    
    def addFunction(self, command: str, function: Callable):
        self.functions.update({command : function})
        log.debug(self.functions)
        log.debug(f'I added a function for command {command}')

    def getPath(self):
        return self.projectPath

if __name__ == '__main__':
    from time import sleep

    log.debug('Start!')
    console = console()

    #TODO make this a general str statement in a different file
    print('This is an internal script, did something went wrong?')
    sleep(1)
    while True:
        console.update()
        sleep(0.1)