from Config import Config as cfg

import json


filename = cfg.stats_file_name()
with open(filename, "r") as f:
    stats = json.load(f)

avg = {
    "waiting_takeoff": stats[0]["waiting_takeoff"],
    "waiting_landing": stats[0]["waiting_landing"]
}

for s in stats[1:]:
    avg["waiting_takeoff"] += s["waiting_takeoff"]
    avg["waiting_landing"] += s["waiting_landing"]

avg["waiting_takeoff"] /= len(stats)
avg["waiting_landing"] /= len(stats)

avg["waiting_takeoff"] = round(avg["waiting_takeoff"], 2)
avg["waiting_landing"] = round(avg["waiting_landing"], 2)

print(avg)

