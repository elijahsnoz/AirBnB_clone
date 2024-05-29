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
    valid_class = ["BaseModel", "User", "State"]

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

<<<<<<< HEAD
    def do_show(self, line):
        """Prints the string representation of
        an instance based on the class name and id."""
        arg = line.split(' ')
        if len(arg) == 0:
            print("** class name missing **")
            return
=======
    def do_count(self, line):
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

    def do_show(self, line, *args):
        """Prints the string representation of
        an instance based on the class name and id."""
        arg = line.split()
        if len(arg) == 0:
            print("** class name missing **")
            return
        elif len(args) == 0:
            print("** instance id missing **")
            return
>>>>>>> 0794edb (console)
        else:
            class_name = arg[0]
            if class_name not in self.valid_class:
                print("** class doesn't exist **")
                return
<<<<<<< HEAD
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
=======
            obj_id = args[0]
            key = "{}.{}".format(class_name, obj_id)
            if key not in storage.all():
                print("** no instance found **")
                return
            print(storage.all()[key])
>>>>>>> 0794edb (console)

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id.
        """
        if line == "" or line is None:
            print("** class name missing **")
        else:
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(words) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(words[0], words[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[key]
                    storage.save()

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
<<<<<<< HEAD
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
=======
                args_str = method_call.split('(', 1)[1][:-1]  # Get the part inside the parentheses
                # print(f"arg str{args_str}")
                args = args_str.split(',')  # Split arguments by comma
                # Strip whitespace and quotes from arguments
                args = [arg.strip().strip('"').strip("'") for arg in args]
                
                if method_name:
                    command_method = getattr(self, f"do_{method_name}", None)
                    if command_method:
                        return command_method(class_name, *args)
                    else:
                        print("** invalid command **")
>>>>>>> 0794edb (console)
            except Exception as e:
                print(f"** an error occurred: {e} **")
if __name__ == '__main__':
    HBNBCommand().cmdloop()
