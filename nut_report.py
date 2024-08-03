from dotenv import find_dotenv, load_dotenv
from consolemenu import ConsoleMenu, MenuFormatBuilder
from consolemenu.items import FunctionItem, SubmenuItem, CommandItem
from consolemenu import SelectionMenu
from consolemenu.menu_component import Dimension
from os import listdir, path, getenv
from datetime import datetime as dt
from demoparser2 import DemoParser
from sys import argv, exit
import pandas as pd
import numpy as np
from prettytable import PrettyTable, PLAIN_COLUMNS
import requests
import inspect


pd.set_option("mode.chained_assignment", None)
pd.set_option("display.max_rows", 500)


def nut_chart():
    chart = PrettyTable(["1", "2", "3", "4", "5", "6"])
    chart.add_row(
        [
            "nut meter",
            NUT,
            (NUT * 2),
            (NUT * 3),
            (FIRE * 3),
            f"kills, timing & location influence the nut meter",
        ]
    )
    chart.align = "l"
    chart.header = False
    return chart.get_string()


def get_rating(num_kills, num_zones, time):
    # rate multikill events that happen within KILL_THRESHOLD_SECONDS
    if (
        (num_kills >= 4 and time <= 0.1)
        or (num_kills >= 3 and time <= 0.1 and num_zones >= 2)
        or (num_zones >= 3)
    ):
        return FIRE * 3
    elif (num_kills >= 4 and time <= 0.25) or (
        num_kills >= 3 and time <= 0.25 and num_zones >= 2
    ):
        return NUT * 3
    elif (num_kills >= 2 and time <= 0.25) or (
        num_kills >= 2 and time <= 0.5 and num_zones >= 2
    ):
        return NUT * 2
    elif (num_kills >= 2 and time <= 0.5) or (
        num_kills >= 2 and time <= 1 and num_zones >= 2
    ):
        return NUT
    else:
        return ""  # no nuts


def get_rating_text():
    rating_text = inspect.getsource(get_rating)
    # trim first and last line from multiline string `rating_text`
    return "\n".join(rating_text.split("\n")[1:-1])


def parse_demo(demoFilePath):
    parser = DemoParser(demoFilePath)
    created = dt.fromtimestamp(path.getctime(demoFilePath)).strftime("%m/%d/%y %H:%M")
    info = parser.parse_header()
    info["created"] = created
    df = parser.parse_event(
        "player_death",
        player=["last_place_name", "team_name", "game_time"],
        other=["total_rounds_played", "is_warmup_period"],
    )
    df = df.replace(np.nan, None)
    columns = [
        "total_rounds_played",
        "game_time",
        "game_time_diff",
        "tick",
        "attacker_name",
        "attacker_last_place_name",
        "user_name",
        "user_last_place_name",
    ]

    # filter out team-kills and warmup
    df = df[df["attacker_team_name"] != df["user_team_name"]]
    df = df[df["is_warmup_period"] == False]

    player_events = []

    players_kills_by_round = (
        df.groupby(["total_rounds_played", "attacker_name"])
        .size()
        .to_frame(name="total_kills")
        .reset_index()
    )
    players_with_multi_kills = (
        players_kills_by_round[players_kills_by_round["total_kills"] > 2][
            "attacker_name"
        ]
        .unique()
        .tolist()
    )

    for player in players_with_multi_kills:
        player_kills = df[df["attacker_name"] == player]
        player_kills["game_time_diff"] = player_kills["game_time"].diff()
        # player_kills = player_kills[player_kills["game_time_diff"] < KILL_THRESHOLD_SECONDS]

        quick_kills = []

        for idx, kill in player_kills.iterrows():
            kill = kill[columns].to_dict()

            # capture streak
            if kill["game_time_diff"] < KILL_THRESHOLD_SECONDS:
                kill_previous = player_kills.iloc[player_kills.index.get_loc(idx) - 1][
                    columns
                ].to_dict()
                if kill_previous not in quick_kills:
                    quick_kills.append(kill_previous)
                quick_kills.append(kill)

            # end streak
            elif quick_kills:
                player_events.append(
                    {
                        "player": player,
                        "round": quick_kills[0]["total_rounds_played"],
                        "start": quick_kills[0]["game_time"],
                        "time": quick_kills[len(quick_kills) - 1]["game_time"]
                        - quick_kills[0]["game_time"],
                        "ticks": quick_kills[len(quick_kills) - 1]["tick"]
                        - quick_kills[0]["tick"],
                        "kills": quick_kills,
                        "zones": list(
                            set(
                                [
                                    kill["attacker_last_place_name"]
                                    for kill in quick_kills
                                ]
                            )
                        ),
                    }
                )
                quick_kills = []

        # cleanup any remaining streaks
        if quick_kills:
            player_events.append(
                {
                    "player": player,
                    "round": quick_kills[0]["total_rounds_played"],
                    "start": quick_kills[0]["game_time"],
                    "time": quick_kills[len(quick_kills) - 1]["game_time"]
                    - quick_kills[0]["game_time"],
                    "ticks": quick_kills[len(quick_kills) - 1]["tick"]
                    - quick_kills[0]["tick"],
                    "kills": quick_kills,
                    "zones": list(
                        set([kill["attacker_last_place_name"] for kill in quick_kills])
                    ),
                }
            )
    return player_events, info


