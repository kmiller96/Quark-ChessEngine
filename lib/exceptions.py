# DESCRIPTION: Contains my custom exceptions.

class IllegalMoveError(IndexError):
    """Called if the move is illegal for any reason."""

    def __init__(self):
        IndexError.__init__(self, "The move supplied is not valid.")
