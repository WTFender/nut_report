# nut_report

### Usage
```sh
python nut_report.py                             # default csgo folder
python nut_report.py "c:/path/to/demos/"         # load a folder
python nut_report.py "c:/path/to/demos/demo.dem" # load a demo
```
```
  ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
  │                                                                                                                 │
  │  Nut Reporter                                                                                                   │
  │                                                                                                                 │
  │  +-----------+---+----+-----+-----+--------------------------------------------------+                          │
  │  | nut meter | * | ** | *** | $$$ | kills, timing & location influence the nut meter |                          │
  │  +-----------+---+----+-----+-----+--------------------------------------------------+                          │
  │                                                                                                                 │
  │                                                                                                                 │
  │  Select a demo:                                                                                                 │
  │                                                                                                                 │
  │                                                                                                                 │
  │    1 - 08/02/24 23:13 de_inferno (2)                                                                            │
  │    2 - 08/02/24 23:13 de_dust2 (0)                                                                              │
  │    3 - 08/02/24 23:12 de_nuke (0)                                                                               │
  │    4 - 07/31/24 20:58 de_inferno (2)                                                                            │
  │    5 - 07/29/24 20:01 de_nuke (0)                                                                               │
  │    6 - 07/28/24 10:43 de_nuke (2)                                                                               │
  │    7 - 07/27/24 21:53 de_mirage (0)                                                                             │
  │    q - quit                                                                                                     │
  │                                                                                                                 │
  │                                                                                                                 │
  │  Loaded: C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\replays        │
  │                                                                                                                 │
  │                                                                                                                 │
  └─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```
  ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
  │                                                                                                                 │
  │  #6                                                                                                             │
  │  Valve Counter-Strike 2 us_north_central Server (srcds1007-ord1.129.40)                                         │
  │  07/28/24 10:43                                                                                                 │
  │  de_nuke                                                                                                        │
  │                                                                                                                 │
  │  round        player                      killed                                     time              meter    │
  │  1            WTFender (Outside)          Jotherc (Outside), Deathray2               0.73 (47)                  │
  │                                           (Outside)                                                             │
  │  15           seon (Decon)                pross (BombsiteB), Jegao                   0.39 (25)         *        │
  │                                           (BombsiteB)                                                           │
  │                                                                                                                 │
  │                                                                                                                 │
  │    1 - Send Webhook                                                                                             │
  │    2 - Return to Nut Reporter                                                                                   │
  │                                                                                                                 │
  │                                                                                                                 │
  └─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

[Adjust accordingly](https://github.com/WTFender/nut_report/blob/fa145727ccdeb751d9436da938b3690e7fd985c4/nut_report.py#L24)
```python
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
```
