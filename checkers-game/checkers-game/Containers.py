import Logic as GL

class PotentialMove:
    
    def __init__(self, start_vec, end_vec, captured=None):
        """
        initial
        :param start_vec:
        :param end_vec:
        :param captured:
        """
        self.start_vec = start_vec
        self.end_vec = end_vec
        self.captured = captured
    
    def __eq__(self, other):
        """
        equal
        :param other:
        :return:
        """
        if type(other) is tuple:
            return self.start_vec == other[0] and self.end_vec == other[1]
        assert type(other) is PotentialMove
        return self.start_vec == other.start_vec and self.end_vec == other.end_vec
    
    def __str__(self):
        return '<PotentialMove | start: ' + str(self.start_vec) + ' end: ' + str(self.end_vec) + 'captured: ' + str(self.captured) + '>'
    
    def __repr__(self):
        return '<PotentialMove | start: ' + str(self.start_vec) + ' end: ' + str(self.end_vec) + 'captured: ' + str(self.captured) + '>'

class PendingMove:

    def __init__(self, board, player):
        """
        initial
        :param board:
        :param player:
        """
        self.board = board
        self.start_vec = None
        self.end_vec = None
        self.player = player
        self.captured = None
    
    def set_start(self, vec):
        """
        set the start vector
        :param vec:
        :return:
        """
        self.start_vec = vec

    def set_end(self, vec):
        """
        set the end vector
        :param vec:
        :return:
        """
        self.end_vec = vec

    def is_valid(self):
        """
        make sure the next moving of the piece is valid
        :return: True, False
        """
        if self.start_vec is None or self.end_vec is None:
            return False

        start_piece = GL.get_piece(self.board, self.start_vec)
        end_piece = GL.get_piece(self.board, self.end_vec)

        if GL.get_team(start_piece) != self.player: # make sure you're moving your own pieces
            return False
        if end_piece != GL.EMPTY: #must move to an empty square
            return False
        
        move_tup = (self.start_vec, self.end_vec)

        temp = GL.get_potential_moves(self.board, self.start_vec) #get the availabe position for next

        for potential_move in temp:
            if potential_move == move_tup:
                self.captured = potential_move.captured
                if GL.can_capture(self.board, self.player) and not self.captured: #whether the piece can be captured or not
                    return False
                return True

        return False
    
    def reset(self):
        """
        reset the params of start,end vector and captured
        :return:
        """
        self.start_vec = None
        self.end_vec = None
        self.captured = None
    
    def switch_player(self):
        """
        switch of AI and player
        :return:
        """
        self.player *= -1
        self.reset()

class Vector2:

    def __init__(self, x, y):
        """
        initial
        :param x:
        :param y:
        """
        self.x = x
        self.y = y
    
    def __add__(self, other):
        """
        add x, y to the vector
        :param other:
        :return: Vector2
        """
        assert type(other) is Vector2
        return Vector2(self.x+other.x, self.y+other.y)
    
    def __radd__(self, other):
        """
        if vector has changed, it call the _add_ func and change the vector
        :param other:
        :return:
        """
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __eq__(self, other):
        """
        the vector equal
        :param other:
        :return:
        """
        assert type(other) is Vector2
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return '<Vec2 | x: ' + str(self.x) + ' y: ' + str(self.y) + '>'
    
    def __repr__(self):
        return '<Vec2 | x: ' + str(self.x) + ' y: ' + str(self.y) + '>'