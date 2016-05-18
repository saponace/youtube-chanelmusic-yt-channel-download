import os

import re
import shutil
from warnings import warn

from file_matches_no_regex_error import FileMatchesNoRegexError


class DiskIO(object):
    """
    Handle the disk IO
    """

    def __init__(self, config):
        """
        Constructor
        :param config: The config dictionary outputed by Parser.parse()
        """
        super(DiskIO, self).__init__()
        self.config = config

    @staticmethod
    def ensure_dir(dir_path):
        """
        Recursively create a directory if it does not exist
        :param dir_path: The directory
        """
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def get_dir_to_store_track(self, filename):
        """
        Get the path of the directory to store the given file according to its
        name
        :param filename: The path of the file
        :return: The path to the directory to move the file
        """
        matching_dirs = []
        for regex, path in self.config['download_locations'].items():
            p = re.compile(regex)
            if p.search(filename):
                matching_dirs.append(path)
        if len(matching_dirs) == 0:
            raise FileMatchesNoRegexError("Filename " + filename + " does not match " +
                                          "any regex in the config file.")
        elif len(matching_dirs) == 1:
            return matching_dirs[0]
        elif len(matching_dirs) > 1:
            first_dir = matching_dirs[0]
            warning_string = "Filename " + filename + " matches several regexs ("
            append_string = ""
            for current_dir in matching_dirs:
                append_string += "\"" + current_dir + "\", "
            warning_string += "). Storing the track in " + first_dir + "."
            warn(warning_string)
            return first_dir

    def move_file(self, filepath):
        filename = os.path.basename(filepath)
        destination = self.get_dir_to_store_track(filename)
        DiskIO.ensure_dir(destination)
        shutil.move(filepath, destination)
