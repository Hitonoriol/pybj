from shutil import get_terminal_size
from os import system, name

def cls(): 
    if name == 'nt': 
        _ = system('cls') 
    elif (name == 'posix'): 
        _ = system('clear')
    else:
        print("\n" * get_terminal_size().lines * 2, end='')
