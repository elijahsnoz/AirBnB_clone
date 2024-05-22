#!/usr/bin/python3
"""contains the entry point of the command interpreter"""
import cmd
import re
from shlex import split

import models
# A global constant since both functions within and outside uses it.
CLASSES = [
    "BaseModel",
    "User",
    "City",
    "Place",
    "State",
    "Amenity",
    "Review"
]


def parse(arg):
    """ Parse data """
    data = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if data is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            ret = [i.strip(",") for i in lexer]
            ret.append(brackets.group())
            return ret
    else:
        lexer = split(arg[:data.span()[0]])
        ret = [i.strip(",") for i in lexer]
        ret.append(data.group())
        return ret


def ch_args(args):
    """checks if args is valid

    Args:
        args (str): the string containing the arguments passed to a command

    Returns:
        Error message if args is None or not a valid class, else the arguments
    """
    arg_list = parse(args)

    if len(arg_list) == 0:
        print("** class name missing **")
    elif arg_list[0] not in CLASSES:
        print("** class doesn't exist **")
    else:
        return arg_list


class HBNBCommand(cmd.Cmd):
    """The class that implements the console
    for the AirBnB clone web application
    """
    prompt = "(hbnb) "
    storage = models.storage

    def emptyline(self):
        """Command to executed when empty line + <ENTER> key"""
        pass

    def default(self, arg):
        """Default behaviour for cmd module when input is invalid"""
        action_map = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update,
            "create": self.do_create
        }

        match = re.search(r"\.", arg)
        if match:
            arg1 = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", arg1[1])
            if match:
                command = [arg1[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in action_map:
                    call = "{} {}".format(arg1[0], command[1])
                    return action_map[command[0]](call)

        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_EOF(self, line):
        """EOF signal to exit the program"""
        print("")
        return True

    def do_quit(self, line):
        """When executed, exits the console."""
        return True

    def do_create(self, line):
        """Creates a new instance of BaseModel, saves it (to a JSON file)
        and prints the id"""
        args = ch_args(line)
        if args:
            print(eval(args[0])().id)
            self.storage.save()

    def do_show(self, line):
        """Prints the string representation of an instance based
        on the class name and id"""
        args = ch_args(line)
        if args:
            if len(args) != 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(args[0], args[1])
                if key not in self.storage.all():
                    print("** no instance found **")
                else:
                    print(self.storage.all()[key])

    def do_all(self, line):
        """Prints all string representation of all instances based or not
        based on the class name"""
        arg_list = split(line)
        objs = self.storage.all().values()
        if not arg_list:
            print([str(obj) for obj in objs])
        else:
            if arg_list[0] not in CLASSES:
                print("** class doesn't exist **")
            else:
                print([str(obj) for obj in objs
                       if arg_list[0] in str(obj)])

    def do_destroy(self, line):
        """Delete a class instance based on the name and given id."""
        arg_list = ch_args(line)
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

    def do_count(self, arg):
        """Retrieve the number of instances of a class"""
        arg1 = parse(arg)
        count = 0
        for obj in models.storage.all().values():
            if arg1[0] == type(obj).__name__:
                count += 1
        print(count)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
