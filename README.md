# nut_report

```
python nut_report.py match730_003697890146624995381_0051397283_129.dem
```

```
+-------+--------------------------+------------------------------------------+-----------+-------+
| round | player                   | killed                                   | time      | meter |
+-------+--------------------------+------------------------------------------+-----------+-------+
| 8     | WTFender (SideAlley)     | bbw (TSpawn), Bulla (SideAlley)          | 0.73 (47) |       |
| 11    | WTFender (Apartments)    | xeofobia (BackAlley), Bulla (BackAlley)  | 0.84 (54) |       |
| 11    | WTFender (Apartments)    | xeofobia (Catwalk), Bulla (Catwalk),     | 0.21 (13) | 🥜🥜 |
|       |                          | bbw (Catwalk)                            |           |       |
+-------+--------------------------+------------------------------------------+-----------+-------+
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
