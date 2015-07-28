#imports from standard packages
from uuid import uuid1
import time

"""
This file contains utility functions used throughout the application
"""

def generate_uid():
    """
    will generate a random UUID.
    see python documentation https://docs.python.org/2/library/uuid.html
    """
    ui = str(uuid1())
    return ui

def is_unique(data, dataset):
    """
    will verify if 'data' passed as argument is unique in a dataset
    """
    seen = set()
    return not any(value in seen or seen.add(value) for value in data)


def describe(something):
    """
    this will return the object(something) class name and type as well as all attributes excluding those starting with a double underscore
    """
    #will return the object type and class (Type:Class) as text
    objectclass = str(something.__class__.__name__)
    objecttype = str(type(something))
    #will return a list of all non"__" attributes, including use defined ones (**kwargs)
    attributes = str(filter(lambda a: not a.startswith('__'), dir(something)))
    returnvalue = objectclass, " (", objecttype, "): ", attributes
    return returnvalue

def get_current_date():
    """
    will return today's date as a string of format yyyymmdd
    """
    return time.strftime("%Y%m%d")

def get_current_time(option):
    """
    will return current time as a string of format hhmmss
    """
    if option == 1:
        return time.strftime("%H%M%S")
    elif option == 2:
        return time.strftime("%H:%M:%S")
    else:
        pass


def error_log(message):
    # append/save timestamp and exception to errorlog.txt
    # object Exception e is sent as is and this method is taking care of parsing it to string
    # and adding a timestamp
    console = 1  #TODO use this value to send error message to the console instead of the file
    if console == 0:
        timestamp = time.strftime("%c") # date and time representation using this format: 11/07/14 12:50:35
        fullmessage = timestamp + ": " + str(message) + "\n"
        anyfile = open("errorlog.txt", "a") #this is required since a file object is later expected
        anyfile.write(fullmessage)
        anyfile.close()
    elif console == 1:
        print message + "\n"  #TODO remove when done



def center_window(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)-200
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    




########################################################################################
def gather_attributes(something):
    """
    Receive an object and return an array containing the object attributes and value
    """
    attributes =[]
    for key in sorted(something.__dict__):
        attributes.append('%s' %(key))
    return attributes


def search_uid(db, value):
    return filter(lambda candidate: candidate['uid'] == value, db)
    

def print_object(something):
    #for dev only!
    #will print key, attributes, value in the console.
    #most likely will be an dict or a class instance.
    #so this is for the dict
    if type(something) is dict:
        for key, value in something.iteritems():
            c = something.get(key)
            for attr, value in c.__dict__.iteritems():
                print attr,": ", value
            print "\n"
    else:  #and this for the class instance
        for attr, value in something.__dict__.iteritems():
            print attr, value
    print "\n\n"


# self-test "module"  TODO remove before release
if __name__ == '__main__':
    import lib.datamanagement as DataManagement
    data=dict(DataManagement.read_studydata())
    print_object(data)