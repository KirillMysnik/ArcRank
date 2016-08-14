from time import time

from events import Event

from spam_proof_commands.command import anti_spam_message

from ..models.ranked_player import RankedPlayer as DB_RankedPlayer

from ..ranked_player import ranked_player_manager

from ..resource.sqlalchemy import Session

from ..resource.strings import build_module_strings

from .popup import send_popup


ANTI_SPAM_TIMEOUT = 5

_client_timestamps = {}
strings_module = build_module_strings('command_top')


@Event('player_say')
def on_player_say(game_event):
    text = game_event['text']

    if text.startswith('!top'):
        limit_raw = text[4:]
    elif text.startswith('/top'):
        limit_raw = text[4:]
    elif text.startswith('top'):
        limit_raw = text[3:]
    else:
        return

    try:
        limit = int(limit_raw)
    except ValueError:
        return

    if limit < 1:
        return

    # From now on, we now that a valid !top command has been issued
    player = ranked_player_manager.get_by_userid(game_event['userid'])

    # Anti-spam protection
    current_time = time()
    client_time = _client_timestamps.get(player.player.index, 0)

    _client_timestamps[player.player.index] = current_time

    if current_time - client_time < ANTI_SPAM_TIMEOUT:
        anti_spam_message.send(player.player.index)
        return

    # Command handling itself
    db_session = Session()

    db_ranked_players = db_session.query(DB_RankedPlayer).\
        filter(DB_RankedPlayer.position > 0).\
        order_by(DB_RankedPlayer.position)[:limit]

    send_popup(player, db_ranked_players,
               strings_module['popup title'].tokenize(limit=limit))

    db_session.close()
