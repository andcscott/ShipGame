# Author: Andrew Scott
# Date: 2022-03-04
# Description: Allows two people to play the ShipGame. Each player has their own
#              10x10 grid on which they place their ships. On their turn, each
#              player can fire a torpedo at a square on the enemy's grid. Player
#              'first' gets the first turn to fire a torpedo, after which
#              players alternate. A ship is sunk when all of its squares have
#              been hit. When a player sinks their opponent's final ship, they
#              win.

class Ship():
    """Represents a ship in the ShipGame."""

    def __init__(self, player, length, coords, orientation):
        """Constructor for the Ship class. All data members are private.

        Parameters
        ----------
        player : obj
            The player object that owns the ship ('first' or 'second')
        length : int
            The length of the ship
        coords : str
            Coordinates of the square closest to A1 that the ship will occupy
        orientation : str
            'R' if the ships squares occupy the same row, or 'C' if its squares
            occupy the same column
        """

        self._player = player
        self._length = length
        self._coords = coords
        self._orientation = orientation
        self._squares = []
        self._hits = set()

        if coords[0] == 'A':
            self._indices = '0' + str(int(coords[1]) - 1)
        elif coords[0] == 'B':
            self._indices = '1' + str(int(coords[1]) - 1)
        elif coords[0] == 'C':
            self._indices = '2' + str(int(coords[1]) - 1)
        elif coords[0] == 'D':
            self._indices = '3' + str(int(coords[1]) - 1)
        elif coords[0] == 'E':
            self._indices = '4' + str(int(coords[1]) - 1)
        elif coords[0] == 'F':
            self._indices = '5' + str(int(coords[1]) - 1)
        elif coords[0] == 'G':
            self._indices = '6' + str(int(coords[1]) - 1)
        elif coords[0] == 'H':
            self._indices = '7' + str(int(coords[1]) - 1)
        elif coords[0] == 'I':
            self._indices = '8' + str(int(coords[1]) - 1)
        elif coords[0] == 'J':
            self._indices = '9' + str(int(coords[1]) - 1)


    def get_player(self):
        """Get the player who owns the ship.

        Returns
        -------
        str
            Either 'first' or 'second'
        """

        return self._player

    def get_length(self):
        """Get the ships length.

        Returns
        -------
        int
            The length of the ship
        """

        return self._length

    def get_indices(self):
        """Get the square occupied by the ship closes to A1 as a 2-digit string.

        Returns
        -------
        str
            2-digit string representing the square the ship occupies on the grid
            closest to A1 (e.g 'A1' = '00')
        """

        return self._indices

    def get_coords(self):
        """Get the coordinates of the square occupied by the ship closest to A1.

        Returns
        -------
        str
            The coordinates (e.g. 'B7')
        """

        return self._coords

    def get_orientation(self):
        """Get the ships orientation.

        Returns
        -------
        str
            'R' if the ships squares occupy the same row, or 'C' if its squares
            occupy the same column
        """

        return self._orientation

    def get_hits(self):
        """Get the number of hits recorded against a ship.

        Returns
        -------
        int
            The number of times the ships has been hit
        """

        return self._hits

    def get_squares(self):
        """Get the squares occupied by the ship.

        Returns
        -------
        list
            List of 2-digit strings representing squares occupied by the ship
            (e.g 'A1' = '00')
        """

        return self._squares

    def set_squares(self, squares):
        """Set the squares occupied by the ship.

        Parameters
        ----------
        squares : list
            List of 2-digit strings representing squares occupied by the ship
            (e.g 'A1' = '00')
        """

        self._squares = squares

    def add_hit(self, index):
        """Records when the ship is hit. A hit only counts once per square.

        Parameters
        ----------
        index : str
            2-digit string representing the square on the grid to add
            (e.g coordinate 'A1' = index '00')
        """

        self._hits.add(index)

    def is_sunk(self):
        """Checks if the ship was sunk.

        Returns
        -------
        bool
            True if the ship was sunk, otherwise False
        """

        if len(self._squares) == len(self._hits):
            return True
        return False

class Board():
    """Represents each players board for the ShipGame class."""

    def __init__(self, player):
        """Constructor for the Board class. All data members are private.

        Parameters
        ----------
        player : str
            Either 'first' or 'second'
        """

        self._player = player
        self._rows = 10
        self._columns = 10
        self._grid = [[' ' for r in range(self._rows)] for c in range(self._columns)]

    def render(self):
        """Prints the current state of the board to the terminal"""

        print('\n  1 2 3 4 5 6 7 8 9 10')

        column_char = 'A'
        for column in self._grid:
            output = str()
            for item in column:
                output += item
            print(column_char, ' '.join(output))
            column_char = chr(ord(column_char) + 1)

    def check_hit(self, index):
        """Checks the grid for a hit.

        Parameters
        ----------
        index : str
            2-digit string representing the square on the grid to check for a hit
            (e.g coordinate 'A1' = index '00')
        """

        try:
            location = self._grid[int(index[0])][int(index[1])]
        except:
            return False
        if location != ' ':
            return True
        return False

    def is_valid(self, ship):
        """Determines whether a position requested for ship placement is valid.

        Uses the current state of the board to determine whether or not the
        coordinates and orientation passed to the ShipGame's place_ship method
        represent a valid move.

        Parameters
        ----------
        ship : obj
            The ship that needs to be validated

        Returns
        -------
        bool
            True if coordinates are valid, otherwise false
        """

        length = ship.get_length()
        orientation = ship.get_orientation()
        location = ship.get_indices()
        column = int(location[0])
        row = int(location[1])

        try:
            if orientation == 'R':
                for index in range(length):
                    if self._grid[column][row] != ' ':
                        return False
                    row += 1
                return True
            if orientation == 'C':
                for index in range(length):
                    if self._grid[column][row] != ' ':
                        return False
                    column += 1
                return True
        except:
            return False

    def add_ship(self, ship):
        """Called by ShipGame's place_ship method to add a ship to the grid.

        Parameters
        ----------
        ship : obj
            A Ship object

        Returns
        -------
        ship_squares : list
            List of 2-digit strings representing squares occupied by the ship
            (e.g 'A1' = '00')
        """

        length = ship.get_length()
        orientation = ship.get_orientation()
        location = ship.get_indices()
        column = int(location[0])
        row = int(location[1])

        if orientation == 'R':
            ship_squares = []
            for index in range(length):
                self._grid[column][row] = str(length)
                ship_squares.append(str(column) + str(row))
                row += 1
            return ship_squares
        if orientation == 'C':
            ship_squares = []
            for index in range(length):
                self._grid[column][row] = str(length)
                ship_squares.append(str(column) + str(row))
                column += 1
            return ship_squares

