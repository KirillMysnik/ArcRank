from events import Event

from ..ranked_player import ranked_player_manager

from ..resource.config import config

from ..resource.strings import build_module_strings

from .points import earn_points, lose_points


strings_module = build_module_strings('hostages')


@Event('hostage_rescued')
def on_hostage_rescued(game_event):
    player = ranked_player_manager.get_by_userid(game_event['userid'])

    if player is None:
        return

    player.data['hostages_rescued'] = player.data.get(
        'hostages_rescued', 0) + 1

    earn_points(player, int(config['scoring']['per_hostage_rescued']),
                strings_module['reason hostage_rescued'])


@Event('hostage_killed')
def on_bomb_defused(game_event):
    player = ranked_player_manager.get_by_userid(game_event['userid'])

    if player is None:
        return

    player.data['hostages_killed'] = player.data.get(
        'hostages_killed', 0) + 1

    lose_points(player, int(config['scoring']['per_hostage_killed']),
                strings_module['reason hostage_killed'])
