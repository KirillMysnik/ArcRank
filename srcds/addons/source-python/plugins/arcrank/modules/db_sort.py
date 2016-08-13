from time import time

from listeners.tick import Delay, GameThread

from ..internal_events import InternalEvent

from ..models.ranked_player import RankedPlayer as DB_RankedPlayer

from ..ranked_player import ranked_player_manager

from ..resource.config import config

from ..resource.sqlalchemy import Session

from .server import server


def sort():
    live_player_steamid_map = {}
    for ranked_player in ranked_player_manager.values():
        live_player_steamid_map[ranked_player.player.steamid] = ranked_player

    db_session = Session()
    db_ranked_players = db_session.query(DB_RankedPlayer).all()

    # We do sorting manually to avoid low database performance
    db_ranked_players = sorted(
        db_ranked_players, key=lambda db_ranked_player: db_ranked_player.score,
        reverse=True
    )

    current_time = time()
    max_delta = (int(config['tracking']['inactive_days_before_deletion']) *
                 24 * 3600)

    total_positions = 0
    for db_ranked_player in db_ranked_players:
        if current_time - db_ranked_player.last_seen_at > max_delta:
            db_session.delete(db_ranked_player)

        else:
            total_positions += 1
            db_ranked_player.position = total_positions

            ranked_player = live_player_steamid_map.get(
                db_ranked_player.steamid)

            if ranked_player is not None:
                ranked_player.position = total_positions

    db_session.commit()
    db_session.close()

    server.total_positions = total_positions
    server.last_sorted_at = current_time

    # Schedule another sort
    Delay(int(config['tracking']['resorting_interval_seconds']), start_sorting)


def start_sorting():
    GameThread(target=sort).start()


@InternalEvent('load')
def on_load(event_var):
    sort()
