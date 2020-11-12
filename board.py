from piece import Piece
# assume player 1 is white
# assume player 2 is red
class Board:
    def __init__(self):
        self.board = []
        self.moves = []
        self.player = 2
        self.rows = 8
        self.cols = 8

        self.player1Color = "white"
        self.player1ColorShort = "w"
        self.player1ColorKing = "W"
        self.player1Pieces = []

        self.player2Color = "red"
        self.player2ColorShort = "r"
        self.player2ColorKing = "R"
        self.player2Pieces = []

    
    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(self.rows):
            self.board.append([])
            for col in range(self.cols):
                if col % 2 == ((row +  1) % 2):
                    if row < 3: #top half - player 1
                        temp_piece = Piece(row, col, self.player1Color, self.player1ColorShort, self.player1ColorKing)
                        self.board[row].append(temp_piece)
                        self.player1Pieces.append(temp_piece)
                    elif row > 4: #bottom half - player 2
                        temp_piece = Piece(row, col, self.player2Color, self.player2ColorShort, self.player2ColorKing)
                        self.board[row].append(temp_piece)
                        self.player2Pieces.append(temp_piece)
                    else:
                        self.board[row].append(0)
                   
                else:
                    self.board[row].append(0)

    #print board with padding of nubers
    def print_board(self):
        print("   0 1 2 3 4 5 6 7")
        print("   _______________")
        for row in range(self.rows):
            print(row,end="| ")
            for col in range(self.cols):
                if self.board[row][col] == 0:
                    print(". ", end="")
                elif self.board[row][col].king:
                    print(self.board[row][col].colorKing, end=" ")
                else:
                    print(self.board[row][col].colorShort, end=" ")
            print("")
    
    #move a piece from before to after
    # needs:
    # clean up
    # check if move is valid
    # check if correct player piece is moving (white is moving white)
    def move(self,row,col, new_row,new_col):
        piece = self.board[row][col]
        #move the piece in pieces
        piece.move(new_row,new_col)
        #set new location to current piece
        self.board[new_row][new_col] = piece
        #set old position to free
        self.board[row][col] = 0

        #make it king if at end
        if self.player == 1 and new_row == self.rows-1:
            piece.make_king()
        elif self.player == 2 and new_row == 0:
            piece.make_king()

        #record the move
        self.moves.append([(row,col),(new_row,new_col)])

        #change turns
        self.change_turn()

    #change turn of play, should be called from move
    def change_turn(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    #return if speicied position is valid
    # no longer need i think
    def valid_position(self, row, col):
        return (row >= 0 and row <= self.rows) and (col >= 0 and col <= self.cols)

    #check who's turn it is to play
    def whose_turn(self):
        return self.player

    #check to see if there is a winner
    def has_winner(self):
        return len(self.player2Pieces) == 0 or len(self.player2Pieces) == 0
    
    #if there is no more pieces left return who won
    def get_winner(self):
        if len(self.player2Pieces) == 0:
            return "Player 1 is Winner"
        elif len(self.player2Pieces) == 0:
            return "Player 2 is Winner"

    #itterate over all pieces of player that is not captured
    #find moves it can make and save it a list
    #return list
    def get_all_valid_moves(self):
        all_moves = []
        if self.player == 1:
            for piece in self.player1Pieces:
                if not piece.captured:
                    all_moves.extend(self.get_valid_moves(piece.row, piece.col, piece.color))
        else:
            for piece in self.player2Pieces:
                if not piece.captured:
                    all_moves.extend(self.get_valid_moves(piece.row, piece.col, piece.color))
        return all_moves

    #given a piece find position it can move to
    #find places it can move to - an right
    def get_valid_moves(self,row,col, color):
        piece = self.board[row][col]
        if piece != 0:
            moves = []
            if self.player == 1 or piece.king:
                moves.extend(self._lookLeft(row, col,color)) #player 1 move down
                moves.extend(self._lookRight(row, col,color)) #player 1 move down

            if self.player == 2 or piece.king:
                moves.extend(self._lookLeft(row, col,color)) #player 2 move up
                moves.extend(self._lookRight(row, col,color)) #bottom piece move up
            
            if moves != []:
                return [([row,col],moves)]
        return []


    #seraches down left side of the board from given location
    #direction is where the piece will be moving towards
    #when it encounters a piece, not its own color, 
    #          check if it can to a empty spot after captring
    #   (need to implement recursive capturing)
    # -----in progress capture
    # after getting back where it can move, call get_valid_moves to recurse
    
    def _lookLeft(self,given_row,given_col,color, needEmpty = False):
        new_places = []
        #check the left side it can move to
        if self.player == 1 and given_row+1 < self.rows and given_col-1 >= 0:
            new_places.append((given_row+1,given_col-1)) #bottom left
        elif self.player == 2 and given_row-1 >= 0 and given_col-1 >= 0:
            new_places.append((given_row-1,given_col-1)) #top left
        
        #check if there is empty piece or enemy piece in the way
        valid_places = []
        check_capture = []
        for row,col in new_places:
            if self.board[row][col] == 0:
                valid_places.append((row,col))
            else:
                if not needEmpty and self.board[row][col].color != color:
                    check_capture.append((row,col))
        #if there is piece in the way, check if it can jump over to empty place
        for row,col in check_capture:
            valid_places.extend(self._lookLeft(row,col,color, True))

        return valid_places

    def _lookRight(self,given_row,given_col,color,needEmpty = False):
        #check the right side it can move to
        new_places = []
        if self.player == 1 and given_row+1 < self.rows and given_col+1 < self.cols:
            new_places.append((given_row+1,given_col+1)) #bottom right
        elif self.player == 2 and given_row-1 >= 0 and given_col+1 < self.cols:
            new_places.append((given_row-1,given_col+1)) #top right
        
        #check if there is empty piece or enemy piece in the way
        valid_places = []
        check_capture = []
        for row,col in new_places:
            if self.board[row][col] == 0:
                valid_places.append((row,col))
            else:
                if not needEmpty and self.board[row][col].color != color:
                    check_capture.append((row,col))
        #if there is piece in the way, check if it can jump over to empty place
        for row,col in check_capture:
            valid_places.extend(self._lookRight(row,col,color,True))

        return valid_places
    
    #given a move (current posititon, list of pieces with moves, index of piece, index of move)
    #will make the move, capture any piece in the way
    # given example:
    #    cur       new   |   cur      new      new   |    cur     new
    # [([1, 2], [(2, 1)]), ([3, 2], [(5, 0), (4, 3)]), ([1, 2], [(2, 1)])]
    def make_move(self,valid_moves,index_piece, index_move):
        #check if it has a piece location and move location
        move = valid_moves[index_piece]
        if len(move) != 2:
            return

        #get current piece location and move location
        row,col = move[0]
        new_row,new_col = move[1][index_move]
        
        #condition check to see if there is piece in the way we have to capture
        if abs(row-new_row) >1 or abs(col-new_col) > 1:
            print("---------------------------")
            print("Capturing")
            mid_row = (new_row+row)//2
            mid_col = (new_col+col)//2
            print(mid_row,mid_col )
            remove_piece = self.board[mid_row][mid_col]
            remove_piece.capture()
            self.board[mid_row][mid_col] = 0
            print("---------------------------")

        #move the piece
        self.move(row,col,new_row,new_col)

def main():
    board = Board()
    board.create_board()
    board.print_board()


    #red
    print("Player:",board.whose_turn())
    x = board.get_all_valid_moves()
    print(x)
    board.make_move(x,0,0)
    board.print_board()
    print()
    
    #white
    print("Player:",board.whose_turn())
    x = board.get_all_valid_moves()
    print(x)
    board.make_move(x,0,1)
    board.print_board()

    #red
    print("Player:",board.whose_turn())
    x = board.get_all_valid_moves()
    print(x)
    board.make_move(x,-3,1)
    board.print_board()
    print()

    #white
    print("Player:",board.whose_turn())
    x = board.get_all_valid_moves()
    print(x)
    
    board.make_move(x,3,0)
    board.print_board()

    '''
    #move red to just below white
    print("red")
    x = board.get_valid_moves(5,2)
    print(x)
    board.move(5,2,4,1)
    board.print_board()
    
    print("red")
    x = board.get_valid_moves(4,1)
    print(x)
    board.move(4,1,3,2)
    board.print_board()

    print("red")
    x = board.get_valid_moves(3,2)
    print(x)

    #see white capture moves
    print("white")
    y = board.get_valid_moves(2,1)
    print(y)
    '''

main()