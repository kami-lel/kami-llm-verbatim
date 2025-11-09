"""
implement `SrtSubtitleEpisode`
"""

import re

from kami_llm_verbatim import kamilog

from .episode import SubtitleEpisode

__all__ = ("SrtSubtitleEpisode",)


logger = kamilog.getLogger()


class SrtSubtitleEpisode(SubtitleEpisode):
    """
    implement SubtitleEpisode for `.srt` format
    """

    LINE_PATTERN = r"^(\d+\n[\d:,]+ --> [\d:,]+)\n(.+)$"

    def _populate(self):
        content = self._src_file.read().split("\n\n")
        for line in content:
            match = re.match(self.LINE_PATTERN, line, re.DOTALL)

            if not match:
                err = ValueError("invalid .srt line: {}".format(repr(line)))
                logger.exception(err)
                raise err

            self._timestamps.append(match.group(1))
            self.lines.append(match.group(2))

    def _reconstruct(self):
        last_line = len(self.lines) - 1

        for i, (time, line) in enumerate(
            zip(self._timestamps, self.translated_lines)
        ):
            self._dest_file.write(time)
            self._dest_file.write("\n")
            self._dest_file.write(line)
            if i != last_line:
                self._dest_file.write("\n\n")
