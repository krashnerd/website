from .ScrabbleTile import Tile
from .ScrabbleDictionary import dictionary
from ..utils import utils, consts
from .exceptions import *

class Board:
    """docstring for S_Board"""
    def __init__(self):

        class BoardSpaceTemplate():
            """ Template for a board space, including letter/word bonus amount as well as cosmetic info."""
            def __init__(self, bonus_type = None):
                css_class_lookup = {
                    'L2':'square-double-letter',
                    'W2':'square-double-word',
                    'L3':'square-triple-letter',
                    'W3':'square-triple-word',
                    None:'square'
                }

                bonus_text_lookup = {
                    'L2':'Double\nletter\nscore',
                    'W2':'Double\nword\nscore',
                    'L3':'Triple\nletter\nscore',
                    'W3':'Triple\nword\nscore',
                    None:''
                }

                self.bonus_type = bonus_type
                self.css_class = css_class_lookup.get(bonus_type)
                self.bonus_text = bonus_text_lookup.get(bonus_type, "")
                self.css_class_lookup = css_class_lookup.get(bonus_type)

                # Default bonus values
                self.letter_bonus = 1
                self.word_bonus = 1

                if bonus_type is not None:
                    bonus_amt = int(bonus_type[1])
                    if(bonus_type [0] == "L"):
                        self.letter_bonus = bonus_amt
                    else:
                        self.word_bonus = bonus_amt

            def in_range(self, a):
                return 0 <= a[0] < 15 and 0 <= a[1] < 15

        self.is_transposed = False
        _TWS = [(x,y) for x in [0,7,14] for y in [0,7,14]]
        _TWS.remove((7,7))
        _DWS = [(7 + dx*ffset,7+dy*ffset) for ffset in range(3,7) for dx in [-1,1] for dy in [-1,1]] 
        _DWS.append((7,7))

        # Double letters
        _DLS = [(x0+dx*mx,y0+dy*my)
                for x0,dx in [(0,1),(14,-1)] 
                    for y0,dy in [(0,1),(14,-1)]
                        for mx,my in [(0,3),(2,6),(3,7),(6,6),(3,0),(6,2),(7,3)]]

        # Triple letters
        _TLS = [(x0+dx*mx,y0+dy*my) 
                for x0,dx in [(0,1),(14,-1)]
                    for y0,dy in [(0,1),(14,-1)]
                        for mx,my in [(5,1),(5,5),(1,5)]]

        # self.vert_grid = [[self.grid[c][r] for r in range(15)] for c in range(15)]
        templates = {bonus_type: BoardSpaceTemplate(bonus_type) for bonus_type in ("L2", "W2", "L3", "W3", None)}

        self.grid = [[Board_Space((r, c), templates[None]) for c in range(15)] for r in range(15)]
        
        for coords_lst, bonus_type in [(_DLS,"L2"),(_DWS,"W2"),(_TWS,"W3"),(_TLS,"L3")]:
            for coords in coords_lst:
                self[coords].set_bonus(templates[bonus_type])

    def place_tile_on_board(self, tile, coords):
        self[coords].place_tile_on_space(tile)

    def __getitem__(self, r, c = None):

        if c is None:
            if isinstance(r, int):
                raise TypeError("Expected iterable, got int")
            r, c = r

        if r < 0 or c < 0:
            raise NegativeIndexError        
        return self.grid[r][c]

    def __setitem__(self, ind, tile):
        if ind != self[ind].loc:
            print("Given: {} which is index of tile at {}".format(ind, self[ind].loc))
        assert ind == self[ind].loc
        if isinstance(tile, Tile):
            self.place_tile_on_board(tile, ind)
        elif tile is None:
            self[ind].pick_up_tile()
        else:
            raise TypeError("Expected Tile instance or None, got {}".format(type(tile)))

    def __repr__(self):
        result = ""
        result += ("_" * 76) + '\n'
        for row in self.grid:
            for printedRowFn in [
                    lambda tile: "   ",
                    lambda tile:
                        (" %s " % tile.tile.letter) if tile.occupied 
                        else 
                            tile.template.bonus_type if tile.bonus_type is not None 
                            else 
                                "   ",
                     lambda tile: "___"]:

                result += ("|%s|\n" % "|".join(map(printedRowFn, row)))
        return result

    def transpose(self, which = None):
        if which != self.is_transposed:
            self.is_transposed = not self.is_transposed
            self.grid = utils.grid_transpose(self.grid)

    def untranspose(self):
        if self.is_transposed:
            self.transpose()

    def get(self, r,c = None):
        if c == None:
            r,c = r
        return self.grid[r][c]

    def get_letter(self, r,c = None):
        try:
            return self[r, c].tile.letter
        except AttributeError:
            return 

    def score_word(self, new_tile_locs_preprocess):
        assert not self.is_transposed
        for r, c in new_tile_locs_preprocess:
            assert self[r, c].occupied

        rows, cols = zip(*new_tile_locs_preprocess)

        # Handle transposition of board if the word was placed vertically -------------------

        if len(set(rows)) == 1:
            new_tile_locs = new_tile_locs_preprocess
        else:
            if len(set(cols)) != 1:
               
                raise InvalidMoveError

            self.transpose()
            new_tile_locs = [(a, b) for b, a in new_tile_locs_preprocess]

        main_word_score = 0
        r,original_c = new_tile_locs[0]


        # Scores a single word based on the word locations -----------------


        def score_single_word(word_locs):
            word_points = 0
            word_mult = 1

            for r, c in word_locs:
                space = self[r, c]
                tile = space.tile
                letter_mult = 1

                # Apply bonus
                if (r, c) in new_tile_locs:
                    word_mult *= space.word_bonus
                    letter_mult *= space.letter_bonus

                word_points += letter_mult * tile.points

            return word_mult * word_points


        # --------- Find beginning and end of horizontal word ------------


        c = original_c
        letter = self[r, c].get_letter()

        while c >= 0 and letter is not None:
            c -= 1
            try:
                letter = self[r, c].get_letter()
            except IndexError:
                break

        begin = c + 1

        c = original_c

        letter = self[r, c].get_letter()
        while c < 15 and letter is not None:
            c += 1
            try:
                letter = self[r, c].get_letter()
            except IndexError:
                break

        end = c


        # --------- Get list of coordinates for each new word -----------


        all_word_locs = [[(r, curr_c) for curr_c in range(begin, end)]]
        for r, c in new_tile_locs:
            letter = self[r, c].get_letter()

            # Backtrack until finding an empty square or the start of the self
            while r >= 0 and letter is not None:
                r -= 1
                try:
                    letter = self[r, c].get_letter()
                except IndexError:
                    letter = None
                
            r += 1
            letter = self[r, c].get_letter()
            curr_word_locs = list()

            while r < 15 and letter is not None:
                curr_word_locs.append((r, c))
                r += 1
                try:
                    letter = self[r, c].get_letter()
                except IndexError:
                    break

            all_word_locs.append(curr_word_locs)


        # -------- Return the score of each word with length > 1 ---------


        all_word_locs = list(filter(lambda x:len(x) > 1, all_word_locs))
        all_words = ["".join([self[loc].get_letter() for loc in word_locs]) for word_locs in all_word_locs]

        

        base_score = sum([score_single_word(word) for word in all_word_locs if len(word) > 1])

        self.untranspose()

        for word in all_words:
            if word not in dictionary:
                print("{} is not a word".format(word))
                raise InvalidMoveError

        bonus_score = 50 if len(new_tile_locs) == 7 else 0
        return base_score + bonus_score


    def check_move_score(self, move):
        """Checks the score of a move without applying it"""
        assert not self.is_transposed

        if not move:
            raise EmptyMoveError

        for _, loc in move:
            assert self[loc].loc == loc

        try:
            locs = [loc for _, loc in move]
        except ValueError:
            print("Move:{} ".format(move))
            locs = [loc for _, loc in move]

        for tile, loc in move: 
            if self[loc].occupied:
                raise OccupiedSpaceError("Board:\n{}\nMove:{}".format(str(self), loc))
            self[loc] = tile

        try:
            score = self.score_word(locs)

        except InvalidMoveError:
            for loc in locs:
                self[loc] = None
            raise

        for loc in locs:
            self[loc] = None
        return score


