from enum import Enum

class GameEvent(Enum):
    MAP_UPDATED  = "map_updated"
    FIGHT_START  = "fight_start"
    KILL         = "kill"
    LOG          = "log"
    GAME_OVER    = "game_over"
