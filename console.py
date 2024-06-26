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
    valid_class = ["BaseModel", "User", "State",  "City", "Amenity", "Place", "Review"]

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
        """Prints the string representation of an instance based
        on the class name and id"""
        args = line.split(' ')
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in self.valid_class:
            print("** class doesn't exist **")
        if len(args) < 2:
            print("** instance id missing **")
            return
        else:
            key = f"{args[0]}.{args[1]}"
            if key not in storage.all():
                    print("** no instance found **")
                    return
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
        """Prints all string representation of all instances based or not
        based on the class name"""
        """arg_list = line.split(line)
        objs = storage.all().values()
        if not arg_list:
            print([str(obj) for obj in objs])
        else:
            if arg_list[0] not in self.valid_class:
                print("** class doesn't exist **")
                return
            print([str(obj) for obj in objs
                if arg_list[0] in str(obj)])"""
        """Prints all string representation of all instances.
        """
        if line != "":
            words = line.split(' ')
            if words[0] not in self.valid_class:
                print("** class doesn't exist **")
            else:
                nl = [str(obj) for key, obj in storage.all().items()
                      if type(obj).__name__ == words[0]]
                print(nl)
        else:
            new_list = [str(obj) for key, obj in storage.all().items()]
            print(new_list)

    def do_destroy(self, line):
        """Delete a class instance based on the name and given id."""
        """arg_list = line.split()
        if arg_list:
            if len(arg_list) == 1:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(*arg_list)
                if key in self.storage.all():
                    del self.storage.all()[key]
                    self.storage.save()
                else:
                    print("** no instance found **")
        """
        if line == "" or line is None:
            print("** class name missing **")
        else:
            args = line.split(' ')
            if args[0] not in self.valid_class:
                print("** class doesn't exist **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(args[0], args[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[key]
                    storage.save()

    def do_update(self, line):
        """Updates an instance based on the class name and id by adding or
        updating attribute and save it to the JSON file."""
        arg_list = ch_args(line)
        if arg_list:
            if len(arg_list) == 1:
                print("** instance id missing **")
            else:
                id = "{}.{}".format(arg_list[0], arg_list[1])
                if id in self.storage.all():
                    if len(arg_list) == 2:
                        print("** attribute name missing **")
                    elif len(arg_list) == 3:
                        print("** value missing **")
                    else:
                        obj = self.storage.all()[id]
                        if arg_list[2] in type(obj).__dict__:
                            v_type = type(obj.__class__.__dict__[arg_list[2]])
                            setattr(obj, arg_list[2], v_type(arg_list[3]))
                        else:
                            setattr(obj, arg_list[2], arg_list[3])
                else:
                    print("** no instance found **")

            self.storage.save()

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
