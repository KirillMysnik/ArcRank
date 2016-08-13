from filters.players import PlayerIter
from listeners import OnClientActive, OnClientDisconnect, OnLevelInit
from listeners.tick import GameThread
from players.entity import Player

from .internal_events import InternalEvent

from .ranked_player import broadcast, RankedPlayer, ranked_player_manager

from .resource.strings import strings_common

from .resource.sqlalchemy import Base, engine

from . import modules

from . import models


Base.metadata.create_all(engine)


def load():
    for player in PlayerIter():
        ranked_player = RankedPlayer(player)
        ranked_player_manager[player.index] = ranked_player

    InternalEvent.fire('load')
    broadcast(strings_common['load'])


def unload():
    InternalEvent.fire('unload')
    broadcast(strings_common['unload'])


@OnClientActive
def listener_on_client_active(index):
    player = Player(index)
    ranked_player_manager[player.index] = ranked_player = RankedPlayer(player)

    GameThread(target=ranked_player.load_from_database).start()


@OnClientDisconnect
def listener_on_client_disconnect(index):
    if index not in ranked_player_manager:
        return

    ranked_player = ranked_player_manager.pop(index)

    GameThread(target=ranked_player.save_to_database).start()


@OnLevelInit
def listener_on_level_init(map_name):
    def save_all_to_database():
        for ranked_player in dict(ranked_player_manager).values():
            ranked_player.save_to_database()

    GameThread(target=save_all_to_database).start()

    ranked_player_manager.clear()
