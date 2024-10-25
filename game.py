from typing import List, Tuple
from json import load, dump
from random import randint, shuffle, choice
from pathlib import Path

RANDOM_NAMES = [
    "Harry",
    "Gojo",
    "Messi",
    "Sakura",
    "Godzilla",
    "Napoleón"
]

RGB_COLORS = {
        "red": (255, 0, 0),
        "blue": (0, 0, 255),
        "green": (0, 255, 0),
        "yellow": (255, 255, 0),
        "orange": (255, 165, 0),
        "purple": (128, 0, 128),
        "gray": (128, 128, 128),
        "black": (0, 0, 0)
    }

def factorize(n: int) -> List[int]:
    """Factorize a number

    Args:
        n (int): Number to factorize

    Returns:
        List[int]: List of factors  
    """
    factors = []
    for i in range(2, n):
        while n % i == 0:
            factors.append(i)
            n = n // i
    if n > 1:
        factors.append(n)
    return factors

def _create_colors() -> dict:
    BASE_COLORS = {
        0: ["black"],
        1: ["gray"],
        2: ["orange"],
        3: ["green"],
        5: ["blue"],
        7: ["purple"]
    }

    PRIMES = [1, 2, 3, 5, 7, 11, 13, 17, 19, 23,
            29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
            71, 73, 79, 83, 89, 97, 101]

    BASE_COLORS.update({prime: ["red"] for prime in PRIMES if prime > 7})

    BASE_COLORS.update({num: [BASE_COLORS[factor][0] for factor in factorize(num)] for num in range(2, 101) 
                        if len(factorize(num)) > 1})

    BASE_COLORS = dict(sorted(BASE_COLORS.items()))

    with open("colors.json", "w") as f:
        dump(BASE_COLORS, f, indent=4)
        
    return BASE_COLORS

def _load_colors():
    if not Path("colors.json").exists():
        return _create_colors()
    
    with open("colors.json", "r") as f:
        colors = {int(k): v for k, v in load(f).items()}
        return colors
    
COLORS = _load_colors()

functions = {
    "++": {
        "f": lambda x,y: x + 1,
        "desc": "Suma 1 al resultado"
    },
    "--": {
        "f": lambda x,y: x - 1,
        "desc": "Resta 1 al resultado"
    },
    "^2": {
        "f": lambda x,y: x**2,
        "desc": "Eleva al cuadrado el resultado"
    },
    "+": {
        "f": lambda x,y: x + y,
        "desc": "Suma el resultado con y"
    },
    "-": {
        "f": lambda x,y: x - y,
        "desc": "Réstale y al resultado"
    },
    "/": {
        "f": lambda x,y: x / y,
        "desc": "Divide el resultado entre y"
    },
    "*": {
        "f": lambda x,y: x * y,
        "desc": "Multiplica y por el resultado"
    },
}

def is_prime(n: int) -> bool:
    """Check if a number is prime

    Args:
        n (int): Number to check

    Returns:
        bool: True if the number is prime, False otherwise
    """
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

OPERATIONS = ["+", "-", "*", "/"]

class Card:  
    def __init__(self, op: str, y: int = None) -> None:
        self.func: callable = functions[op]["f"]
        if y is not None:
            self.description:str = functions[op]["desc"].replace("y", y)
        self.y: int = y
    def use(self, x: int):
        return self.func(x,self.y)

class Piece:
    def __init__(self, iD: str) -> None:
        self.iD = iD
        self.loc = 0
        self.stops = 0
        
    def __str__(self):
        return self.iD

class Player:
    def __init__(self, iD: int, name: str = None) -> None:
        self.id = iD
        self.name: str = name if name else RANDOM_NAMES[randint(0,len(RANDOM_NAMES) - 1)]
        self.cards: List[Card] = []
        self.f1 = Piece(f"{iD}-1")
        self.f2 = Piece(f"{iD}-2")
        
    def move(self, player_id: int, board: list, dice: list) -> None:
        return [[choice(OPERATIONS), None], [None, choice(OPERATIONS)]]

class Board:
    """Prime Climb Board
    """
    def __init__(self) -> None:
        self.spaces: List[List] = [None for i in range(102)]
        self.spaces[0] = []
        self.spaces[-1] = []
        self.length = 101
    def __getitem__(self, i):
        return self.spaces[i]
    def __setitem__(self, i, value):
        self.spaces[i] = value
    def __len__(self):
        return self.length
    def __iter__(self):
        return iter(self.spaces)
    
    def simple_repr(self):
        """ Simple representation of the board

        Returns:
            list: List of strings
        """
        new_board = []
        for i in range(len(self.spaces)):
            if type(self.spaces[i]) is list:
                new_board.append([])
                for j in self.spaces[i]:
                    new_board[-1].append(str(j))
            else:
                new_board.append(str(self.spaces[i]))
        return new_board

