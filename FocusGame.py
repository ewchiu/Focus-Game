# Eric Chiu
# 11/11/20
# This program contains all classes and methods to simulate the Focus board game in Python.
# Contains FocusGame class, and Player and Board classes that are compositions of the FocusGame class
# FocusGame class contains methods for the main functionality of the game
# Board class contains methods to initialize and populate the game board for Focus
# Player class contains private data members that represent attributes required to play Focus

class Board:
    """
    Initializes and represents a game board that is used in the FocusGame class
    Contains methods to fill the game board with markers at the initial positions
    Player's markers are represented by strings and taken from the Player class
    """

    def __init__(self, p1_marker, p2_marker):
        """
        Initializes a Board object for the Focus game that consists of a list of lists representing a 6x6 game board
        Uses list comprehension and for loops to generate the list of lists
        There is one main list, with 6 lists that represent rows, and each one of those 6 lists will have
        6 lists containing the player's marker pieces
        Calls a method to fill the board with markers at their initial position
        """
        self._board = [[] for row in range(6)]

        # initializing empty board
        for row in self._board:
            for i in range(6):
                row.append([])

        # fill board with player markers taken from parameters
        self.fill_board(p1_marker, p2_marker)

    def fill_board(self, p1_marker, p2_marker):
        """
        Takes markers for both players as parameters
        Fills board with markers in initial starting positions
        This is achieved by iterating through the board, which is a list of lists, in increments of 2
        And adding 1 of each player's markers to each empty space, 2 spaces at a time
        The player markers being placed are alternated using a boolean value that is changed with every step
        """
        player = True

        # loop to iterate and fill board with each players markers, alternating every 2 positions
        for row in self._board:
            for i in range(0, len(row), 2):

                # uses boolean to keep track of which player's markers to fill
                if player:
                    marker = p1_marker
                else:
                    marker = p2_marker

                row[i].append(marker)
                row[i + 1].append(marker)
                player = not player

    def get_board(self):
        """
        Returns the Board and the current state of its markers
        """
        return self._board


class Player:
    """
    Represents a player object that is a part of the FocusGame object
    Contains methods for initializing the object and getter methods to retrieve their data members
    The getter methods are mainly used by the FocusGame class to access the private data members of the Player object
    """

    def __init__(self, new_player):
        """
        Takes a tuple as a parameter, with the first item in the tuple containing a str representing the player name
        and the second item in the tuple containing a str representing the player's chosen marker for the game
        The string with the player's marker is what will be placed on the Board object when it is initialized
        Initializes a Player object with its private data members, including captured and reserve data members
        that track how many captured and reserved pieces each player has at any point in the game
        """
        self._name = new_player[0]
        self._marker = new_player[1]
        self._captured = 0
        self._reserve = 0

    def get_name(self):
        """
        Returns value of player's name
        """
        return self._name

    def get_marker(self):
        """
        Returns value of Player's marker
        """
        return self._marker

    def get_captured(self):
        """
        Returns amount of player's captured pieces
        """
        return self._captured

    def get_reserve(self):
        """
        Returns amount of player's reserved pieces
        """
        return self._reserve

    def inc_captured(self):
        """
        Increments amount of player's captured pieces by 1
        """
        self._captured += 1

    def inc_reserve(self):
        """
        Increments amount of player's reserve pieces by 1
        """
        self._reserve += 1

    def dec_reserve(self):
        """
        Decrements amount of player's reserve pieces by 1
        """
        self._reserve -= 1


