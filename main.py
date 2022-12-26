import random
import statistics


class GameSquare:  # Nodes
    def __init__(self, description, next_node=None, prev_node=None, slide_node=None):
        self.description = description
        self.next_node = next_node
        self.prev_node = prev_node
        self.slide_node = slide_node


class Player:
    skip_turn = False

    def __init__(self, current_square):
        self.current_square = current_square


class GameBoard:  # Linked List
    def __init__(self, head_node=None):
        self.head_node = head_node
        self.tail_node = head_node

    def add_node(self, node):
        if self.head_node is None:
            self.head_node = node
            self.tail_node = node
        if self.head_node is not None:
            self.tail_node.next_node = node
            node.prev_node = self.tail_node
            self.tail_node = node

    def get_node_from_index(self, index):
        current_node = self.head_node
        for i in range(index):
            if current_node.next_node is None:
                return None
            current_node = current_node.next_node
        return current_node

    def get_index_from_node(self, node):
        if node is None:
            return 0
        index = 0
        current_node = self.head_node
        while current_node is not node:
            index += 1
            current_node = current_node.next_node
        return index

    def get_index_from_value(self, value):
        index = 0
        current_node = self.head_node
        while current_node.value is not value:
            index += 1
            current_node = current_node.next_node
        return index

    def find_node_from_special(self, special_card):
        current_node = self.head_node
        while current_node.description is not special_card.value:
            current_node = current_node.next_node
        return current_node


class Card:
    def __init__(self, color=None, amount_of_squares=None, special_value=None, special=False):
        self.special = special
        self.color = color
        self.amount = amount_of_squares
        self.value = special_value


main_squares = ["Red", "Purple", "Yellow", "Blue", "Orange", "Green"]


def adding_values_to_board(adding_color_index, board, repeat_length):
    for i in range(repeat_length):
        adding_color_index += 1
        if adding_color_index >= len(main_squares):
            adding_color_index = 0
        board.add_node(GameSquare(main_squares[adding_color_index]))


def create_board():
    adding_color_index = 0
    board = GameBoard(GameSquare(main_squares[adding_color_index]))  # Declaring GameBoard
    # Adding all values
    adding_values_to_board(adding_color_index, board, 19)
    board.add_node((GameSquare("Peppermint")))
    adding_color_index = 1
    adding_values_to_board(adding_color_index, board, 5)
    board.add_node(GameSquare("Licorice"))
    adding_color_index = 1
    adding_values_to_board(adding_color_index, board, 5)
    board.add_node(GameSquare("Gumdrop"))
    adding_color_index = 0
    adding_values_to_board(adding_color_index, board, 10)
    board.add_node(GameSquare("Chocolate"))
    adding_color_index = -1
    adding_values_to_board(adding_color_index, board, 7)
    board.add_node(GameSquare("Lollipop"))
    board.add_node(GameSquare("Purple"))
    board.add_node(GameSquare("Licorice"))
    adding_color_index = 2
    adding_values_to_board(adding_color_index, board, 12)
    board.add_node(GameSquare("IceCream"))
    adding_color_index = 2
    adding_values_to_board(adding_color_index, board, 15)
    # Setting slide squares
    board.get_node_from_index(3).slide_node = board.get_node_from_index(35)
    board.get_node_from_index(17).slide_node = board.get_node_from_index(24)

    return board


deck = []


def create_deck():
    color_index = 0
    for i in range(6):
        for _ in range(6):
            deck.append(Card(main_squares[color_index], 1))
        for _ in range(4):
            deck.append(Card(main_squares[color_index], 2))
        color_index += 1
    deck.append(Card(special_value="Peppermint", special=True))
    deck.append(Card(special_value="Peppermint", special=True))
    deck.append(Card(special_value="Gumdrop", special=True))
    deck.append(Card(special_value="Chocolate", special=True))
    deck.append(Card(special_value="Lollipop", special=True))
    deck.append(Card(special_value="IceCream", special=True))
    random.shuffle(deck)


def draw_card():
    if len(deck) == 0:
        create_deck()
    deleted_card = deck[0]
    del deck[0]
    return deleted_card


def play_one_game(no_players, game_board):
    players = [Player(GameSquare(description=None, next_node=game_board.head_node)) for _ in range(no_players)]
    stop = False
    current_player_index = 0
    no_draws = 0
    while not stop:
        # Setting current player
        if current_player_index >= no_players:
            current_player_index = 0
        current_player = players[current_player_index]
        # Checking if player skips their turn
        if current_player.skip_turn:
            current_player.skip_turn = False
            current_player_index += 1
            continue
        else:
            current_card = draw_card()  # Drawing a card
            if current_card.special:  # Checking if you drew a special card
                current_player.current_square = game_board.find_node_from_special(current_card)
            else:
                current_node = current_player.current_square
                for i in range(current_card.amount):  # Finding the square to move to
                    if current_node.next_node is None:  # Checking if player is at the end of the board
                        stop = True
                        break
                    current_node = current_node.next_node
                    while current_node.description is not current_card.color:
                        if current_node.next_node is None:  # Checking if player is at the end of the board
                            stop = True
                            break
                        current_node = current_node.next_node
                current_player.current_square = current_node
                if current_player.current_square.slide_node:  # Checking if square has a slide
                    current_player.current_square = current_player.current_square.slide_node

        current_player_index += 1
        no_draws += 1
    return no_draws


def simulate(no_games, no_players):
    game_board = create_board()
    all_game_draws = []
    for _ in range(no_games):
        create_deck()
        all_game_draws.append(play_one_game(no_players, game_board))
    return "\nGames Simulated: {}\nPlayers Per Game: {}\nAverage Number of Draws: {}\n".format(no_games,
            no_players, round(statistics.mean(all_game_draws)))


number_of_games = 1000
number_of_players = 2

print(simulate(number_of_games, number_of_players))
