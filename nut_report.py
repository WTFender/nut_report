
from demoparser2 import DemoParser
from dotenv import load_dotenv
from os import path, getenv
from sys import argv
import pandas as pd
import numpy as np
import prettytable
import requests
import inspect


pd.set_option('mode.chained_assignment', None)
pd.set_option('display.max_rows', 500)


def nut_chart():
    chart = prettytable.PrettyTable(["1", "2", "3", "4", "5", "6"])
    chart.add_row(["nut meter", "🥜", "🥜🥜", "🥜🥜🥜", "🔥🔥🔥", f"kills, timing & location influence the nut meter"])
    chart.align = "l"
    chart.header = False
    return chart.get_string()

def get_rating(num_kills, num_zones, time):
    # rate multikill events that happen within KILL_THRESHOLD_SECONDS
    if ((num_kills >= 4 and time <= .1) or
        (num_kills >= 3 and time <= .1 and num_zones >= 2) or
        (num_zones >= 3)): 
        return "🔥" * 3
    elif ((num_kills >= 4 and time <= .25) or
          (num_kills >= 3 and time <= .25 and num_zones >= 2)):
        return "🥜" * 3
    elif ((num_kills >= 2 and time <= .25) or
          (num_kills >= 2 and time <= .5 and num_zones >= 2)
        ):
        return "🥜" * 2
    elif ((num_kills >= 2 and time <= .5) or
          (num_kills >= 2 and time <= 1 and num_zones >= 2)
        ):
        return "🥜"
    else:
        return "" # no nuts

def get_rating_text():
    rating_text = inspect.getsource(get_rating)
    # trim first and last line from multiline string `rating_text`
    return "\n".join(rating_text.split("\n")[1:-1])

def parse_demo(demoFilePath):
    parser = DemoParser(demoFilePath)
    info = parser.parse_header()
    df = parser.parse_event("player_death", player=["last_place_name", "team_name", "game_time"], other=["total_rounds_played", "is_warmup_period"])
    df = df.replace(np.nan, None)
    columns = ["total_rounds_played", "game_time", "game_time_diff", "tick", "attacker_name", "attacker_last_place_name", "user_name", "user_last_place_name"]

    # filter out team-kills and warmup
    df = df[df["attacker_team_name"] != df["user_team_name"]]
    df = df[df["is_warmup_period"] == False]

    player_events = []

    players_kills_by_round = df.groupby(["total_rounds_played", "attacker_name"]).size().to_frame(name='total_kills').reset_index()
    players_with_multi_kills = players_kills_by_round[players_kills_by_round["total_kills"] > 2]["attacker_name"].unique().tolist()

    for player in players_with_multi_kills:
        player_kills = df[df["attacker_name"] == player]
        player_kills['game_time_diff'] = player_kills['game_time'].diff()
        #player_kills = player_kills[player_kills["game_time_diff"] < KILL_THRESHOLD_SECONDS]

        quick_kills = []

        for idx, kill in player_kills.iterrows():
            kill = kill[columns].to_dict()

            # capture streak
            if kill["game_time_diff"] < KILL_THRESHOLD_SECONDS:
                kill_previous = player_kills.iloc[player_kills.index.get_loc(idx)-1][columns].to_dict()
                if kill_previous not in quick_kills:
                    quick_kills.append(kill_previous)
                quick_kills.append(kill)
            
            # end streak
            elif quick_kills:
                player_events.append({
                    "player": player,
                    "round": quick_kills[0]["total_rounds_played"],
                    "start": quick_kills[0]["game_time"],
                    "time": quick_kills[len(quick_kills)-1]["game_time"] - quick_kills[0]["game_time"],
                    "ticks": quick_kills[len(quick_kills)-1]["tick"] - quick_kills[0]["tick"],
                    "kills": quick_kills,
                    "zones": list(set([kill["attacker_last_place_name"] for kill in quick_kills]))
                })
                quick_kills = []
        
        # cleanup any remaining streaks
        if quick_kills:
            player_events.append({
                "player": player,
                "round": quick_kills[0]["total_rounds_played"],
                "start": quick_kills[0]["game_time"],
                "time": quick_kills[len(quick_kills)-1]["game_time"] - quick_kills[0]["game_time"],
                "ticks": quick_kills[len(quick_kills)-1]["tick"] - quick_kills[0]["tick"],
                "kills": quick_kills,
                "zones": list(set([kill["attacker_last_place_name"] for kill in quick_kills]))
            })
    return player_events, info

def create_report(player_events, info, include_chart=False, include_rating=False, include_header=True):
    report = prettytable.PrettyTable(["round", "player", "killed", "time", "meter"], sort_by="round")
    report.align = "l"
    report._max_width = {"player": 25, "killed" : 40}

    for event in player_events:
        event["meter"] = get_rating(len(event["kills"]), len(event["zones"]), event["time"])
        report.add_row(
            [event["round"],
            f"{event['player']} ({', '.join(event['zones'])})",
            ", ".join([f"{kill['user_name']} ({kill['user_last_place_name']})" for kill in event['kills']]),
            f'{float("{:.2f}".format(event["time"]))} ({event["ticks"]})',
            event["meter"]]
        )

    report_str = report.get_string(sortby="round")
    if include_chart:
        report_str = report_str + "\n" + nut_chart()
    if include_rating:
        report_str = report_str + "\n" + get_rating_text()
    if include_header:
        header = prettytable.PrettyTable(["1", "2"])
        header.header = False
        header.align = "l"
        header.add_row([info['map_name'], info['server_name']])
        report_str = header.get_string() + "\n" + report_str
    return report_str

def send_webhook(url, payload):
    nutreport = {
        "username": "NutReport",
        "content": f"```{payload}```",
    }
    return requests.post(url, json=nutreport)


if __name__ == "__main__":
    # cfg
    load_dotenv()
    WEBHOOK_URL = getenv("WEBHOOK_URL", None)

    # settings
    INCLUDE_CHART = True
    INCLUDE_RATING = False
    INCLUDE_HEADER = True
    POST_WEBHOOK = False
    KILL_THRESHOLD_SECONDS = 1

    # get demo file path
    if len(argv) > 1:
        demoFilePath = argv[1]
    else:
        demoFilePath = input('Demo FilePath: ')

    # check that file exists
    if not path.exists(demoFilePath):
        print(f"File does not exist: {demoFilePath}")
        exit(1)

    # parse demo, create report
    player_events, info = parse_demo(demoFilePath)
    report = create_report(
        player_events,
        info,
        include_chart=INCLUDE_CHART,
        include_rating=INCLUDE_RATING,
        include_header=INCLUDE_HEADER,
    )
    print(report)

    # "addons", "server_name", "demo_file_stamp", "network_protocol", "map_name", "fullpackets_version", "allow_clientside_entities", "allow_clientside_particles", "demo_version_name", "demo_version_guid", "client_name", "game_directory"

    # notify
    if POST_WEBHOOK and WEBHOOK_URL:
        send_webhook(WEBHOOK_URL, report)
