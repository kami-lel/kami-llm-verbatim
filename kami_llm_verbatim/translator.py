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

    config = None
    max_response = None
    lines_per_response = None
    llm_api_key = None

    def __init__(self):
        # load various configs if never loaded into class
        if self.config is None:
            # ensure config.json exists
            if not CONFIG_FILE_PATH.exists():
                CONFIG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(DEFAULT_CONFIG_FILE_PATH, CONFIG_FILE_PATH)

            with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as f:
                self.config = json5_load(f)

            logger.debug("load config.json:\n%s", self.config)

            # read configs  ----------------------------------------------------
            self.max_responses = self.config["max_responses"]
            self.lines_per_response = self.config["lines_per_response"]

            # assert llm api key exists
            self.llm_api_key = self.config["llm_api_key"]
            if self.llm_api_key is None:
                err = ValueError("llm_api_key is required in config.json")
                logger.error(err)
                raise err

    def translate(self, episode):
        """
        translate an single episode with multiple connections

        :param episode:
        :type episode: SubtitleEpisode
        """
        total_trunk_count = math.ceil(len(episode) / self.lines_per_response)

        # multiple treading for network blocking
        with ThreadPoolExecutor(max_workers=self.max_responses) as executor:
            for trunk_index in range(total_trunk_count):
                # Bug better error handling, such as resubmitting
                executor.submit(self._translate_trunk, episode, trunk_index)

    def _translate_trunk(self, episode, trunk_index):
        pass  # TODO
