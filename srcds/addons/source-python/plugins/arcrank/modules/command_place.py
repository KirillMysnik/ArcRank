from datetime import datetime

from spam_proof_commands.say import SayCommand

from ..ranked_player import ranked_player_manager, tell

from ..resource.strings import build_module_strings

from .server import server


strings_module = build_module_strings('command_place')


@SayCommand(3, ['place', '!place', '/place'])
def say_place(command, index, team_only):
    ranked_player = ranked_player_manager[index]

    if ranked_player.position < 1:
        tell(ranked_player, strings_module['response not_ranked'])

    else:
        delta = datetime.fromtimestamp(server.last_sorted_at) - datetime.now()
        tell(ranked_player, strings_module['response ranked'].tokenize(
            pos=ranked_player.position,
            total=server.total_positions,
            updated=str(delta),
        ))
