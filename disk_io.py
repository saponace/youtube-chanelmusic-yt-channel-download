import os

import re
import shutil
import logging

# TODO: Should I use this exception or not ?
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
        self.logger = logging.getLogger(__name__)
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
        self.logger.debug('Filename {0} matches regexes of '
                          'directorie(s) {1}'.format(filename, matching_dirs))
        return matching_dirs

    def ensure_dir(self, dir_path):
        """
        Recursively create a directory if it does not exist
        :param dir_path: The directory
        """
        self.logger.debug('Checking existence of directory {0} ...'.
                          format(dir_path))
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            self.logger.debug('Directory {0} did not exist and has been '
                              'created !'.format(dir_path))
        else:
            self.logger.debug('Directory {0} exists'.format(dir_path))

    def get_dir_to_store_track(self, filename):
        """
        Get the path of the directory to store the given file according to its
        name
        :param filename: The path of the file
        :return: The path to the directory to move the file
        """
        matching_dirs = self.get_matching_dirs(filename)
        if len(matching_dirs) == 0:
            self.logger.warn('Filename {0} does not match any regex in the '
                             'config file, moving it to the project base '
                             'directory'.format(filename))
            # Matches the project base directory
            # FIXME: Works, but very ugly
            return self.config['download_locations']['$^']
        elif len(matching_dirs) == 1:
            ret_val = matching_dirs[0]
            # No logging here because it would be redundant with log in method
            # get_matching_dirs
            return ret_val
        elif len(matching_dirs) > 1:
            chosen_dir = matching_dirs[0]
            self.logger.warn('Filename {0} matches several regexes of the '
                             'directories {1}. Moving the file to {2}'.
                             format(filename, matching_dirs, chosen_dir))
            return chosen_dir

    def move_file(self, filepath):
        """
        Move a given file to a directory which regex matches the filename
        :param filepath: The path of the file to move
        """
        filename = os.path.basename(filepath)  # TODO: Catch exception here (ex: file does not exist or unreadable)
        destination = self.get_dir_to_store_track(filename)
        self.ensure_dir(destination)
        self.logger.debug('Moving {0} to {1} ...'.format(filepath, destination))
        shutil.move(filepath, destination)  # TODO: Catch exception here (ex: destination file already exists)
        self.logger.debug('{0} successfully moved to {1}'.
                          format(filepath, destination))