class FocusGame:
    """
    Represents a FocusGame object that has FocusBoard and Player objects classes
    Utilizes these objects and methods within this class to run a game of Focus
    Contains methods to play the Focus game, including initializing the relevant objects by calling Board and Player
    classes, move pieces, check wins, and showing pieces on the game board
    """

    def __init__(self, player1, player2):
        """
        Takes 2 tuples as parameters, strings each containing player name and marker
        Initializes all private data members of FocusGame object
        Calls the Board class to initialize the game board with the player markers passed as arguments
        Calls the Player class to initialize Player objects with the requested name and markers in the tuples
        """
        self._turn = 0

        self._p1 = Player(player1)
        self._p2 = Player(player2)
        self._players = (self._p1, self._p2)

        self._board = Board(self._p1.get_marker(), self._p2.get_marker())

    def get_turn(self):
        """
        Returns value of turn private data member
        """
        return self._turn

    def inc_turn(self):
        """
        Increments value of turn private data member by 1
        """
        self._turn += 1

    def get_board(self):
        """
        Returns Board object associated with FocusGame
        """
        return self._board.get_board()

    def get_player_from_name(self, name):
        """
        Searches tuple that contains Players
        Returns Player object that matches name parameter
        """
        for player in self._players:
            if name == player.get_name():
                return player

    def move_piece(self, name, start_pos, end_pos, num):
        """
        Takes a player name, starting position, destination position, and number of pieces to move as parameters
        Calls methods to verify whether requested move was legal; if not, an error message is returned
        Moves the requested amount of pieces by popping the markers from the list at the start position
        and appending them to the list at the destination position
        Then calls methods to fill in empty positions with empty strings, validate that the win condition has
        been achieved, captures/reserves pieces if stack at destination contains more than 5 markers
        Lastly, increments the turn and returns message stating pieces were successfully moved
        """
        # validates move is legal, if not returns error message
        valid = self.move_validation(name, start_pos, end_pos, num)
        if not valid:
            return False

        # pop the pieces from list at source and append them to destination list
        start = self.show_pieces(start_pos)
        end = self.show_pieces(end_pos)
        length = len(start)

        for i in range(length - num, length):
            end.append(start.pop(length - num))

        # fills in start_pos with empty piece if necessary
        self.empty_pos(start_pos)

        # calls method to validate win condition
        if self.validate_win(self.get_player_from_name(name)):
            return 'Wins'

        # calls method to check end_pos to see if len(stack) > 5, and if so captures/reserves pieces
        self.five_stack(name, end_pos)

        self.inc_turn()
        return 'successfully moved'

    def move_validation(self, name, start_pos, end_pos, num):
        """
        Takes player name, start & end position, and number of pieces to move as parameters
        Calls methods to validate that the move is made on the correct turn, the move is valid for the number
        of pieces entered, and that the position the pieces start and end at are valid
        Will return a string message if these conditions are not met
        """
        # validates correct player is making a move during current turn
        if not self.validate_turn(name):
            return False
        # validates number of pieces entered
        elif not self.validate_num_pieces(start_pos, num):
            return False
        # validates source and destination positions are legal
        elif not self.validate_pos(name, start_pos, end_pos, num):
            return False
        else:
            return True

    def validate_turn(self, name):
        """
        Takes a player name as parameter
        Validates that the player name matches the player whose turn it is
        First player's turn when value of self._turn is even or 0
        Second player's turn when value of self._turn is odd
        Returns boolean based on if the player name matches the player whose turn it is
        """
        # 0 or even amount turns are reserved for p1, if turns is odd then p2 turn
        if self.get_turn() % 2 == 0 and name == self._p1.get_name():
            return True
        elif self.get_turn() % 2 != 0 and name == self._p2.get_name():
            return True
        else:
            return False

    def validate_pos(self, name, start_pos, end_pos, num):
        """
        Takes player name, start & end position, and number of pieces to move as parameters
        Validates that the start position has a marker on top of the stack that matches the player's marker
        Verifies that the end position is valid given the direction of movement and number of pieces moved
        Returns a boolean value depending on whether or not the starting position is legal
        """
        # checks to see that positions are valid coordinates on the board
        if start_pos[0] not in range(0,6) or start_pos[1] not in range(0, 6):
            return False
        elif end_pos[0] not in range(0, 6) or end_pos[1] not in range(0, 6):
            return False

        # checks top piece of stack matches player's marker
        pieces = self.show_pieces(start_pos)
        top_piece = pieces[len(pieces) - 1]
        player = self.get_player_from_name(name)

        if top_piece != player.get_marker():
            return False

        # checks to see that distance to end_pos does not exceed number of pieces to move
        horizontal = abs(end_pos[0] - start_pos[0])
        vertical = abs(end_pos[1] - start_pos[1])

        if horizontal == num or vertical == num:
            # checks to see that pieces are not moved diagonally
            if start_pos[0] != end_pos[0] and start_pos[1] != end_pos[1]:
                return False
            else:
                return True

        return False

    def validate_num_pieces(self, start_pos, num):
        """
        Takes a number of pieces as parameter
        Returns boolean value based on whether or not the number of pieces does not exceed
        the number of markers at start_pos
        Also validates that if x > 1, and x amount of pieces are moved in a turn, that the stack is moved
        to exactly x spaces away from the start position
        """
        # Checks to see that num does not exceed number of markers at position
        stack = self.show_pieces(start_pos)

        if num not in range(1, len(stack) + 1):
            return False

        # Verifies num pieces to move == distance moved
        pass

        return True

    def empty_pos(self, pos):
        """
        Takes a position on the Focus Board as a parameter
        Checks to see if position on the board is empty, and if so changes it to empty str
        """
        pieces = self.show_pieces(pos)

        if len(pieces) == 0:
            pieces.append(' ')

    def five_stack(self, name, pos):
        """
        Takes a player's name and position on the Focus Board as a parameter
        Verifies stack at pos is more than 5 pieces, and if not exits method
        Will pop all pieces from bottom of stack until 5 pieces are left
        Player's pieces will be added to reserve, opponent's pieces will be added to captured
        """
        stack = self.show_pieces(pos)
        overflow = []
        player = self.get_player_from_name(name)
        player_marker = player.get_marker()

        if len(stack) <= 5:
            return

        for i in range(len(stack) - 5):
            overflow.append(stack.pop(0))

        for piece in overflow:
            if piece == player_marker:
                player.inc_reserve()
            else:
                player.inc_captured()

    def validate_win(self, player):
        """
        Win condition - when one player has captured 6 enemy pieces
        Returns boolean depending on whether win condition was achieved
        """
        if player.get_captured() >= 6:
            return True
        else:
            return False

    def show_pieces(self, pos):
        """
        Takes a tuple containing coordinates as a parameter
        Coordinates must be within (0,0) to (5.5)
        Returns a list containing the markers that are at that location on the board
        The bottom piece will be at the 0th index of the returned array
        """
        x = pos[0]
        y = pos[1]

        return self.get_board()[x][y]

    def show_reserve(self, name):
        """
        Takes a player name as a parameter and finds the corresponding Player object
        Returns amount of reserve pieces that player has
        """
        player = self.get_player_from_name(name)
        return player.get_reserve()

    def show_captured(self, name):
        """
        Takes a player name as a parameter and finds the corresponding Player object
        Returns amount of captured pieces that player has
        """
        player = self.get_player_from_name(name)
        return player.get_captured()

    def reserved_move(self, name, pos):
        """
        Takes a player's name and position on the board for the reserved piece as parameters
        Checks to see if the player has any reserve pieces, and returns error message if there are none
        If yes, the reserve piece is placed on the board at the requested location provided the location is valid
        Reduces the amount of reserve pieces the player has by 1
        """
        # validates player has reserve pieces
        player = self.get_player_from_name(name)

        if self.show_reserve(name) == 0:
            return False
        # validate location is valid
        elif pos[0] not in range(0,6) or pos[1] not in range(0, 6):
            return False

        # place the marker on the board at the requested pos,
        dest = self.show_pieces(pos)

        if dest == [' ']:
            dest[0] = player.get_marker()
        else:
            dest.append(player.get_marker())

        # calls method to check end_pos to see if len(stack) > 5, and if so captures/reserves pieces
        self.five_stack(name, pos)

        # dec amount of reserve pieces by 1, increments turn
        player.dec_reserve()
        self.inc_turn()
        return 'successfully moved'

    def print_board(self):
        """
        Prints the current state of the game board with player markers by iterating through each "row"
        of the FocusGame board and printing out the contents of each list at the row
        Used primarily for testing purposes to show the current status of the game board
        """
        board = self.get_board()

        for row in board:
            print(row)


if __name__ == '__main__':

    game = FocusGame(('PlayerA', 'R'), ('PlayerB', 'G'))
    print(game.move_piece('PlayerA', (0, 0), (0, 1), 1))  # Returns message "successfully moved"
    print(game.show_pieces((0, 1)))  # Returns ['R','R']
    print(game.show_captured('PlayerA'))  # Returns 0
    print(game.reserved_move('PlayerA', (0, 0)))  # Returns message "No pieces in reserve"
    print(game.show_reserve('PlayerA'))  # Returns 0
    game.print_board()