class ShipGame():
    """Represents the game ShipGame. Uses Board and Player classes."""

    def __init__(self):
        """Constructor for the ShipGame class. All data members are private."""

        self._player1 = 'first'
        self._player2 = 'second'
        self._board1 = Board(self._player1)
        self._board2 = Board(self._player2)
        self._player1_ships_dict = dict()
        self._player2_ships_dict = dict()
        self._current_state = 'UNFINISHED'
        self._current_turn = self._player1

    def place_ship(self, player, length, coords, orientation):
        """Places a ship on the player's board.

        If a ship would not fit entirely on that player's board, if it would
        overlap any previously placed ships, or if the length of the ship is
        less than 2 the ship will not be added.

        Parameters
        ----------
        player : str
            Either 'first' or 'second'
        length : int
            The length of the ship
        coords : str
            Coordinates of the square closest to A1 that the ship will occupy
        orientation : str
            'R' if the ships squares occupy the same row, or 'C' if its squares
            occupy the same column

        Returns
        -------
        bool
            True if the ship is added, False if it cannot be added
        """

        if length < 2:
            return False
        if length > 10:
            return False

        ship = Ship(player, length, coords, orientation)
        if player == 'first':
            board = self._board1
            if board.is_valid(ship):
                squares = board.add_ship(ship)
                self._player1_ships_dict[coords] = ship
                ship.set_squares(squares)
                return True
            return False
        if player == 'second':
            board = self._board2
            if board.is_valid(ship):
                squares = board.add_ship(ship)
                self._player2_ships_dict[coords] = ship
                ship.set_squares(squares)
                return True
            return False

    def get_current_state(self):
        """Get the current state of the game.

        Returns
        -------
        str
            'FIRST_WON', 'SECOND_WON', or 'UNFINISHED'
        """

        return self._current_state

    def fire_torpedo(self, player, coords):
        """Fires a torpedo at the enemy ships.

        Records the move, updates whose turn it is, and updates the current
        state of the game if the move resulted in a win.

        Parameters
        ----------
        player : str
            Either 'first' or 'second'
        coords : str
            Coordinates of the target square (e.g. 'B7')

        Returns
        -------
        bool
            False when the game is already over or it's not the players turn,
            otherwise True
        """

        if self._current_state != 'UNFINISHED' or self._current_turn != player:
            return False

        index = ''
        if coords[0] == 'A':
            index = '0' + str(int(coords[1]) - 1)
        elif coords[0] == 'B':
            index = '1' + str(int(coords[1]) - 1)
        elif coords[0] == 'C':
            index = '2' + str(int(coords[1]) - 1)
        elif coords[0] == 'D':
            index = '3' + str(int(coords[1]) - 1)
        elif coords[0] == 'E':
            index = '4' + str(int(coords[1]) - 1)
        elif coords[0] == 'F':
            index = '5' + str(int(coords[1]) - 1)
        elif coords[0] == 'G':
            index = '6' + str(int(coords[1]) - 1)
        elif coords[0] == 'H':
            index = '7' + str(int(coords[1]) - 1)
        elif coords[0] == 'I':
            index = '8' + str(int(coords[1]) - 1)
        elif coords[0] == 'J':
            index = '9' + str(int(coords[1]) - 1)

        if player == 'first':
            board = self._board2
            ships_dict = self._player2_ships_dict
            if board.check_hit(index):
                for key in ships_dict:
                    ship = ships_dict[key]
                    if index in ship.get_squares():
                        ship.add_hit(index)
                        if ship.is_sunk():
                            del ships_dict[key]
                            ships_remaining = self.get_num_ships_remaining('second')
                            if ships_remaining == 0:
                                self._current_state = 'FIRST_WON'
                            return True
            self._current_turn = 'second'
        if player == 'second':
            board = self._board1
            ships_dict = self._player1_ships_dict
            if board.check_hit(index):
                for key in ships_dict:
                    ship = ships_dict[key]
                    if index in ship.get_squares():
                        ship.add_hit(index)
                        if ship.is_sunk():
                            del ships_dict[key]
                            ships_remaining = self.get_num_ships_remaining('first')
                            if ships_remaining == 0:
                                self._current_state = 'SECOND_WON'
                            return True
            self._current_turn = 'first'
        return True

    def get_num_ships_remaining(self, player):
        """Get how many ships a player has left.

        Parameters
        ----------
        player : str
            Either 'first' or 'second'

        Returns
        -------
        int
            How many ships the specified player has left
        """

        if player == 'first':
            return len(self._player1_ships_dict.keys())
        if player == 'second':
            return len(self._player2_ships_dict.keys())
