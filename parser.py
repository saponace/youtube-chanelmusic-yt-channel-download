import json
from duplicate_regex_error import DuplicateRegexError


class Parser(object):

    def __init__(self, config_file_path):
        self.config_file_path = config_file_path

    def parse_directories_aux(self, node, parent_dir):
        """
        Recursively parse a tree of download locations

        Parameters:
            current_dir --- Current directory of the node
            node --- Node of the tree

        Return value: Dictionary where
            Keys: Regex pattern
            Values: Path of the directory to store tracks that match the regex
        """
        download_locations = {}
        current_dir = parent_dir + "/" + node['name']
        pattern = node['pattern']
        download_locations[pattern] = current_dir

        if 'children' in node:
            for child_node in node['children']:
                subcall_ret_val = self.parse_directories_aux(child_node,
                                                             current_dir)
                for pat in subcall_ret_val:
                    if (pat in download_locations):
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

        Parameters:
            subdirs_list -- The list of directories to store tracks.
            basedir -- The base directory in which the file tree structure
            should be created.
            project_name -- The name of the project. Will be used as root
            directory

        Return value: Dictionary where
            Keys: Regex patterns
            Values: The relative location of the directory from the
            base_location
        """
        head = {}
        head['name'] = project_name
        head['pattern'] = "*"
        head['children'] = subdirs_list
        return self.parse_directories_aux(head, basedir)

    def parse(self):
        """
        Parse a config file

        Return value: Dictionary containing the data that will be outputed
            Key project_name: Name of the project
            Key upstream_URLs: List of upstream URL from which to download the
            tracks
            Key locations: List of directories to store downloaded tracks
        """
        ret_val = {}

        with open(self.config_file_path) as config_file:
            config = json.load(config_file)

        project_name = config['projectName']
        ret_val['project_name'] = project_name

        upstream_urls = config['upstreamURLs']
        ret_val['upstream_urls'] = upstream_urls

        base_location = config['baseLocation']
        ret_val['download_locations'] = self.parse_directories(
            config['directories'], base_location, project_name)

        return ret_val
