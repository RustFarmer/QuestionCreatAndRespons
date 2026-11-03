from dataclasses import dataclass
from firstRun import get_absolute_path

file_path = get_absolute_path()

@dataclass(frozen=True)
class File_path:
    topic_settings = f"{file_path}/Topic/data/topic_settings.json"
    topic_save = f"{file_path}/Topic/data/topic_save.json"
    