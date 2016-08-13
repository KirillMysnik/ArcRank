from events import Event
from listeners import OnClientDisconnect

from ..ranked_player import ranked_player_manager, tell

from ..resource.strings import strings_common


points_earned_storage = {}
points_lost_storage = {}


def earn_points(player, points, reason):
    player.score += points
    points_earned_storage[player.player.index] = points_earned_storage.get(
        player.player.index, 0) + points

    tell(player, strings_common['points_earned'].tokenize(
         points=abs(points), reason=reason))


def lose_points(player, points, reason):
    player.score += points  # Note the "+" here: points is already signed
    points_lost_storage[player.player.index] = points_lost_storage.get(
        player.player.index, 0) + points

    tell(player, strings_common['points_lost'].tokenize(
         points=abs(points), reason=reason))


@OnClientDisconnect
def listener_on_client_disconnect(index):
    for dict_ in (points_earned_storage, points_lost_storage):
        if index in dict_:
            del dict_[index]


@Event('round_start')
def on_round_start(game_event):
    for index, player in ranked_player_manager.items():
        if not player.loaded:
            continue

        points_earned_storage[index] = 0
        points_lost_storage[index] = 0


@Event('round_end')
def on_round_end(game_event):
    for index, player in ranked_player_manager.items():
        if not player.loaded:
            continue

        points_earned = abs(points_earned_storage.get(index, 0))
        points_lost = abs(points_lost_storage.get(index, 0))

        tell(player, strings_common['points_diff_round'],
             plus=points_earned, minus=points_lost)
