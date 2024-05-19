#!/usr/bin/python3
import cmd

from models.base_model import BaseModel
from models import storage
from models.state import State
"""
    program contains the entry point of the command interpreter
"""


class HBNBCommand(cmd.Cmd):
    """
    Console class
    """
    prompt = '(hbnb) '
    valid_class = ["BaseModel", "User"]

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, line):
        """Quits command interpreter with ctrl+d"""
        return True

    def do_create(self, line):
        """Creates a new instance of BaseModel,
        saves it (to the JSON file) and prints the id."""
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
        arg = line.split()
        if len(arg) == 0:
            print("** class name missing **")
            return
        elif len(args) == 0:
            print("** instance id missing **")
            return
        obj_id = args[1]
        key = "{}.{}".format(class_name, obj_id)
        if key not in storage.all():
            print("** no instance found **")
        else:
            print(storage.all()[key])

    def do_destroy(self, line):
        """Deletes an instance based on the class
        name and id (save the change into the JSON file)."""
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in self.valid_class:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        obj_id = args[1]
        if args[1][0] == '"':
            args[1] = args[1].replace('"', "")
        key = args[0] + '.' + args[1]
        if key not in storage.all():
            print("** no instance found **")
        else:
             del storage.all()[key]
        storage.save()

    def do_all(self, line):
        """Prints all string representation of all
        instances based or not on the class name."""
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

    def do_update(self, line):
        """Updates an instance based on the class name
        and id by adding or updating attribute."""
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in self.valid_class:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        obj_id = args[1]
        key = "{}.{}".format(class_name, obj_id)
        if key not in storage.all():
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        attr_name = args[2]
        if len(args) < 4:
            print("** value missing **")
            return
        # Handling double quotes for string arguments with spaces
        attr_value = ""
        if args[3][0] == '"' and args[-1][-1] == '"':
            attr_value = " ".join(args[3:-1])[1:-1]
        else:
            attr_value = args[3]
        obj = storage.all()[key]
        setattr(obj, attr_name, attr_value)
        obj.save()

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
    cm = HBNBCommand()
    cm.cmdloop()
