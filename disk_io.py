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

    def get_matching_dirs(self, filename):
        """
        Get the list of the directories that are eligible to store the file
        :param self:
        :param filename: The filename to look for matches
        :return: A list of strings rpresenting the eligibles directories
        """
        matching_dirs = []
        for regex, path in self.config['download_locations'].items():
            p = re.compile(regex)
            if p.search(filename):
                matching_dirs.append(path)
        return matching_dirs

    @staticmethod
    def ensure_dir(dir_path):
        """
        Recursively create a directory if it does not exist
        :param dir_path: The directory
        """
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    @staticmethod
    def several_matching_dirs_warning(filename,
                                      matching_dirs_list, chosen_dir):
        """
        Send a warning when severql directories's regex match the filename
        :param filename: The filename
        :param matching_dirs_list: The list of directories that match
        :param chosen_dir: The directory amongst the list that has been chosen
        to store the file
        """
        warning_string = "Filename " + filename + " matches several regexs ("
        append_string = ""
        for current_dir in matching_dirs_list:
            append_string += "\"" + current_dir + "\", "
        warning_string += append_string + "). Storing the track in " + \
                          chosen_dir + "."
        warn(warning_string)

    def get_dir_to_store_track(self, filename):
        """
        Get the path of the directory to store the given file according to its
        name
        :param filename: The path of the file
        :return: The path to the directory to move the file
        """
        matching_dirs = self.get_matching_dirs(filename)
        if len(matching_dirs) == 0:
            raise warn("Filename " + filename + " does not match any regex in"
                                                " the config file, moving it to"
                                                " the project base directory")
            return self.config['download_locations']['$^']  # Matches the
            # project base
            # directory
        elif len(matching_dirs) == 1:
            return matching_dirs[0]
        elif len(matching_dirs) > 1:
            chosen_dir = matching_dirs[0]
            DiskIO.several_matching_dirs_warning(filename, matching_dirs,
                                                 chosen_dir)
            return chosen_dir

    def move_file(self, filepath):
        """
        Move a given file to a directory which regex matches the filename
        :param filepath: The path of the file to move
        """
        filename = os.path.basename(filepath)
        destination = self.get_dir_to_store_track(filename)
        DiskIO.ensure_dir(destination)
        shutil.move(filepath, destination)
