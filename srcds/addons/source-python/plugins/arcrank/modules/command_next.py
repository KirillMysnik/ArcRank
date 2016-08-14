from spam_proof_commands.say import SayCommand

from ..models.ranked_player import RankedPlayer as DB_RankedPlayer

from ..ranked_player import ranked_player_manager, tell

from ..resource.sqlalchemy import Session

from ..resource.strings import build_module_strings

from .popup import send_popup


strings_module = build_module_strings('command_next')


@SayCommand(5, ['next', '!next', '/next'])
def say_next(command, index, team_only):
    player = ranked_player_manager[index]

    if player.position < 1:
        tell(player, strings_module['response not_ranked'])
        return

    if player.position == 1:
        tell(player, strings_module['response first'])
        return

    db_session = Session()

    db_ranked_player = db_session.query(DB_RankedPlayer).filter_by(
        position=player.position-1).first()

    if db_ranked_player is None:
        tell(player, strings_module['response removed_from_db'])
        return

    send_popup(player, [db_ranked_player, ],
               strings_module['popup title'].tokenize(pos=player.position-1))

    db_session.close()
