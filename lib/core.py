# DESCRIPTION: A script that contains the small, miscellaneous functions and
# classes that are used everywhere.

# 50726f6772616d6d696e6720697320627265616b696e67206f66206f6e652062696720696d706f
# 737369626c65207461736b20696e746f207365766572616c207665727920736d616c6c20706f73
# 7369626c65207461736b732e

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MAIN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from lib import vectors
from copy import deepcopy


 ####### #     # #     #  #####  ####### ### ####### #     #  #####
 #       #     # ##    # #     #    #     #  #     # ##    # #     #
 #       #     # # #   # #          #     #  #     # # #   # #
 #####   #     # #  #  # #          #     #  #     # #  #  #  #####
 #       #     # #   # # #          #     #  #     # #   # #       #
 #       #     # #    ## #     #    #     #  #     # #    ## #     #
 #        #####  #     #  #####     #    ### ####### #     #  #####


def xor(x, y):
    """An XOR gate for two condition checks."""
    if ((x and y) or (not x and not y)):
        return False
    else:
        return True

def xnor(x, y):
    """An XNOR gate, which is simply a NOT XOR gate."""
    return (not xor(x, y))

def onlyone(iterable):
    """Returns true if only one of the items in iterable is true."""
    count = 0
    for ii in iterable:
        if count > 1:
            return False  # Stop iterating if there is more then one.
        elif ii:
            count += 1
            continue
    return True

def combinelists(*lists):
    """Combine lists together into a single list (i.e. unflatten lists)."""
    return [element for sublist in lists for element in sublist]

def convert(indexorcoordinateorvector,
            tocoordinate=False, toindex=False, tovector=False):
    """Converts the input into a coordinate, vector or index.

    What this function does is it forces the input to change into the desired
    form, with each different form being useful in different conditions. This
    conversion is done via if-elif chains nested inside an if-elif-else chain.

    This method has catches in place: only one of the output types are allowed
    and if the input isn't an index, coordinate or vector it raises TypeErrors.

    PARAMETERS & RETURNS
    ======================
    :indexorcoordinateorvector: This parameter is the item to convert.
    :toindex:       Converts the input into an index.
    :tocoordinate:  Converts the input into the coordinate (rank, file).
    :tovector:      Converts the input into a vector define by core.Vector with
                    the x-component being the rank and the y-component being the
                    file.

    :return:        The input but in the forced form.

    EXAMPLES
    ======================
    How this function works on a basic level, input the square 'b1' as an index:
        >>> print core.convert(9, tocoordinate=True)
        >>> (1, 1)

        >>> print core.convert((1, 1), toindex=True)
        >>> 9

    Using the tovector parameter is harder to observe (as it is just a class):
        >>> print core.convert(9, tovector=True) == vector.Vector(1, 1)
        >>> True  # An equivalent call

        >>> a = core.convert(10, tovector=True)  # (1, 2)
        >>> b = core.convert(25, tovector=True)  # (3, 1)
        >>> print a + b
        >>> (4, 3)
    """
    # Sanity checks.
    assert any([tocoordinate, toindex, tovector]), \
        "Specify the output using the optional arguments."
    assert onlyone([tocoordinate, toindex, tovector]), \
        "The output is only a coordinate, vector or an index, not multiple."

    # Define functions
    def isindex(x):
        return isinstance(x, int)
    def iscoordinate(x):
        return (isinstance(x, (tuple, list)) and len(x) == 2)
    def isvector(x):
        return isinstance(x, Vector)

    # Convert to desired form:
    x = indexorcoordinateorvector  # Shorthand notation.
    if tocoordinate:  # Convert to coordinate.
        if isindex(x):
            return (x/8, x % 8)
        elif isvector(x):
            return x.tupleform()
        elif iscoordinate(x):
            return x
    elif toindex:  # Convert to index.
        if isindex(x):
            return x
        elif isvector(x):
            x = x.tupleform()
            return x[0]*8 + x[1]
        elif iscoordinate(x):
            return x[0]*8 + x[1]
    elif tovector:  # Convert to vector.
        if isindex(x):
            return Vector(x/8, x % 8)
        elif iscoordinate(x):
            return Vector(*x)
        elif isvector(x):
            return x
    else:
        raise TypeError("Passed item is none of the allowed options.")
    # If x isn't a vector, index or coordinate:
    raise TypeError("The item to be converted isn't a valid type.")
    return None

def convertlist(lst, **kwargs):
    """Same call as convert but for a list. Basically, a shortcut call."""
    return map(lambda x: convert(x, **kwargs), lst)

def readablelistof(lst):
    """Calls the __str__ method of classes, but structures it traditionally."""
    string = ''
    for item in lst:
        string += str(item) + ', '
    return '[' + string[:-2] + ']'


 ####### #     #  #####  ####### ######  ####### ### ####### #     #  #####
 #        #   #  #     # #       #     #    #     #  #     # ##    # #     #
 #         # #   #       #       #     #    #     #  #     # # #   # #
 #####      #    #       #####   ######     #     #  #     # #  #  #  #####
 #         # #   #       #       #          #     #  #     # #   # #       #
 #        #   #  #     # #       #          #     #  #     # #    ## #     #
 ####### #     #  #####  ####### #          #    ### ####### #     #  #####


class IllegalMoveError(IndexError):
    """Called if the move is illegal for any reason."""

    def __init__(self, errormsg=None):
        if errormsg == None:
            errormsg = "The move supplied is not valid."
        IndexError.__init__(self, errormsg)

class ColourError(TypeError):
    """Raised if the colour specified isn't either white or black."""

    def __init__(self, errormsg=None):
        if errormsg == None:
            errormsg = "The colours of the players are either white or black."
        TypeError.__init__(self, errormsg)

class UnknownPieceError(TypeError):
    """The piece passed is unknown (not in 'RNBQK')."""

    def __init__(self, errormsg=None):
        if errormsg == None:
            errormsg = "I don't know the piece passed."
        TypeError.__init__(self, errormsg)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
