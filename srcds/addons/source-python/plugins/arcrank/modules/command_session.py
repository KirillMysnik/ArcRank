from datetime import timedelta

from menus import SimpleMenu, SimpleOption, Text

from spam_proof_commands.say import SayCommand

from ..ranked_player import ranked_player_manager

from ..resource.strings import build_module_strings

from .server import server


strings_module = build_module_strings('command_session')


def session_popup_select_callback(popup, index, option):
    pass


def send_session_popup(player):
    popup = SimpleMenu(select_callback=session_popup_select_callback)

    # "Total" title
    popup.append(SimpleOption(1, strings_module['popup entry total']))

    # Total position
    if player.position < 1:
        popup.append(Text(strings_module['popup entry not_ranked']))
    else:
        popup.append(Text(strings_module['popup entry position'].tokenize(
            pos=player.position, total=server.total_positions)))

    # Score (points)
    popup.append(Text(strings_module['popup entry score'].tokenize(
        score=player.score)))

    # Frag info
    kills = player.data.get('kills', 0)
    deaths = player.data.get('deaths', 0)
    if deaths == 0:
        if kills == 0:
            kdr = "???"
        else:
            kdr = "inf"
    else:
        kdr = "{:.2f}".format(kills / deaths)

    popup.append(Text(strings_module['popup entry kdr'].tokenize(
        kills=kills, deaths=deaths, kdr=kdr)))

    # Headshot info
    hs_kills = player.data.get('headshot_kills', 0)
    if kills == 0:
        hs_ratio = "???"
    else:
        hs_ratio = "{:.2f}".format(hs_kills / kills)

    popup.append(Text(strings_module['popup entry headshots'].tokenize(
        headshots=hs_kills, ratio=hs_ratio)))

    # Accuracy
    shots_total = player.data.get('shots_total', 0)
    shots_landed = player.data.get('shots_landed', 0)
    if shots_total == 0:
        shots_ratio = "???"
    else:
        shots_ratio = "{:.2f}".format(shots_landed / shots_total)

    popup.append(Text(strings_module['popup entry accuracy'].tokenize(
        ratio=shots_ratio, shots_total=shots_total)))

    # Online time
    td = timedelta(seconds=player.online_time)
    popup.append(Text(strings_module['popup entry online_time'].tokenize(
        online_time=str(td))))

    # Blank line
    popup.append(Text(" "))

    # "Session" title
    popup.append(SimpleOption(2, strings_module['popup entry session']))

    # Session position delta
    if player.position < 1:
        popup.append(Text(strings_module['popup entry not_ranked']))
    else:
        pos_delta = player.position - player.session_initial_position
        if pos_delta == 0:
            popup.append(Text(strings_module['popup entry same_position']))
        elif pos_delta > 0:
            popup.append(Text(strings_module['popup entry down_x_positions'].
                              tokenize(x=pos_delta)))
        else:
            popup.append(Text(strings_module['popup entry up_x_positions'].
                              tokenize(x=pos_delta)))

    # Score (points) delta
    score_delta = "{:+d}".format(player.session_score)
    popup.append(Text(strings_module['popup entry score'].tokenize(
        score=score_delta)))

    # Session frag info
    kills = player.session_data.get('kills', 0)
    deaths = player.session_data.get('deaths', 0)
    if deaths == 0:
        if kills == 0:
            kdr = "???"
        else:
            kdr = "inf"
    else:
        kdr = "{:.2f}".format(kills / deaths)

    popup.append(Text(strings_module['popup entry kdr'].tokenize(
        kills=kills, deaths=deaths, kdr=kdr)))

    # Session headshot info
    hs_kills = player.session_data.get('headshot_kills', 0)
    if kills == 0:
        hs_ratio = "???"
    else:
        hs_ratio = "{:.2f}".format(hs_kills / kills)

    popup.append(Text(strings_module['popup entry headshots'].tokenize(
        headshots=hs_kills, ratio=hs_ratio)))

    # Session accuracy
    shots_total = player.session_data.get('shots_total', 0)
    shots_landed = player.session_data.get('shots_landed', 0)
    if shots_total == 0:
        shots_ratio = "???"
    else:
        shots_ratio = "{:.2f}".format(shots_landed / shots_total)

    popup.append(Text(strings_module['popup entry accuracy'].tokenize(
        ratio=shots_ratio, shots_total=shots_total)))

    # Session online time
    td = timedelta(seconds=player.session_online_time)
    popup.append(Text(strings_module['popup entry online_time'].tokenize(
        online_time=str(td))))

    # Blank line
    popup.append(Text(" "))

    # Send popup
    popup.send(player.player.index)


@SayCommand(3, ['session', '!session', '/session'])
def say_session(command, index, team_only):
    player = ranked_player_manager[index]
    send_session_popup(player)
