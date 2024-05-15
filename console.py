#!/usr/bin/python3
import cmd

"""
    program contains the entry point of the command interpreter
"""

class HBNBCommand(cmd.Cmd):
    """
    Console class
    """
    prompt = '(hbnb) '

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, line):
        """Quits command interpreter with ctrl+d"""
        return True

if __name__ == '__main__':
    cm = HBNBCommand()
    cm.cmdloop()
