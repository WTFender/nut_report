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
  │  C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\replays                │
  │                                                                                                                 │
  │                                                                                                                 │
  │  Select a demo:                                                                                                 │
  │                                                                                                                 │
  │                                                                                                                 │
  │    1 - 07/27/24 21:53 de_mirage (0)                                                                             │
  │    2 - 07/28/24 10:43 de_nuke (2)                                                                               │
  │    3 - 07/29/24 20:01 de_nuke (0)                                                                               │
  │    4 - 08/02/24 23:13 de_dust2 (0)                                                                              │
  │    5 - 07/31/24 20:58 de_inferno (2)                                                                            │
  │    6 - 08/02/24 23:12 de_nuke (0)                                                                               │
  │    7 - 08/02/24 23:13 de_inferno (2)                                                                            │
  │    Q - Quit                                                                                                     │
  │                                                                                                                 │
  │                                                                                                                 │
  │  +-----------+---+----+-----+-----+--------------------------------------------------+                          │
  │  | nut meter | * | ** | *** | $$$ | kills, timing & location influence the nut meter |                          │
  │  +-----------+---+----+-----+-----+--------------------------------------------------+                          │
  │                                                                                                                 │
  │                                                                                                                 │
  └─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```
  ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
  │                                                                                                                 │
  │  08/02/24 23:13                                                                                                 │
  │  Valve Counter-Strike 2 us_north_central Server (srcds1012-ord1.129.109)                                        │
  │  de_inferno                                                                                                     │
  │                                                                                                                 │
  │  round        player                    killed                                   time             meter         │
  │  2            something (Arch)          Papa (CTSpawn), Henry (CTSpawn)          0.02 (1)         **            │
  │  10           something (Middle)        Henry (TopofMid), Papa (TopofMid)        0.61 (39)                      │
  │                                                                                                                 │
  │                                                                                                                 │
  │    1 - Return to Nut Reporter                                                                                   │
  │                                                                                                                 │
  │                                                                                                                 │
  └─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

[Adjust accordingly](https://github.com/WTFender/nut_report/blob/fa145727ccdeb751d9436da938b3690e7fd985c4/nut_report.py#L24)
```python
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
```
