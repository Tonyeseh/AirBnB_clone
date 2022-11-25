#!/usr/bin/env python3
# console.py

""" Entry point for the command interpreter """
import cmd
import re
from models.base_model import BaseModel
from models.state import State
from models.user import User
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):
    """ Defines the HBNB class

        Inherits from Cmd class
    """
    prompt = '(hbnb) '
    __class_list = [
        "BaseModel",
        "User",
        "State",
        "Place",
        "Amenity",
        "Review",
        "City"
        ]

    def default(self, line):
        """ Gets command if the command is not caught by any other command """
        self._precmd(line)

    def _precmd(self, line):
        """Catches commands with class.command() syntax"""
        match = re.search(r'^(\w*)\.(\w+)(?:\(([^)]*)\))', line)
        if not match:
            return line

        classname = match.group(1)
        method = match.group(2)
        args = match.group(3)
        command = method + " " + classname
        self.onecmd(command)
        return command

    def do_create(self, arg):
        """ Creates a new instance of BaseModel, saves it
        (to the JSON file) and prints the id """
        class_dict = {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review,
            "City": City}
        if arg is None or arg == '':
            print('** class name missing **')
        elif arg not in class_dict.keys():
            print("** class doesn't exist **")
        else:
            obj = class_dict[arg]()
            obj.save()
            print(obj.id)

    def do_show(self, arg):
        """ Prints the string representation of an instance based
on the class name and id.
        """
        if arg is None or arg == '':
            print('** class name missing **')
        else:
            args = arg.split()
            if args[0] not in HBNBCommand.__class_list:
                print("** class doesn't exist **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(args[0], args[1])
                obj = storage.all().get(key, None)
                if obj is None:
                    print("** no instance found **")
                else:
                    print(obj)

    def do_destroy(self, arg):
        """ Deletes an instance based on the class name and id
        (save the change into the JSON file)

            Usage:
                destroy <name of class> <id of object>
        """
        if arg is None or arg == '':
            print("** class name missing **")
        else:
            args = arg.split()
            if args[0] not in HBNBCommand.__class_list:
                print("** class doesn't exist **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(args[0], args[1])
                obj = storage.all().get(key, None)
                if obj is None:
                    print("** no instance found **")
                else:
                    storage.all().pop(key)
                    storage.save()

    def do_all(self, arg):
        """ Prints all string representation of all instances based
        or not on the class name.

            Usage:
                all - prints all objects
                all <class name> - prints all instances of <class name>
        """
        if arg is None or arg == '':
            for k, v in storage.all().items():
                print(v)
        else:
            if arg in HBNBCommand.__class_list:
                for k, v in storage.all().items():
                    class_name = k.split('.')
                    if class_name[0] == arg:
                        print(v)
                    else:
                        pass
            else:
                print("** class doesn't exist **")

    def do_update(self, arg):
        """ Updates an instance based on the class name and id by
        adding or updating attribute(save the chaneg into the JSON file)

            Usage:
                update <class name> <id> <attribute name> "<attribute value>"
        """
        class_list = [
            "BaseModel",
            "User",
            "State",
            "Place",
            "Amenity",
            "Review",
            "City"]
        if arg is None or arg == '':
            print("** class name missing **")
        else:
            args = arg.split(maxsplit=3)
            if args[0] not in HBNBCommand.__class_list:
                print("** class doesn't exist **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(args[0], args[1])
                obj = storage.all().get(key, None)
                if obj is None:
                    print("** no instance found **")
                elif len(args) < 3:
                    print("** attribute name missing **")
                elif len(args) < 4:
                    print("** value missing **")
                else:
                    value = obj.__dict__.get(args[2], None)
                    new_val = args[3].split("\"")
                    if len(new_val) != 3 or new_val[2] != '':
                        pass
                    else:
                        if value:
                            obj.__dict__[args[2]] = new_val[1]
                            obj.save()
                        else:
                            setattr(obj, args[2], new_val[1])
                            obj.save()

    def do_EOF(self, arg):
        """ Press ^D(Control + D) to exit the program """
        print('\n')
        return True

    def do_quit(self, arg):
        """ Quit command to exit the program """
        return True

    def emptyline(self):
        """ Called when an empty line is entered in the prompt
        If the method is not overridden, it repeates the last
        non-empty command entered.
        Another Implementation:
        if self.lastcmd:
            self.lastcmd = ''
            return self.onecmd("\n")
        """
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
