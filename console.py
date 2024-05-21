#!/usr/bin/python3
import cmd

from models.base_model import BaseModel
from models import storage
import re
import json

"""
Program contains the entry point of the command interpreter
"""


class HBNBCommand(cmd.Cmd):
    """
    Console class
    """
    prompt = '(hbnb) '
    valid_class = ["BaseModel", "User", "State"]

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, line):
        """Quit command interpreter with ctrl+d"""
        return True

    def emptyline(self):
        """Overrides the emptyline method to do nothing"""
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

    def do_count(self, line):
        """Counts the number of instances of a given class"""
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        else:
            class_name = args[0]
            if class_name not in self.valid_class:
                print("** class doesn't exist **")
                return
            objs = [obj for obj in storage.all().values()
                    if type(obj).__name__ == class_name]
            print(len(objs))

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

    def do_destroy(self, line):
        """Deletes an instance based on class name and id"""
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        class_name = args[0]
        if class_name not in self.valid_class:
            print("** class doesn't exist **")
            return
        obj_id = args[1]
        key = "{}.{}".format(class_name, obj_id)
        if key in storage.all():
            del storage.all()[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, line):
        """Shows all instances, or all instances of a given class"""
        args = line.split()
        if len(args) == 0:
            objs = storage.all().values()
        else:
            class_name = args[0]
            if class_name not in self.valid_class:
                print("** class doesn't exist **")
                return
            objs = [obj for obj in storage.all().values()
                    if type(obj).__name__ == class_name]
        obj_list = [str(obj) for obj in objs]
        print(obj_list)

    def do_update(self, line, *args):
        """Updates an instance based on the class name and id by adding or
        updating attribute and save it to the JSON file."""
        arg = line.split(" ", 2)
        if len(arg) == 0:
            print("** class name missing **")
            return
        class_name = arg[0]
        if class_name not in self.valid_class:
            print("** class doesn't exist **")
            return
        if len(args) < 1:
            print("** instance id missing **")
            return
        arg_list = args
        if arg_list:
            if len(arg_list) < 0:
                print("** instance id missing **")
            else:
                instance_id = "{}.{}".format(class_name, arg_list[0])
                if instance_id in storage.all():
                    if len(arg_list) == 1:
                        print("** attribute name missing **")
                    elif len(arg_list) == 2:
                        print("** value missing **")
                    else:
                        obj = storage.all()[instance_id]
                        if arg_list[1] in type(obj).__dict__:
                            v_type = type(obj.__class__.__dict__[arg_list[1]])
                            setattr(obj, arg_list[1], v_type(arg_list[2]))
                        else:
                            setattr(obj, arg_list[1], arg_list[2])
                else:
                    print("** no instance found **")

            storage.save()

    def default(self, line):
        """Handle unrecognized commands and pass arguments to the methods."""
        if '.' in line and '(' in line and ')' in line:
            try:
                # Extract class name and method call
                class_name, method_call = line.split('.', 1)
                method_name = method_call.split('(', 1)[0]
                # Get the command method
                command_method = getattr(self, f"do_{method_name}", None)

                if command_method:
                    # Call method with or without arguments
                    if method_call.split('(', 1)[1] is not None:
                        args_str = method_call.split('(', 1)[1][:-1]

                        # Split arguments by comma
                        args = args_str.split(',')

                        cleaned_args = []
                        for arg in args:
                            stripped_arg = arg.strip().strip('"').strip("'")
                            if stripped_arg:
                                cleaned_args.append(stripped_arg)
                        if cleaned_args:
                            return command_method(class_name, *cleaned_args)
                        else:
                            return command_method(class_name)
                else:
                    print("** invalid command **")
            except Exception as e:
                print(f"** an error occurred: {e} **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
