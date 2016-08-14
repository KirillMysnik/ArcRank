from spam_proof_commands.say import SayCommand

from ..ranked_player import ranked_player_manager, tell

from ..resource.strings import build_module_strings


strings_module = build_module_strings('command_kdr')


@SayCommand(1, ['kdr', '!kdr', '/kdr'])
def say_kdr(command, index, team_only):
    player = ranked_player_manager[index]
    tell(player, strings_module['response'])
