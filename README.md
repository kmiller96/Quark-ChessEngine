# Quark - A Python Based Chess Engine

Welcome! This is Quark, a chess engine with the main aim of not beating Magnus, or even an amateur, but being able to play by itself. Currently it is a one-man-show running as a hobby project.

The engine is split up into two main components: the front-end and the back-end.

### The Front-End
The front end is what the user interacts with. In the front end there is currently a ASCII art GUI which renders the board plus a UI so that the user isn't manually changing the board state themselves. The UI will eventually work solely on traditional chess notation rules but currently it works on a special set of notational rules, which are outlined later on in this README.

### The Back-End
In the back-end there is a complete chessboard, with rules, built from scratch. This engine uses a mailbox approach to storing the board state with 64 holes, each representing a single square on the board like so:

<!-- language: lang-none -->
    +---------------------------------------+
    | 56 | 57 | 58 | 59 | 60 | 61 | 62 | 63 |
    +---------------------------------------+
    | 48 | 49 | 50 | 51 | 52 | 53 | 54 | 55 |
    +---------------------------------------+
    | 40 | 41 | 42 | 43 | 44 | 45 | 46 | 47 |
    +---------------------------------------+
    | 32 | 33 | 34 | 35 | 36 | 37 | 38 | 39 |
    +---------------------------------------+
    | 24 | 25 | 26 | 27 | 28 | 29 | 30 | 31 |
    +---------------------------------------+
    | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 |
    +---------------------------------------+
    | 08 | 09 | 10 | 11 | 12 | 13 | 14 | 15 |
    +---------------------------------------+
    | 00 | 01 | 02 | 03 | 04 | 05 | 06 | 07 |
    +---------------------------------------+

However the engine is not required to work in indices.

Auxiliary to the engine, a class for vectors have been defined and used extensively in the methods and calculations of the engine. They behave mostly as 2D mathematical vectors, with sutble changes to methods to make them applicable to the engine. One example of this behaviour is in determing unit vectors; for a vector at a 45 degree bearing instead of making the unit vector (1/sqrt(2), 1/sqrt(2)) it is scaled up by sqrt(2) so that the indices are only integers, making it (1, 1). 

The chess pieces are all individual classes that have their own specialised methods. They determine their moves using [vector attack](https://chessprogramming.wikispaces.com/Vector+Attacks) logic and uses the vector class for its mathematical grounding.

The search-and-evaluate part of the engine is currently being developed, and as such has no information pertaining to its inner workings yet.

## Why bother? Isn't there already lots of chess engines, ones that are better then yours?

My response to that question is why bother ever doing anything? It is done half as a hobby and half as a way to learn how large-scale projects behave. I am yet to write a program larger then 500 lines of code so I do not know yet what goes wrong when doing so.

Don't expect this engine to ever beat anyone with half a brain in chess. I am hoping at best that it can play a game without breaking any rules.

## Examples

The GUI currently looks like so:
<!-- language: lang-none -->
    +----------+
    | rnbqkbnr |
    | pppppppp |
    | ........ |
    | ........ |
    | ........ |
    | ........ |
    | PPPPPPPP |
    | RNBQKBNR |
    +----------+

where the capitalised pieces are on white while the lowercase pieces are on black.

The notational rules follow a format similar to traditional chess notation but with a bit more detail. Two examples of moves under the special notation would be "Qd1->a4" or "e4xd5" if this helps to make a bit more sense. A concrete set of rules are as follows:
  - Start with the symbol for the piece being moved. So the queen has "Q", the king has "K", the knight "N", the bishop "B", the rook "R" and the pawns have no special symbol.
  - Add on the current position of the piece (e.g. e3)
  - If just moving, write '->'. If capturing write 'x'
  - Finish the notation with the final position.

The special symbols being used are identical to traditional chess:
  - If the piece has caused check, start the move with '+'
  - If the piece has caused checkmate, start the move with '#'
  - If castling, use either 0-0 for kingside or 0-0-0 for queenside.
  - Pawn promotions add to the end of the note '=?' where the ? symbol represents the symbol of the newly promoted piece.

## API Reference

Currently there is no API, but it will be added as the project progresses further.

## Tests

Under each individual method, class and function there are both unit tests and integrated tests to make sure that they are behaving in a sane manner. For more details of the tests written, please see the python scripts in the "tests" directory.

## Contributors

If you would like to contribute to the project, please visit one of the main contributor's accounts and send them and email. We are always happy for more help.

## License

This project is covered under the MIT license.
