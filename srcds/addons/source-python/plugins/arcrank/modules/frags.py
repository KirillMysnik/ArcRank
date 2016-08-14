from events import Event

from ..ranked_player import ranked_player_manager

from ..resource.config import config

from ..resource.strings import build_module_strings

from .points import earn_points, lose_points


strings_module = build_module_strings('frags')


@Event('player_death')
def on_player_death(game_event):
    attacker = ranked_player_manager.get_by_userid(game_event['attacker'])
    player = ranked_player_manager.get_by_userid(game_event['userid'])

    if attacker is not None:
        attacker.data['kills'] = attacker.data.get('kills', 0) + 1
        attacker.session_data['kills'] = attacker.session_data.get(
            'kills', 0) + 1

        if game_event['headshot']:
            attacker.data['headshot_kills'] = attacker.data.get(
                'headshot_kills', 0) + 1

            attacker.session_data['headshot_kills'] =\
                attacker.session_data.get('headshot_kills', 0) + 1

            earn_points(attacker, int(config['scoring']['per_headshot_kill']),
                        strings_module['reason headshot_kill'])

        else:
            earn_points(attacker, int(config['scoring']['per_kill']),
                        strings_module['reason kill'])

    if player is not None:
        player.data['deaths'] = player.data.get('deaths', 0) + 1
        player.session_data['deaths'] = player.session_data.get(
            'deaths', 0) + 1

        lose_points(player, int(config['scoring']['per_death']),
                    strings_module['reason death'])
