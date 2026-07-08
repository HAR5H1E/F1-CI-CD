import fastf1
from fastf1 import Cache
from pathlib import Path

cacheDir = Path("./DataCache")
cacheDir.mkdir(parents=True,exist_ok=True)

Cache.enable_cache(cacheDir)

schecule = [fastf1.get_event_schedule(2023,include_testing=False),
            fastf1.get_event_schedule(2024,include_testing=False),
            fastf1.get_event_schedule(2023,include_testing=False)]

