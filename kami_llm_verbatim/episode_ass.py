"""
implement `AssSubtitleEpisode`
"""

import re

from kami_llm_verbatim import kamilog

from .episode import SubtitleEpisode

__all__ = ("AssSubtitleEpisode",)


logger = kamilog.getLogger()


class AssSubtitleEpisode(SubtitleEpisode):
    """
    implement SubtitleEpisode for `.ass` format
    """

    PATTERN = r"^(.+\[Events\]\n[^\n]+\n)(.+)$"
    LINE_PATTERN = r"^(Dialogue.+,,)(.+)$"

    def _populate(self):
        content = self._src_file.read()
        entire_match = re.match(self.PATTERN, content, re.DOTALL)

        if not entire_match:
            err = ValueError("invalid .ass syntax")
            logger.exception(err)
            raise err

        self._prefix = entire_match.group(1)
        lines = entire_match.group(2)

        # populate by lines
        for line_match in re.finditer(self.LINE_PATTERN, lines, re.MULTILINE):
            if not line_match:
                err = ValueError("invalid .ass line")
                logger.exception(err)
                raise err

            self._timestamps.append(line_match.group(1))
            self.lines.append(line_match.group(2))

    def _reconstruct(self):
        # write prefix
        self._dest_file.write(self._prefix)

        # write all lines
        last_line = len(self.lines) - 1
        for i, (time, line) in enumerate(
            zip(self._timestamps, self.translated_lines)
        ):
            self._dest_file.write(time)
            self._dest_file.write(line)
            if i != last_line:
                self._dest_file.write("\n")
