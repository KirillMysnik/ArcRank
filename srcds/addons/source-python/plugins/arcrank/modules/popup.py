from menus import PagedMenu, PagedOption

from ..resource.strings import build_module_strings

from .server import server


strings_module = build_module_strings('popup')


def popup_select_callback(popup, index, option):
    pass


def send_popup(player, db_ranked_players, title):
    popup = PagedMenu(select_callback=popup_select_callback, title=title)

    for db_ranked_player in db_ranked_players:
        popup.append(PagedOption(
            text=strings_module['popup entry'].tokenize(
                player=db_ranked_player.last_used_name,
                score=db_ranked_player.score,
                pos=db_ranked_player.position,
                total=server.total_positions,
            ),
            value=db_ranked_player.steamid,
        ))

    popup.send(player.player.index)