def create_report(
    player_events, info, include_chart=False, include_rating=False, include_header=True
):
    report = PrettyTable(
        ["round", "player", "killed", "time", "meter"], sort_by="round"
    )
    report.set_style(PLAIN_COLUMNS)
    report.align = "l"
    report.min_table_width = 100
    widths = {"round": 1, "player": 20, "killed": 35, "time": 10, "meter": 1}
    report._min_width = widths
    report._max_width = widths

    for event in player_events:
        event["meter"] = get_rating(
            len(event["kills"]), len(event["zones"]), event["time"]
        )
        report.add_row(
            [
                event["round"],
                f"{event['player']} ({', '.join(event['zones'])})",
                ", ".join(
                    [
                        f"{kill['user_name']} ({kill['user_last_place_name']})"
                        for kill in event["kills"]
                    ]
                ),
                f'{float("{:.2f}".format(event["time"]))} ({event["ticks"]})',
                event["meter"],
            ]
        )

    report_str = report.get_string(sortby="round")
    if include_chart:
        report_str = report_str + "\n" + nut_chart()
    if include_rating:
        report_str = report_str + "\n" + get_rating_text()
    if include_header:
        header = PrettyTable(["1", "2"])
        header.header = False
        header.align = "l"
        header.add_row([info["map_name"], info["server_name"]])
        report_str = header.get_string() + "\n" + report_str
    return report_str


def summarize_events(events):
    report = PrettyTable(["demo created", "map", "nut_events", "nut_players"])
    report.align = "l"
    report._max_width = {"nut_players": 25, "killed": 40}

    for event in events:
        report.add_row(
            [
                event["info"]["created"],
                event["info"]["map_name"],
                len(event["player_events"]),
                ", ".join(
                    [
                        f"{event['player']}{event['meter']}"
                        for event in event["player_events"]
                    ]
                ),
            ]
        )
    return report.get_string(sortby="demo created")


def send_webhook(url, payload):
    if not url:
        raise Exception(f"No webhook url provided: {url}")
    nutreport = {
        "username": "NutReport",
        "content": f"```{payload}```",
    }
    resp = requests.post(url, json=nutreport)
    if resp.status_code >= 400:
        raise Exception(f"Failed to send webhook: {resp.text}")
    return resp


if __name__ == "__main__":

    # cfg
    load_dotenv(find_dotenv())
    WEBHOOK_URL = getenv("WEBHOOK_URL", None)

    # settings
    INCLUDE_CHART = False
    INCLUDE_RATING = False
    INCLUDE_HEADER = False
    USE_EMOJIS = False
    POST_WEBHOOK = True
    POST_SUMMARY_ONLY = True
    KILL_THRESHOLD_SECONDS = 1
    DEFAULT_PATH = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Counter-Strike Global Offensive\\game\\csgo\\replays"

    NUT = "*"
    FIRE = "$"
    if USE_EMOJIS:
        NUT = "🥜"
        FIRE = "🔥"

    # get demo file path
    if len(argv) > 1:
        argFilePath = argv[1]
    else:
        argFilePath = DEFAULT_PATH

    # check that file exists
    if not path.exists(argFilePath):
        print(f"File does not exist: {argFilePath}")
        exit(1)

    # determine if demo or directory of demos
    demoFilePaths = []
    if path.isdir(argFilePath):
        demoFilePaths = [
            path.join(argFilePath, f)
            for f in listdir(argFilePath)
            if f.endswith(".dem")
        ]
    else:
        demoFilePaths = [argFilePath]

    reports = []

    for demoFilePath in demoFilePaths:
        # parse demo, create report
        player_events, info = parse_demo(demoFilePath)
        report = create_report(
            player_events,
            info,
            include_chart=INCLUDE_CHART,
            include_rating=INCLUDE_RATING,
            include_header=INCLUDE_HEADER,
        )
        reports.append(
            {
                "report": report,
                "player_events": player_events,
                "info": info,
            }
        )

    # sort reports by created date
    reports = sorted(reports, key=lambda x: x["info"]["created"])
    reports.reverse()

    summary = summarize_events(reports)

    thin = Dimension(
        width=120, height=60
    )  # Use a Dimension to limit the "screen width" to 40 characters
    menu_format = MenuFormatBuilder(max_dimension=thin)
    menu = ConsoleMenu(
        f"Nut Reporter",
        nut_chart(),
        prologue_text=("Select a demo:"),
        epilogue_text=(f"Loaded: {argFilePath}"),
        exit_menu_char="q",
        exit_option_text="quit",
    )
    menu.formatter = menu_format

    if len(reports) == 1:
        menu.prologue_text = reports[0]["report"]

    elif len(reports) > 1:
        for idx, r in enumerate(reports):
            header = "\n".join(
                [
                    f"#{idx+1}",
                    r["info"]["server_name"],
                    r["info"]["created"],
                    r["info"]["map_name"],
                ]
            )
            submenu = ConsoleMenu(
                header,
                r["report"],
            )
            submenu.append_item(FunctionItem("Send Webhook", send_webhook, (WEBHOOK_URL, r['report']), menu_char='1', should_exit=True))
            submenu.formatter = menu_format
            submenu_item = SubmenuItem(
                f"{r['info']['created']} {r['info']['map_name']} ({len(r['player_events'])})",
                submenu,
                menu=menu,
            )
            menu.append_item(submenu_item)
    menu.show()
