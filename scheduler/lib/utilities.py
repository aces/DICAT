from uuid import uuid1
import time

def generateUniqueID():
    """
    will generate a random 14-bit sequence number is chosen.
    see python documentation https://docs.python.org/2/library/uuid.html
    """
    ui = str(uuid1())
    return ui

def isUnique(visitdata):
    """
    will verify if the visitdata passed as argument is unique in a set
    """
    seen = set()
    return not any(value in seen or seen.add(value) for value in visitdata)


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




def errorlog(message):
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



def centerwindow(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)-200
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    




########################################################################################
def gatherattributes(something):
    """
    Receive an object and return an array containing the object attributes and value
    """
    attributes =[]
    for key in sorted(something.__dict__):
        attributes.append('%s' %(key))
    return attributes


def searchuid(db, value):
    return filter(lambda candidate: candidate['uid'] == value, db)
    

def printobject(something):
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
