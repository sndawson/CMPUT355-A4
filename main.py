# Using this library for now: https://pypi.org/project/imparaai-checkers/

from checkers.game import Game
import alphabeta

game = Game()

#print(alphabeta.alphabeta(game))

while not game.is_over():
    print("Board coords:")
    alphabeta.print_board_coords()
    print("Board:")
    alphabeta.pretty_print_board(game.board)
    print(game.get_possible_moves())
    start_piece = int(input("Black piece to move: "))
    end_pos = int(input("Where to move to: "))
    game.move([start_piece, end_pos])

    # Now white's turn:
    alphabeta.play_move(game)

print("Board coords:")
alphabeta.print_board_coords()
print("Board:")
alphabeta.pretty_print_board(game.board)
print(game.get_possible_moves())
print(game.whose_turn())
print(game.is_over())
print(game.get_winner())
