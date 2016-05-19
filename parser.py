import json
import logging
from duplicate_regex_error import DuplicateRegexError


class Parser(object):
    """
    Parse a config file
    """

    def __init__(self, config_file_path):
        """
        Constructor
        :param config_file_path: The path to the config file
        """
        self.logger = logging.getLogger(__name__)
        self.config_file_path = config_file_path

    def parse_directories_aux(self, node, parent_dir):
        """
        Recursively parse a tree of download locations
        :param node: Node of the tree
        :param parent_dir: Current directory of the node
        :return: A dictionary where:
            Keys: Regex pattern
            Values: Path of the directory to store tracks that match the regex
        """
        download_locations = {}
        current_dir = parent_dir + "/" + node['name']
        pattern = node['pattern']
        download_locations[pattern] = current_dir
        self.logger.debug('Directory {0} added to download locations with '
                          'regex "{1}"'.format(current_dir, pattern))

        if 'children' in node:
            for child_node in node['children']:
                subcall_ret_val = self.\
                    parse_directories_aux(child_node, current_dir)
                for pat in subcall_ret_val:
                    if pat in download_locations:
                        # TODO: Catch error, log a critical and exit
                        raise DuplicateRegexError("Duplicate regex - '" +
                                                  pat + "' matches paths " +
                                                  download_locations[pat] +
                                                  " and " + subcall_ret_val[pat])
                download_locations.update(subcall_ret_val)
        return download_locations

    def parse_directories(self, subdirs_list, basedir, project_name):
        """
        Return a dictionary containing the directories that will hold the
        tracks
        :param subdirs_list: The list of directories to store tracks.
        :param basedir: The base directory in which the file tree structure
        :param project_name: The name of the project. Will be used as root
        directory
        :return: A dictionary where:
            Keys: Regex patterns
            Values: The relative location of the directory from the
            base_location
        """
        head = dict(name=project_name,
                    pattern="$^",  # Regex that matches nothing. Used to
                                   # recognize the project base directory
                    children=subdirs_list)
        self.logger.debug('Starting parsing of the download locations')
        return self.parse_directories_aux(head, basedir)

    def parse(self):
        """
        Parse the config file
        :return: Dictionary containing the data that will be outputed where:
            project_name -> Name of the project
            upstream_URLs -> List of upstream URL from which to download the
            tracks
            download_locations -> List of directories to store downloaded tracks
        """
        ret_val = {}

        self.logger.debug('Parsing config file {0} ...'.
                          format(self.config_file_path))
        with open(self.config_file_path) as config_file:
            config = json.load(config_file)

        project_name = ret_val['project_name'] = config['projectName']
        self.logger.debug('Successfully parsed project name {0}'.
                          format(project_name))
        upstream_urls = ret_val['upstream_urls'] = config['upstreamURLs']
        self.logger.debug('Successfully parsed upstream URLs {0}'.
                          format(upstream_urls))

        ret_val['download_locations'] = self.parse_directories(
            config['directories'],
            config['baseLocation'],
            project_name)
        self.logger.debug('Successfully parsed download locations')

        return ret_val
