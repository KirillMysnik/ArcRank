from colors import Color
from core import GAME_NAME

from advanced_ts import BaseLangStrings

from ..info import info


if GAME_NAME in ('csgo', ):
    COLOR_SCHEME = {
        'color_tag': "\x01",
        'color_highlight': "\x09",
        'color_default': "\x01",
        'color_error': "\x02",
        'color_points_earned': "\x05",
        'color_points_lost': "\x02",
    }

else:
    COLOR_SCHEME = {
        'color_tag': Color(242, 242, 242),
        'color_highlight': Color(255, 242, 0),
        'color_default': Color(242, 242, 242),
        'color_error': Color(255, 54, 54),
        'color_points_earned': Color(0, 220, 55),
        'color_points_lost': Color(225, 0, 65),
    }


strings_common = BaseLangStrings(info.basename + "/common")
strings_config = BaseLangStrings(info.basename + "/config")
strings_popups = BaseLangStrings(info.basename + "/popups")


def build_module_strings(module):
    return BaseLangStrings('/'.join((info.basename, 'modules', module)))
