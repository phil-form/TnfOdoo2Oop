import curses
import textwrap
from interfaces.IObserver import IObserver
from enums.GameEvent import GameEvent
from models.Coordinate import Coordinate

PAIR_HERO   = 1
PAIR_WOLF   = 2
PAIR_ORC    = 3
PAIR_DRAGON = 4
PAIR_STATS  = 5
PAIR_LOG    = 6
PAIR_DIM    = 7
PAIR_HP_OK  = 8
PAIR_HP_LOW = 9
PAIR_TITLE  = 10
PAIR_SEL    = 11

TOKEN_COLORS = {'H': PAIR_HERO, 'X': PAIR_DIM, 'W': PAIR_WOLF, 'O': PAIR_ORC, 'D': PAIR_DRAGON}
MAX_LOG = 10
INFO_W  = 28


class Display(IObserver):

    def __init__(self, stdscr):
        self._scr = stdscr
        self._map_win = None
        self._info_win = None
        self._log = []
        self._hero = None
        self._characters = []
        self._size = 0
        self._ennemyCount = 0
        self._emptyTile = ' . '
        self._mapName = ''
        self._scr.keypad(True)
        curses.curs_set(0)
        self._setupColors()

    def _setupColors(self):
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(PAIR_HERO,   curses.COLOR_YELLOW,  -1)
        curses.init_pair(PAIR_WOLF,   curses.COLOR_WHITE,   -1)
        curses.init_pair(PAIR_ORC,    curses.COLOR_RED,     -1)
        curses.init_pair(PAIR_DRAGON, curses.COLOR_MAGENTA, -1)
        curses.init_pair(PAIR_STATS,  curses.COLOR_GREEN,   -1)
        curses.init_pair(PAIR_LOG,    curses.COLOR_CYAN,    -1)
        curses.init_pair(PAIR_DIM,    curses.COLOR_WHITE,   -1)
        curses.init_pair(PAIR_HP_OK,  curses.COLOR_GREEN,   -1)
        curses.init_pair(PAIR_HP_LOW, curses.COLOR_RED,     -1)
        curses.init_pair(PAIR_TITLE,  curses.COLOR_BLUE,    -1)
        curses.init_pair(PAIR_SEL,    curses.COLOR_YELLOW,  -1)

    def update(self, event, data):
        if event == GameEvent.MAP_UPDATED:
            self._hero = data['hero']
            self._characters = data['characters']
            self._size = data['size']
            self._ennemyCount = data['ennemyCount']
            self._emptyTile = data['emptyToken']
            self._mapName = data.get('mapName', '')
            self._render()
        elif event in (GameEvent.FIGHT_START, GameEvent.KILL, GameEvent.LOG):
            self._addLog(data)
            self._refreshInfo()
        elif event == GameEvent.GAME_OVER:
            self._addLog(data)
            self._render()

    def _render(self):
        if self._size == 0:
            return
        max_y, max_x = self._scr.getmaxyx()
        map_w = max(1, max_x - INFO_W)
        try:
            self._info_win = curses.newwin(max_y, INFO_W, 0, 0)
            self._map_win  = curses.newwin(max_y, map_w,  0, INFO_W)
            self._map_win.keypad(True)
        except curses.error:
            return
        self._drawInfo(self._info_win)
        self._drawMap(self._map_win)
        try:
            self._info_win.noutrefresh()
            self._map_win.noutrefresh()
            curses.doupdate()
        except curses.error:
            pass

    def _refreshInfo(self):
        if self._info_win is None or self._hero is None:
            return
        self._drawInfo(self._info_win)
        try:
            self._info_win.refresh()
        except curses.error:
            pass

    def _drawMap(self, win):
        try:
            h, w = win.getmaxyx()
            win.erase()
            win.border()

            grid_w = self._size * 3
            grid_h = self._size
            ox = max(2, (w - grid_w) // 2)
            oy = max(3, (h - grid_h) // 2)

            title = f" {self._mapName}  {self._size}×{self._size} "
            self._put(win, oy - 2, max(1, (w - len(title)) // 2),
                      title, curses.color_pair(PAIR_TITLE) | curses.A_BOLD)

            dim = curses.color_pair(PAIR_DIM) | curses.A_DIM
            self._put(win, oy - 1, ox - 1, '┌' + '─' * grid_w + '┐', dim)
            self._put(win, oy + grid_h, ox - 1, '└' + '─' * grid_w + '┘', dim)
            for i in range(grid_h):
                self._put(win, oy + i, ox - 1, '│', dim)
                self._put(win, oy + i, ox + grid_w, '│', dim)

            legend_y = oy + grid_h + 1
            if legend_y < h - 1:
                legend = "H=you  W=wolf  O=orc  D=dragon"
                self._put(win, legend_y, max(1, (w - len(legend)) // 2), legend, dim)

            for i in range(grid_h):
                for j in range(self._size):
                    token = self._tokenAt(Coordinate(i, j))
                    self._put(win, oy + i, ox + j * 3, token, self._tokenAttr(token))

        except curses.error:
            pass

    def _drawInfo(self, win):
        try:
            h, w = win.getmaxyx()
            win.erase()
            win.border()

            hero = self._hero
            if hero is None:
                return

            row = 1
            name_str = f"[ {hero.name} ]"
            self._put(win, row, max(1, (w - len(name_str)) // 2),
                      name_str, curses.color_pair(PAIR_HERO) | curses.A_BOLD)
            row += 1

            self._put(win, row, 2, f"Race : {hero.race}", curses.color_pair(PAIR_STATS))
            row += 1

            bar_w = max(1, w - 8)
            ratio = max(0.0, hero.health / max(1, hero.maxHealth))
            filled = int(bar_w * ratio)
            hp_attr = curses.color_pair(PAIR_HP_OK if ratio > 0.3 else PAIR_HP_LOW) | curses.A_BOLD
            try:
                win.addstr(row, 2, chr(9608) * filled, hp_attr)
                win.addstr(row, 2 + filled, chr(9617) * (bar_w - filled),
                           curses.color_pair(PAIR_DIM) | curses.A_DIM)
            except curses.error:
                pass
            row += 1

            self._put(win, row, 2, f"HP   {hero.health}/{hero.maxHealth}", curses.color_pair(PAIR_STATS))
            row += 1
            self._put(win, row, 2, f"STR  {hero.strength}   STAM {hero.stamina}", curses.color_pair(PAIR_STATS))
            row += 1
            self._put(win, row, 2, f"Kills  {hero.killCount}/{self._ennemyCount}", curses.color_pair(PAIR_STATS))
            row += 1
            self._put(win, row, 2, f"Gold     {hero.getGold()}", curses.color_pair(PAIR_STATS))
            row += 1
            self._put(win, row, 2, f"Leather  {hero.getLeather()}", curses.color_pair(PAIR_STATS))
            row += 2

            self._put(win, row, 1, chr(9472) * (w - 2), curses.color_pair(PAIR_DIM) | curses.A_DIM)
            row += 1
            self._put(win, row, 2, "EVENT LOG", curses.color_pair(PAIR_LOG) | curses.A_BOLD)
            row += 1

            wrap_w = max(1, w - 4)
            lines = []
            for msg in self._log:
                lines.extend(textwrap.wrap(msg, wrap_w) or [msg])

            for line in lines[-(h - row - 1):]:
                if row >= h - 1:
                    break
                self._put(win, row, 2, line, curses.color_pair(PAIR_LOG))
                row += 1

        except curses.error:
            pass

    @staticmethod
    def _put(win, y, x, text, attr=0):
        try:
            win.addstr(y, x, text, attr)
        except curses.error:
            pass

    def _tokenAt(self, coord):
        if self._hero == coord:
            return self._hero.getToken()
        for ch in self._characters:
            if ch == coord:
                return ch.getToken()
        return self._emptyTile

    def _tokenAttr(self, token):
        key = token.strip()
        pair = TOKEN_COLORS.get(key, PAIR_DIM)
        bold = curses.A_BOLD if key in ('H', 'O', 'D') else 0
        dim  = curses.A_DIM  if key in ('X', '')       else 0
        return curses.color_pair(pair) | bold | dim

    def readKey(self):
        # win.getch() refreshes that window; stdscr.getch() would wipe the display
        if self._map_win is not None:
            return self._map_win.getch()
        return self._scr.getch()

    def askReplay(self):
        self._addLog("[ R ] replay   [ Q ] quit")
        self._refreshInfo()
        while True:
            key = self.readKey()
            if key in (ord('r'), ord('R')):
                self._log.clear()
                return True
            if key in (ord('q'), ord('Q')):
                return False

    def _addLog(self, message):
        self._log.append(str(message))
        if len(self._log) > MAX_LOG:
            self._log.pop(0)

    def selectMap(self):
        options = [
            ("forest", "Forest", "15x15  balanced enemies"),
            ("cave",   "Cave",   "12x12  dragon-heavy"),
        ]
        idx = self._menuSelect("  SELECT YOUR MAP  ", options)
        mapType = options[idx][0]
        return (mapType, 15, 15) if mapType == "forest" else (mapType, 12, 12)

    def selectHero(self):
        options = [
            (1, "Human", "+1 STR  +1 STAM"),
            (2, "Dwarf", "+2 STAM  tougher"),
        ]
        idx = self._menuSelect("  SELECT YOUR RACE  ", options)
        race = options[idx][0]
        name = self._inputName("  ENTER YOUR NAME  ")
        return race, name

    def _menuSelect(self, title, options):
        self._scr.clear()
        self._scr.refresh()

        desc_w  = max(len(o[2]) for o in options)
        label_w = max(len(o[1]) for o in options)
        dialog_w = max(len(title) + 4, label_w + desc_w + 10, 36)
        dialog_h = len(options) + 6

        max_y, max_x = self._scr.getmaxyx()
        try:
            win = curses.newwin(dialog_h, dialog_w,
                                max(0, (max_y - dialog_h) // 2),
                                max(0, (max_x - dialog_w) // 2))
            win.keypad(True)
        except curses.error:
            return 0

        selected = 0
        while True:
            win.erase()
            win.border()
            self._put(win, 1, max(1, (dialog_w - len(title)) // 2),
                      title, curses.color_pair(PAIR_TITLE) | curses.A_BOLD)
            self._put(win, 2, 1, chr(9472) * (dialog_w - 2),
                      curses.color_pair(PAIR_DIM) | curses.A_DIM)

            for i, (_, label, desc) in enumerate(options):
                line = f"  {label:<{label_w}}  {desc}"
                if i == selected:
                    self._put(win, 3 + i, 1, f"> {line}",
                              curses.color_pair(PAIR_SEL) | curses.A_BOLD)
                else:
                    self._put(win, 3 + i, 1, f"  {line}", curses.color_pair(PAIR_DIM))

            sep = 3 + len(options)
            self._put(win, sep, 1, chr(9472) * (dialog_w - 2),
                      curses.color_pair(PAIR_DIM) | curses.A_DIM)
            self._put(win, sep + 1, 2, "↑↓ navigate    ENTER confirm",
                      curses.color_pair(PAIR_LOG))

            win.refresh()
            key = win.getch()

            if key in (curses.KEY_UP, ord('k'), ord('w')):
                selected = (selected - 1) % len(options)
            elif key in (curses.KEY_DOWN, ord('j'), ord('s')):
                selected = (selected + 1) % len(options)
            elif key in (ord('\n'), ord('\r'), curses.KEY_ENTER):
                return selected

    def _inputName(self, prompt):
        self._scr.clear()
        self._scr.refresh()

        dialog_w = 46
        dialog_h = 6
        max_y, max_x = self._scr.getmaxyx()
        try:
            win = curses.newwin(dialog_h, dialog_w,
                                max(0, (max_y - dialog_h) // 2),
                                max(0, (max_x - dialog_w) // 2))
            win.keypad(True)
        except curses.error:
            return "Hero"

        curses.curs_set(1)
        text = ""
        while True:
            win.erase()
            win.border()
            self._put(win, 1, max(1, (dialog_w - len(prompt)) // 2),
                      prompt, curses.color_pair(PAIR_TITLE) | curses.A_BOLD)
            self._put(win, 2, 1, chr(9472) * (dialog_w - 2),
                      curses.color_pair(PAIR_DIM) | curses.A_DIM)
            self._put(win, 3, 2, f"> {text}_",
                      curses.color_pair(PAIR_STATS) | curses.A_BOLD)
            self._put(win, 4, 1, chr(9472) * (dialog_w - 2),
                      curses.color_pair(PAIR_DIM) | curses.A_DIM)
            self._put(win, 4, 2, "ENTER to confirm", curses.color_pair(PAIR_LOG))
            win.refresh()
            key = win.getch()

            if key in (ord('\n'), ord('\r'), curses.KEY_ENTER):
                if text.strip():
                    break
            elif key in (curses.KEY_BACKSPACE, 127, 8):
                text = text[:-1]
            elif 32 <= key <= 126 and len(text) < dialog_w - 6:
                text += chr(key)

        curses.curs_set(0)
        return text.strip()
