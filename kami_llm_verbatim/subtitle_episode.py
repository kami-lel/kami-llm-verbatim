# todo docstring
import re

__all__ = ("SubtitleEpisode", "SrtSubtitleEpisode", "AssSubtitleEpisode")


class SubtitleEpisode:
    """
    abstract representation of an episode of subtitle


    :param src_file_path: original untranslated subtitle file
    :type src_file_path: str
    :param dest_file_path: file to write the translated file
    :type dest_file_path: str
    :param src_file_encoding: default to 'utf-8'
    :type src_file_encoding: str
    :param dest_file_encoding: default to 'utf-8'
    :type src_file_encoding: str
    :example: ...

    with SrtSubtitleEpisode(src_file, dest_file) as episode:
        for i, line in enumerate(episode.lines):
            translated = actual_translating_function(line)
            episode.translated_lines[i] = translated
    """

    def __init__(
        self,
        src_file_path,
        dest_file_path,
        src_file_encoding="utf-8",
        dest_file_encoding="utf-8",
    ):
        # open files ready for r/w
        self._src_file = open(src_file_path, "r", encoding=src_file_encoding)
        self._dest_file = open(
            dest_file_path, "w", encoding=dest_file_encoding
        )

        self._timestamps = []
        self._prefix = None
        self._suffix = None

        # init public variables
        self.lines = []
        self.translated_lines = []

        self._populate()

        self.translated_lines = [None] * len(self.lines)

    def _populate(self):
        """
        reading from `._src_file` and populate `.timestamps` and `.lines`,
        also may write to `._prefix` and `._suffix`
        """
        raise NotImplementedError

    def _reconstruct(self):
        """
        taken `.timestamps` and `.translated_lines`
        (may also read from `._prefix` and `._suffix`,)
        and write into `._dest_file` with proper structure
        """
        raise NotImplementedError

    # set up context handler  --------------------------------------------------
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:  # FIXME better handle error
            return False

        self._reconstruct()

        # properly close opened files
        self._src_file.close()
        self._dest_file.close()

        return True


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
                pass  # HACK

            self._timestamps.append(match.group(1))
            self.lines.append(match.group(2))

    def _reconstruct(self):
        for time, line in zip(self._timestamps, self.translated_lines):
            line = "{}\n{}\n\n".format(time, line)
            self._dest_file.write(line)


class AssSubtitleEpisode(SubtitleEpisode):
    """
    implement SubtitleEpisode for `.ass` format
    """

    def _populate(self):
        raise NotImplementedError  # TODO

    def _reconstruct(self):
        raise NotImplementedError  # TODO


# todo additional subtitle formats
