"""
implement ``SubtitleTranslator``
"""

import shutil
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

from pyjson5 import load as json5_load

CONFIG_FILE_PATH = (Path(__file__).parent / "config.json").resolve()
DEFAULT_CONFIG_FILE_PATH = (
    Path(__file__).parent / "config.default.json"
).resolve()


class SubtitleTranslator:
    """
    TODO

    :param episode:
    :type episode: SubtitleTranslator
    """

    def __init__(self, episode):
        self.episode = episode
        self.config = self._load_config_from_file()

    @staticmethod
    def _load_config_from_file():
        # ensure config.json exists
        if not CONFIG_FILE_PATH.exists():
            CONFIG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(DEFAULT_CONFIG_FILE_PATH, CONFIG_FILE_PATH)

        with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as f:
            return json5_load(f)


# TODO refactor as a class

MAX_WORKERS = 8
LINES_PER_RESPONSE = 2  # HACK


def _translation_worker(episode, i):
    end = (i + 1) * LINES_PER_RESPONSE
    if end > len(episode):  # special case last set
        end = len(episode)

    translated_lines = []

    for line in episode.lines[i * LINES_PER_RESPONSE : end]:
        translated_lines.append(line.swapcase())  # HACK

    return (i, translated_lines)


def translate(src_file_path, dest_file_path):

    episode_type = SrtSubtitleEpisode  # HACK

    with episode_type(src_file_path, dest_file_path) as episode:
        updates = []
        with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [
                executor.submit(_translation_worker, episode, i)
                for i in range(len(episode))
            ]

            for future in as_completed(futures):
                updates.append(future.result())  # BUG

        for i, payload in updates:
            episode.translated_lines[i * LINES_PER_RESPONSE] = payload