class Board_Space(object):
    def __init__(self, loc, bonus_template):
        """Makes a board space which knows its own location bonus type"""

        self.occupied = False
        self.tile = None
        self.loc = loc
        r, c = self.loc
        self.id = str(r * 15 + c)
        self.template = bonus_template

        self.sync_template()
        # self.printedBonusType = ("%sx%s" % (bonus_type[0],bonus_type[1]) if self.bonus_type is not None else "  ")

        # # Special case for the center tile
        # if loc == (7,7):
        #     self.printedBonusType = " * "

        #Parsing bonus amount


    def sync_template(self):

        self.word_bonus = self.template.word_bonus
        self.letter_bonus = self.template.letter_bonus
        self.bonus_type = self.template.bonus_type

        self.in_range = self.template.in_range

    def get_letter(self):
        if not self.occupied:
            return None

        else:
            return self.tile.letter

    def set_bonus(self, bonus_template):
        self.template = bonus_template
        self.sync_template()


    def place_tile_on_space(self, tile):
        if tile is None:
            self.pick_up_tile()
            return
        if(self.occupied or self.tile):
            raise OccupiedSpaceError("Space {} is already occupied".format(self.loc))
        self.occupied = True
        self.tile = tile

    def pick_up_tile(self):
        """ Remove and return tile"""
        tile = self.tile
        self.occupied = False
        self.tile = None
        return tile

    def __repr__(self):
        return ' ' if self.tile == None else self.tile.letter



