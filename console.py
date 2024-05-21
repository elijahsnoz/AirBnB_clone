#!/usr/bin/python3
"""Module for the entry point of the command interpreter."""

import cmd
from models.base_model import BaseModel
from models import storage
import re
from shlex import split


class HBNBCommand(cmd.Cmd):

    """Class for the command interpreter."""

    prompt = "(hbnb) "

    def do_EOF(self, line):
        """Handles End Of File character.
        """
        print()
        return True

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def emptyline(self):
        """Doesn't do anything on ENTER.
        """
        pass
    def do_create(self, line):
        """Creates a new instance of a given class and saves it"""
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in self.valid_class:
            print("** class doesn't exist **")
            return
        new_instance = BaseModel()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, line):
        """Prints the string representation of
        an instance based on the class name and id."""
        arg = line.split(' ')
        if len(arg) == 0:
            print("** class name missing **")
            return
        else:
            class_name = arg[0]
            if class_name not in self.valid_class:
                print("** class doesn't exist **")
                return
            elif len(arg) < 2:
                print("** instance id missing **")
                return
            else:
                obj_id = arg[1]
                key = "{}.{}".format(class_name, obj_id)
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[key])
                    """return print(storage.all()[key])"""
if __name__ == '__main__':
    HBNBCommand().cmdloop()
