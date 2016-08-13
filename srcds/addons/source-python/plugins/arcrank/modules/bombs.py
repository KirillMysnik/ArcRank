from events import Event

from ..ranked_player import ranked_player_manager

from ..resource.config import config

from ..resource.strings import build_module_strings

from .points import earn_points


strings_module = build_module_strings('bombs')


@Event('bomb_exploded')
def on_bomb_exploded(game_event):
    player = ranked_player_manager.get_by_userid(game_event['userid'])

    if player is None:
        return

    player.data['bombs_exploded'] = player.data.get('bombs_exploded', 0) + 1
    earn_points(player, int(config['scoring']['per_bomb_explosion']),
                strings_module['reason bomb_exploded'])


@Event('bomb_defused')
def on_bomb_defused(game_event):
    player = ranked_player_manager.get_by_userid(game_event['userid'])

    if player is None:
        return

    player.data['bombs_defused'] = player.data.get('bombs_defused', 0) + 1
    earn_points(player, int(config['scoring']['per_bomb_defusion']),
                strings_module['reason bomb_exploded'])
