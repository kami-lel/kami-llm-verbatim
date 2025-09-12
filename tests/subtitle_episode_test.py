"""
tests for: SubtitleEpisode, SrtSubtitleEpisode
"""

from pathlib import Path
from tempfile import mkstemp

from kaye.subtitle_translator import SrtSubtitleEpisode, AssSubtitleEpisode

TESTEE_DIR = Path(__file__).parent / "testee"
TESTEE_SRT_SHORT = (TESTEE_DIR / "en_short.srt").resolve()
TESTEE_SRT_SHORT_SOLUTION = (TESTEE_DIR / "en_short.solution.srt").resolve()
TESTEE_ASS_SHORT = (TESTEE_DIR / "en_short.ass").resolve()
TESTEE_ASS_SHORT_SOLUTION = (TESTEE_DIR / "en_short.solution.ass").resolve()


class TestSrt:

    def test_parse(_):
        _, dest_file_path = mkstemp()

        # perform translation of case swapping
        with SrtSubtitleEpisode(TESTEE_SRT_SHORT, dest_file_path) as episode:
            for i, line in enumerate(episode.lines):
                episode.translated_lines[i] = line.swapcase()

        # check against solution
        with open(dest_file_path) as dest_file:
            answer = dest_file.read()
            print(answer)

            with open(TESTEE_SRT_SHORT_SOLUTION) as solution_file:
                solution = solution_file.read()

                assert answer == solution


class TestAss:

    def test_parse(_):
        _, dest_file_path = mkstemp()

        # perform translation of case swapping
        with AssSubtitleEpisode(TESTEE_ASS_SHORT, dest_file_path) as episode:
            for i, line in enumerate(episode.lines):
                episode.translated_lines[i] = line.swapcase()

        # check against solution
        with open(dest_file_path) as dest_file:
            answer = dest_file.read()
            print(answer)

            with open(TESTEE_ASS_SHORT_SOLUTION) as solution_file:
                solution = solution_file.read()

                assert answer == solution
