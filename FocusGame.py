# Author: Joseph Coiffman
# Date: 11/27/2020
# Description: portfolio project,playing an abstract board game called Focus/Domination. see the rules
# https://en.wikipedia.org/wiki/Focus_%28board_game%29
# we are playing the two person game, and once someone captures 6 pieces they win

class Player:
    """This class holds a player's name, piece color, how many captured and how many reserved pieces they have."""
    def __init__(self, _name, _color):
        self._name = _name
        self._color = _color
        self._captured = 0
        self._reserved = 0

    def get_name(self):
        return self._name

    def get_color(self):
        return self._color

    def get_captured(self):
        return self._captured

    def get_reserved(self):
        return self._reserved

    def add_to_captured(self):
        self._captured += 1

    def add_to_reserved(self):
        self._reserved += 1

    def remove_from_reserved(self):
        self._reserved -= 1





class FocusGame:
    """The board will be a list of lists, 6 X 6, each position will contain the players color on that position
     has object to help player make a move and returns the appropriate response"""
    def __init__(self, _player1=list, _player2=list):
        self._player1 = Player(_player1[0], _player1[1])
        self._player2 = Player(_player2[0], _player2[1])
        self._board = [[[_player1[1]], [_player1[1]], [_player2[1]], [_player2[1]], [_player1[1]], [_player1[1]]],
                       [[_player2[1]], [_player2[1]], [_player1[1]], [_player1[1]], [_player2[1]], [_player2[1]]],
                       [[_player1[1]], [_player1[1]], [_player2[1]], [_player2[1]], [_player1[1]], [_player1[1]]],
                       [[_player2[1]], [_player2[1]], [_player1[1]], [_player1[1]], [_player2[1]], [_player2[1]]],
                       [[_player1[1]], [_player1[1]], [_player2[1]], [_player2[1]], [_player1[1]], [_player1[1]]],
                       [[_player2[1]], [_player2[1]], [_player1[1]], [_player1[1]], [_player2[1]], [_player2[1]]]]

        self._player_turn = None
        self._players = [self._player1, self._player2]
        self._is_win = False



    def move_piece(self, player_name=str, move_from=tuple, move_to=tuple, number_of_pieces=int):
        """will first make sure that the game is not over, then make sure that is it that players turn,
        then make sure it is a valid location that the player is moving to or from.
        Finally, it will update the board to reflect the move, update the captured and reserved pieces,
        and check if anyone won."""
        if self._is_win is True:
            return False
        for player in self._players:
            if player.get_name() == player_name:  # makes  sure player is referring to the correct player
                if self.check_turn(player_name) is False:
                    return "not your turn"
                if self.check_valid_location(player_name, move_from, move_to, number_of_pieces) is False:
                    return 'invalid location'
                if number_of_pieces > len(self._board[move_from[0]][move_from[1]]):  # moving too many pieces
                    return 'invalid number of pieces'
                add_list = []
                for piece in range(number_of_pieces):  # going to update the board
                    add_list += self._board[move_from[0]][move_from[1]]
                    self._board[move_from[0]][move_from[1]] = self._board[move_from[0]][move_from[1]][:-1]
                for piece in add_list[::-1]:
                    self._board[move_to[0]][move_to[1]].append(piece)
                self.capture_and_reserve(player_name, move_to)
                if self.check_win(player_name) is True:
                    return player_name + " Wins"
                self.change_turn()
                return 'successfully moved', self.print_board()

    def print_board(self):
        """ prints the board"""
        for x in self._board:
            print(x)
        print()
        print()

    def check_valid_location(self, player_name, move_from, move_to, number_of_pieces):
        """ Checks to see if player is making a valid move"""
        for player in self._players:
            if player.get_name() == player_name:
                if move_from[0] >= 6 or move_from[0] < 0 or move_from[1] >= 6 or move_from[1] < 0 or move_to[0] >= 6 or\
                        move_to[0] < 0 or move_to[1] >= 6 or move_to[1] < 0:   #makes sure valid place
                    return False
                if self.top_of_stack(move_from) != player.get_color():  # makes sure player is moving from a place
                    return False                                        # that has his piece on top.
                if not (move_to[0] == move_from[0] or move_to[1] == move_from[1]):  # makes sure not moving diagonally.
                    return False
                if move_to[0] != move_from[0]:
                    if move_from[0] + number_of_pieces != move_to[0] and move_from[0] - number_of_pieces != move_to[0]:
                        return False  # Makes sure only moving the correct amount
                if move_to[1] != move_from[1]:
                    if move_from[1] + number_of_pieces != move_to[1] and move_from[1] - number_of_pieces != move_to[1]:
                        return False  # Makes sure only moving the correct amount
                return True

    def top_of_stack(self, position):
        """returns the piece that is on top of the stack"""
        if self._board[position[0]][position[1]] == []:
            return self._board[position[0]][position[1]]
        else:
            return self._board[position[0]][position[1]][-1]

    def check_turn(self, player_name):
        """checks if it is player_name's turn."""
        for player in self._players:
            if player.get_name() == player_name:
                if self._player_turn is None:
                    self._player_turn = player_name

                if self._player_turn == player_name:
                    return True
                else:
                    return False

    def change_turn(self):
        """ changes the turn"""
        for player in self._players:
            if player.get_name() != self._player_turn:
                self._player_turn = player.get_name()
                return None

    def check_win(self, player_name):
        """ will check capture for player_name and see if someone won"""
        for player in self._players:
            if player.get_name() == player_name:
                if player.get_captured() >= 6:
                    self._is_win = True
                    return True
                else:
                    return False

    def capture_and_reserve(self, player_name, move_to):
        """checks the move_to, and checks how many pieces there are in that place, if more then 5
        then updates the captured and the reserved for that player."""
        for player in self._players:
            if player.get_name() == player_name:
                while len(self._board[move_to[0]][move_to[1]]) > 5:
                    if self._board[move_to[0]][move_to[1]][0] == player.get_color():
                        player.add_to_reserved()
                    else:
                        player.add_to_captured()
                    self._board[move_to[0]][move_to[1]] = self._board[move_to[0]][move_to[1]][1:]

    def show_pieces(self, position):
        """takes the position and shows the color of the pieces starting with the bottom most"""
        return self._board[position[0]][position[1]]

    def show_reserve(self, player_name):
        """Takes player_name, and goes through get_captured_and_reserved, returns the players reserved,
         the list starts with the players name and reserved is the second list"""
        for player in self._players:
            if player.get_name() == player_name:
                return player.get_reserved()

    def show_captured(self, player_name):
        """Takes player_name, and goes through get_captured_and_reserved, returns the players reserved,
                 the list starts with the players name and captured is the first list"""
        for player in self._players:
            if player.get_name() == player_name:
                return player.get_captured()

    def reserved_move(self, player_name, position):
        """takes player's name and checks if the have pieces reserved by using get_captured_and_reserved,
        then checks change_turn, decrements reserved for that player.And adds another piece to the list at location."""
        for player in self._players:
            if player.get_name() == player_name:
                if self.check_turn(player_name) is False:
                    return "not your turn"
                if player.get_reserved() == 0:
                    return 'no pieces in reserve'
                self._board[position[0]][position[1]].append(player.get_color())
                self.capture_and_reserve(player_name, position)
                self.check_win(player_name)
                self.change_turn()
                player.remove_from_reserved()
                return 'successfully moved'



