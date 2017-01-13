# DESCRIPTION: Contains my custom exceptions.

class IllegalMoveError(IndexError):
    """Called if the move is illegal for any reason."""

    def __init__(self):
        IndexError.__init__(self, "The move supplied is not valid.")

class ColourError(TypeError):
    """Raised if the colour specified isn't either white or black."""

    def __init__(self, errormsg=None):
        if errormsg == None:
            errormsg = "The colours of the players are either white or black."
        TypeError.__init__(self, errormsg)
