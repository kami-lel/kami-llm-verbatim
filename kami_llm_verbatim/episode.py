"""
implement SubtitleEpisode and its concrete children classes
"""

__all__ = ("SubtitleEpisode",)


class SubtitleEpisode:
    """
    abstract representation of an episode of subtitle,
    allow one to extract and reconstruct a a subtitle file with correct format
    without worrying about differences in subtitle file format


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
        # perform actual translation
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
        self._prefix = ""
        self._suffix = ""

        # init public variables
        self.lines = []
        self.translated_lines = []

        self._populate()
        self._len = len(self.lines)

        # pre-allocation to allow multi-treads operations
        self.translated_lines = [None] * len(self)

    def _populate(self):
        """
        extract and parse content from original subtitle file

        reading from original subtitle file `._src_file`, and extract content;
        populate `.lines` with subtitle lines,
        and populate `.timestamps` with respective timestamp content
        (both `.lines` and `timestamps` are `list`s of `str`)

        may write to `._prefix` and `._suffix`, both
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
        self._reconstruct()

        # properly close opened files
        self._src_file.close()
        self._dest_file.close()

        return True

    def __len__(self):
        """
        :return: number of lines in this episode
        :rtype: int
        """
        return self._len
