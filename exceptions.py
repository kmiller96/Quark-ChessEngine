# DESCRIPTION: Contains my custom exceptions.

# DEVELOPMENT LOG:
#    27/12/16: Initialized exceptions script. Added exception for illegal moves
# for specific pieces.

class IllegalMoveError(IndexError):
    """Called if the move is illegal for any reason."""

    def __init__(self):
        IndexError.__init__(self, "The move supplied is not valid.")
