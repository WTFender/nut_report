from nut_report.nut_report import *

from consolemenu.items import FunctionItem, SubmenuItem
from consolemenu import ConsoleMenu, MenuFormatBuilder
from consolemenu.menu_component import Dimension
from dotenv import find_dotenv, load_dotenv
from os import listdir, path, getenv
from urllib.parse import urlparse
from sys import argv, exit

def main():
    # cfg
    load_dotenv(find_dotenv())
    KILL_THRESHOLD_SECONDS = float(getenv("KILL_THRESHOLD_SECONDS", 1))
    WEBHOOK_URL = getenv("NR_WEBHOOK_URL", None)

    # settings
    USE_EMOJIS = False
    DEFAULT_PATH = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Counter-Strike Global Offensive\\game\\csgo\\replays"

    NUT = "*"
    if USE_EMOJIS:
        NUT = "🥜"

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

    if len(demoFilePaths) > 0:
        print(f"Loading {len(demoFilePaths)} demo(s) from {argFilePath}")
    else:
        print(f"No demos found in {argFilePath}")
        exit(0)

    reports = []

    for demoFilePath in demoFilePaths:
        # parse demo, create report
        player_events, info = parse_demo(demoFilePath, KILL_THRESHOLD_SECONDS=KILL_THRESHOLD_SECONDS)
        report = create_report(
            player_events,
            info,
            icon=NUT,
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

    # summary = summarize_events(reports)

    thin = Dimension(
        width=100, height=40
    )  # Use a Dimension to limit the "screen width" to 40 characters
    menu_format = MenuFormatBuilder(max_dimension=thin)
    menu = ConsoleMenu(
        f"Nut Reporter",
        nut_chart(icon=NUT),
        prologue_text=("Select a demo:"),
        epilogue_text=(argFilePath),
        exit_menu_char="q",
        exit_option_text="Quit",
    )
    menu.formatter = menu_format

    if len(reports) == 1:
        menu.prologue_text = reports[0]["report"]

    elif len(reports) > 1:
        for idx, r in enumerate(reports):
            header = "\n".join(
                [
                    f"#{idx+1} {r["info"]["created"]}",
                    r["info"]["server_name"],
                    r["info"]["map_name"],
                ]
            )
            submenu = ConsoleMenu(
                header,
                r["report"],
                epilogue_text=f"KILL_THRESHOLD_SECONDS: {KILL_THRESHOLD_SECONDS}",
                exit_option_text="Back",
                exit_menu_char="b",
            )
            if WEBHOOK_URL:
                submenu.append_item(
                    FunctionItem(
                        f"Send Webhook ({(urlparse(WEBHOOK_URL).netloc)})",
                        send_webhook,
                        (WEBHOOK_URL, r["report"]),
                        menu_char="s",
                    )
                )
            submenu.formatter = menu_format
            submenu_item = SubmenuItem(
                f"{r['info']['created']} {r['info']['map_name']} ({len(r['player_events'])})",
                submenu,
                menu=menu,
            )
            menu.append_item(submenu_item)
    menu.show()