class Game:
    """Prime Climb Game
    """
    def __init__(self, players: int = 2) -> None:
        ls = list(range(1, players + 1))
        self.players = [Player(iD=i) for i in ls]
        self.board = Board()
        self.turn = 0
        self.operations = OPERATIONS
        self.put_pieces()
        
    @staticmethod
    def roll_dice(n: int = 2, faces: int = 10) -> List[int]:
        """ Roll the dice
        
        Args:
            n (int, optional): Number of dice. Defaults to 2.
            faces (int, optional): Number of faces. Defaults to 10.

        Returns:
            List[int]: _description_
        """
        return [randint(1,faces) for i in range(n)]
    
    @property
    def current_player(self) -> Player:
        """ Current player

        Returns:
            Player: Current player
        """
        return self.players[(self.turn) % self.player_count]
    
    @property
    def player_count(self) -> int:
        """ Number of players

        Returns:
            int: Number of players
        """
        return len(self.players)
    
    @staticmethod
    def generate_card() -> Card:
        """ Generate a card

        Returns:
            Card: A card with a random operation and value
        """
        op = choice(functions)
        card = Card(op=op, y=randint(1, 50))
        return card
    
    def put_pieces(self) -> None:
        """ Put the pieces in the board
        """
        for p in self.players:
            self.board[0].append(p.f1)
            self.board[0].append(p.f2)
    
    def do_move(self, f: Piece, dice: list, move: list) -> int:
        """ Perform a move

        Args:
            f (Piece): Piece to move
            dice (list): Values of the dice
            move (list): Operations to do

        Returns:
            int: New location of the piece
        """
        val = f.loc
        for op in move:
            if op is not None:
                val = eval(f"{val} {op[1]} {dice[op[0]]}")
        return val
    
    def check_win(self) -> bool:
        """ Check if the player has won

        Returns:
            bool: True if the player has won, False otherwise
        """
        if self.current_player.f1.loc == 101 and self.current_player.f2.loc == 101:
            return True
    
    def check_move(self, dice: list, move: list) -> bool:
        """ Check if the move is valid
        
        Args:
            dice (list): Values of the dice
            move (list): Operations to do
            
        Returns:
            bool: True if the move is valid, False otherwise
        
        Example: move = [["*", None], [None, "*"]]
        """
        def int_division(dice, move) -> bool:
            pieces = [self.current_player.f1, self.current_player.f2]
            for i in range(2):
                mov = self.do_move(pieces[i], dice, move[i])
                if mov - int(mov) != 0:
                    print("The move must be exact")
                    return False
            return True
            
        def stops_101(dice: list, move: list) -> bool:
            """ Check if the player has made the two stops before reaching 101

            Args:
                dice (list): Values of the dice
                move (list): Operations to do

            Returns:
                bool: True if the player has made the two stops, False otherwise
            """
            if ((self.current_player.f1.stops < 2 and self.do_move(self.current_player.f1, dice, move[0]) == 101) or
                (self.current_player.f2.stops < 2 and self.do_move(self.current_player.f2, dice, move[1]) == 101)):
                print("You want to get to 101 and you haven't made the two stops")
                return False
            
            return True
        
        def piece_end_game(dice: list, move: list) -> bool:
            """ Check if the piece has already won

            Args:
                dice (list): Values of the dice
                move (list): Operations to do

            Returns:
                bool: True if the piece has already won, False otherwise
            """
            for op in move[0]:
                if op is not None and self.current_player.f1.loc == 101:
                    print("You can't move a piece that has already won")
                    return False
            for op in move[1]:
                if op is not None and self.current_player.f2.loc == 101:
                    print("You can't move a piece that has already won")
                    return False
            return True
        
        def use_dice_once(dice: list, move: list) -> bool:
            """ Check if the dice are used once

            Args:
                dice (list): Values of the dice
                move (list): Operations to do

            Returns:
                bool: True if the dice are used once, False otherwise
            """
            mask = [0] * len(dice)
            for i in range(len(move)):
                for j in range(i):
                    if move[i][j] is not None:
                        if mask[move[i][j][0]] == 1:
                            print(f"Die {move[i][j][0]} must be used once")
                            return False
                        else:
                            mask[move[i][j][0]] = 1
            return True
        
        def use_correct_operations(move: list) -> bool:
            """ Check if the operations are valid

            Args:
                move (list): Operations to do

            Returns:
                bool: True if the operations are valid, False otherwise
            """
            for i in move:
                for j in i:
                    if j is not None and j[1] not in self.operations:
                        print(f"Invalid operation {j[1]}")
                        return False
            return True
        
        def use_all_dice(dice: list, move: list) -> bool:
            """ Check if all dice are used

            Args:
                dice (list): Values of the dice
                move (list): Operations to do

            Returns:
                bool: True if all dice are used, False otherwise
            """
            mask = [0] * len(dice)
            for i in move:
                for j in i:
                    if j is not None:
                        mask[j[0]] = 1
                        
            count = sum(mask)
            loc1 = self.do_move(self.current_player.f1, dice, move[0])
            loc2 = self.do_move(self.current_player.f2, dice, move[1])
            
            if (count == len(dice) or 
                (count > 0 and loc1 == loc2 == 101)):
                return True
            print("You must use all dice")
            return False
        
        def move_in_range(dice: list, move: list) -> bool:
            """ Check if the move is in range

            Args:
                dice (list): Values of the dice
                move (list): Operations to do

            Returns:
                bool: True if the move is in range, False otherwise
            """
            f1 = self.current_player.f1
            f2 = self.current_player.f2
            m1 = self.do_move(f1, dice, move[0])
            m2 = self.do_move(f2, dice, move[1])
            # print(f'f1: {f1.loc} - f2: {f2.loc} - m1: {m1} - m2: {m2} - {self.current_player.id} - {move} - {dice}')
            if (0 <= m1 <= 101) and (0 <= m2 <= 101):
                return True
            
            print("The operation is out of range")
            return False
                    
        return (use_all_dice(dice, move) and use_correct_operations(move) and 
                use_dice_once(dice, move) and move_in_range(dice, move) and
                piece_end_game(dice, move) and stops_101(dice, move) and 
                int_division(dice, move))
        
    def add_player(self, names: List[str]) -> None:
        """Add a player to the game

        Args:
            player (str): Player's name
        """
        if len(names) != self.player_count:
            return Exception("Number of names must match number of players")
        for i in range(len(self.players)):
            self.players[i] = names[i]
            
    def update_board(self, dice: list, move: list) -> None:
        """ Update the board after a move

        Args:
            dice (list): Values of the dice
            move (list): Operations to do
        """
        f1 = self.current_player.f1
        f2 = self.current_player.f2
        pieces = [f1, f2]
        locs = [f1.loc, f2.loc]
        
        for i,piece in enumerate(pieces):            
            piece_loc = int(self.do_move(piece, dice, move[i]))
            locs[i] = piece_loc
            
            if 0 < piece.loc < 101:
                self.board[piece.loc] = None
            elif piece.loc == 0:
                self.board[0].remove(piece)
            else:
                self.board[101].remove(piece)
        
        for i,piece in enumerate(pieces):   
            if locs[i] == 101: 
                self.board[101].append(piece)
            elif locs[i] == 0:
                self.board[0].append(piece)
            else:
                if self.board[locs[i]] is None:
                    self.board[locs[i]] = piece
                else:
                    if i == 0:
                        if self.board[locs[i]].iD[0] != str(self.current_player.id):
                            f = self.board[locs[i]]
                            self.board[0].append(f)
                            self.board[locs[i]] = None
                            self.board[locs[i]] = piece
                            f.loc = 0
                        else:
                            self.board[locs[i]] = piece
                    else:
                        f = self.board[locs[i]]
                        self.board[0].append(f)
                        self.board[locs[i]] = None
                        self.board[locs[i]] = piece
                        f.loc = 0
                    
            if is_prime(locs[i]) and (30 < locs[i] < 80) and piece.loc != locs[i]:
                piece.stops += 1
                
            piece.loc = locs[i]
    def play(self) -> None:
        """ Play the game
        """
        while True:
            dice = self.roll_dice()
            if dice[0] == dice[1]:
                dice = [dice[0]] * 4
            move = self.current_player.move(self.current_player.id, 
                                            [(player.f1.loc, player.f2.loc) for player in self.players], 
                                            dice)
            is_correct = self.check_move(dice, move)
            if not is_correct:
                print("Invalid move")
                break
            self.update_board(dice, move)
            if self.check_win():
                print(f"{self.current_player.name} wins!")
                break
            self.turn += 1
            
        
# game = Game()
# game.play()