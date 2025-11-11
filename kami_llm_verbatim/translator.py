"""
implement ``SubtitleTranslator``
"""

import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import math

from pyjson5 import load as json5_load

from kamilog import kamilog

CONFIG_FILE_PATH = (Path(__file__).parent / "config.json").resolve()
DEFAULT_CONFIG_FILE_PATH = (
    Path(__file__).parent / "config.default.json"
).resolve()


logger = kamilog.getLogger()


class SubtitleTranslator:
    """
    TODO

    """

    def __init__(self):
        # load various configs if never loaded into class
        if self._config is None:
            # ensure config.json exists
            if not CONFIG_FILE_PATH.exists():
                CONFIG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(DEFAULT_CONFIG_FILE_PATH, CONFIG_FILE_PATH)

            with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as f:
                self._config = json5_load(f)

            logger.debug("load config.json:\n%s", self._config)

            # read configs  ----------------------------------------------------
            self._max_responses = self._config["max_responses"]
            self._lines_per_response = self._config["lines_per_response"]

            # assert llm api key exists
            self._llm_api_key = self._config["llm_api_key"]
            if self._llm_api_key is None:
                err = ValueError("llm_api_key is required in config.json")
                logger.error(err)
                raise err

    def translate(self, episode):
        """
        translate an single episode with multiple connections

        :param episode:
        :type episode: SubtitleEpisode
        """
        total_trunk_count = math.ceil(len(episode) / self._lines_per_response)

        # multiple treading for network blocking
        with ThreadPoolExecutor(max_workers=self._max_responses) as executor:
            for trunk_index in range(total_trunk_count):
                # Bug better error handling, such as resubmitting
                executor.submit(self._translate_trunk, episode, trunk_index)

    _config = None
    _max_responses = None
    _lines_per_response = None
    _llm_api_key = None

    def _translate_trunk(self, episode, trunk_index):
        pass  # TODO
