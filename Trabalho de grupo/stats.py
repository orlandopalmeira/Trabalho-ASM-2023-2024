from Config import Config as cfg

import json


filename = cfg.stats_file_name()

def write_stats(flights_path, results_path):

    with open(flights_path, "r") as f:
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

    res = {
        "average": avg,
        "flights": stats
    }

    with open(results_path, "w") as f:
        json.dump(res, f, indent=4)
    
    # Clear flights file
    with open(flights_path, 'w', encoding='utf-8') as f:
        json.dump([], f)

