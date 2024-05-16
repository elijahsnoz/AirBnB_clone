#!/usr/bin/python3
import cmd
from models.base_model import BaseModel
from models import storage
from models.user import User

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

    def do_create(self, line):
        """Creates a new instance of BaseModel, saves it (to the JSON file) and prints the id."""
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in ["BaseModel"]:
            print("** class doesn't exist **")
            return
        new_instance = BaseModel()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, line):
        """Prints the string representation of an instance based on the class name and id."""
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in ["BaseModel"]:
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
        print(storage.all()[key])

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id (save the change into the JSON file)."""
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in ["BaseModel"]:
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
        del storage.all()[key]
        storage.save()

    def do_all(self, line):
        """Prints all string representation of all instances based or not on the class name."""
        args = line.split()
        if len(args) == 0:
            objs = storage.all().values()
        else:
            class_name = args[0]
            if class_name not in ["BaseModel"]:
                print("** class doesn't exist **")
                return
            objs = [obj for obj in storage.all().values() if type(obj).__name__ == class_name]
        print(objs)

    def do_update(self, line):
        """Updates an instance based on the class name and id by adding or updating attribute."""
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in ["BaseModel"]:
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

if __name__ == '__main__':
    cm = HBNBCommand()
    cm.cmdloop()

