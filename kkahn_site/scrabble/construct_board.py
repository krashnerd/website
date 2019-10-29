from MyScrabble.game import ScrabbleBoard

css_class_lookup = {
    'L2':'square-double-letter',
    'W2':'square-double-word',
    'L3':'square-triple-letter',
    'W3':'square-triple-word',
    }
bonus_text_lookup = {
    'L2':'Double\nletter\nscore',
    'W2':'Double\nword\nscore',
    'L3':'Triple\nletter\nscore',
    'W3':'Triple\nword\nscore',
}


class TileTemplate():
    def __init__(self, bonus_type = None):
        self.css_class = css_class_lookup.get(bonus_type)
        self.bonus_text = self.bonus_text_lookup.get(bonus_type, "")

