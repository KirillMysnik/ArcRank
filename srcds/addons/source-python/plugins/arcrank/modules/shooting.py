from events import Event
from weapons.manager import weapon_manager

from ..ranked_player import ranked_player_manager


@Event('player_hurt')
def on_player_hurt(game_event):
    weapon_instance = weapon_manager[game_event['weapon']]
    if weapon_instance is None:
        return

    if not {'primary', 'secondary'}.intersection(weapon_instance.tags):
        return

    attacker = ranked_player_manager.get_by_userid(game_event['attacker'])

    if attacker is None:
        return

    hitgroup_field = "hitgroup{}_hits".format(game_event['hitgroup'])
    attacker.data[hitgroup_field] = attacker.data.get(hitgroup_field, 0) + 1
    attacker.session_data[hitgroup_field] = attacker.session_data.get(
        hitgroup_field, 0) + 1

    attacker.data['shots_landed'] = attacker.data.get('shots_landed', 0) + 1
    attacker.session_data['shots_landed'] = attacker.session_data.get(
        'shots_landed', 0) + 1


@Event('weapon_fire')
def on_weapon_fire(game_event):
    weapon_instance = weapon_manager[game_event['weapon']]
    if weapon_instance is None:
        return

    if not {'primary', 'secondary'}.intersection(weapon_instance.tags):
        return

    player = ranked_player_manager.get_by_userid(game_event['userid'])

    if player is None:
        return

    player.data['shots_total'] = player.data.get('shots_total', 0) + 1
    player.session_data['shots_total'] = player.session_data.get(
        'shots_total', 0) + 1
