# nut_report
### Install
```
pip install nut-report
```
### Usage
```sh
nut_report                             # default demos folder
nut_report "c:/path/to/demos/"         # load a folder
nut_report "c:/path/to/demos/demo.dem" # load a demo
```
### Nut Report
```
  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐
  │                                                                                             │
  │  Nut Reporter                                                                               │
  │                                                                                             │
  │  +---+----+-----+------+-------+---------------------------------------------------+        │
  │  | * | ** | *** | **** | ***** | kills, timing, and location affects the nut meter |        │
  │  +---+----+-----+------+-------+---------------------------------------------------+        │
  │                                                                                             │
  │                                                                                             │
  │  Select a demo:                                                                             │
  │                                                                                             │
  │                                                                                             │
  │    1 - 08/02/24 23:13 de_inferno (2)                                                        │
  │    2 - 08/02/24 23:13 de_dust2 (0)                                                          │
  │    3 - 08/02/24 23:12 de_nuke (0)                                                           │
  │    4 - 07/31/24 20:58 de_inferno (2)                                                        │
  │    5 - 07/29/24 20:01 de_nuke (0)                                                           │
  │    6 - 07/28/24 10:43 de_nuke (2)                                                           │
  │    7 - 07/27/24 21:53 de_mirage (0)                                                         │
  │    q - Quit                                                                                 │
  │                                                                                             │
  │                                                                                             │
  │  C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global                        │
  │  Offensive\game\csgo\replays                                                                │
  │                                                                                             │
  │                                                                                             │
  └─────────────────────────────────────────────────────────────────────────────────────────────┘
```
List multikill events for a match that happened within `KILL_THRESHOLD_SECONDS`.
- Round
- [Meter](#Meter)
- Time - seconds (ticks)
- Player (location)
- Killed (location)
```
  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐
  │                                                                                             │
  │  #1 08/02/24 23:13                                                                          │
  │  Valve Counter-Strike 2 us_north_central Server (srcds1012-ord1.129.109)                    │
  │  de_inferno                                                                                 │
  │                                                                                             │
  │  meter         round         time          player              killed                       │
  │  ***           2             0.02          something           Papa (CTSpawn), Henry        │
  │                              (1)           (Arch)              (CTSpawn)                    │
  │  *             10            0.61          something           Henry (TopofMid), Papa       │
  │                              (39)          (Middle)            (TopofMid)                   │
  │                                                                                             │
  │                                                                                             │
  │    s - Send Webhook (discord.com)                                                           │
  │    b - Back                                                                                 │
  │                                                                                             │
  │                                                                                             │
  │  KILL_THRESHOLD_SECONDS: 1                                                                  │
  │                                                                                             │
  │                                                                                             │
  └─────────────────────────────────────────────────────────────────────────────────────────────┘
```


#### [Meter](https://github.com/WTFender/nut_report/blob/fa145727ccdeb751d9436da938b3690e7fd985c4/nut_report.py#L24)
- Only multikill events that fall within `KILL_THRESHOLD_SECONDS` get rated
- Pulling in more variables related to movement and direction would contribute a lot
- There are simple indicators of cheating, such as the attacker being in 3+ named map zones in under a certain period of time
```python
def get_rating(num_kills, num_zones, time):
    if ((num_kills >= 4 and time <= 0.1)
        or (num_kills >= 3 and time <= 0.1 and num_zones >= 2)
        or (num_zones >= 3)):
        return NUT * 5
    elif (num_kills >= 4 and time <= 0.25)
        or (num_kills >= 3 and time <= 0.25 and num_zones >= 2):
        return NUT * 4
    elif (num_kills >= 2 and time <= 0.25)
        or (num_kills >= 2 and time <= 0.5 and num_zones >= 2):
        return NUT * 3
    elif (num_kills >= 2 and time <= 0.5)
        or (num_kills >= 2 and time <= 1 and num_zones >= 2):
        return NUT * 2
    else:
        return NUT
```

### Settings
Set envars or create a .env file to customize settings.
```
KILL_THRESHOLD_SECONDS=1
NR_WEBHOOK_URL="https://discord.com/api/webhooks/XYZ"
```
