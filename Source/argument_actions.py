import argparse
import re
import os

class DatasetCsvsDoNotExistError(Exception):
    """ Raised when the argument directory does not contain the needed csvs.
    """
    pass

class NotADirError(Exception):
    """ Raised when the argument is not a directory.
    """
    pass

class DatasetCsvsExistAction(argparse.Action):
    '''A custom action that ensures that the input directory has the necessary csv files and saves the list of csvs as the attribute.

    This verifies: 
    - The argument to be a directory. If not, raise a NotADirError exception.
    - The argument directory contains the timing, metrics, and metadata csv files. If not, raise a DatasetCsvsDoNotExistError exception.
    '''

    def verify_dataset_csvs_existence(self, dir_name):
        # Verify that the argument is a directory
        if not os.path.isdir(dir_name):
            message = '[ERROR]: {dir} is not a directory.'.format(dir=dir_name)
            raise NotADirError(message)

        # Get the csv files that are named exactly 'timing.csv', 'metrics.csv', or 'metadata.csv' 
        csv_file_matches = [ '{dir}/{file}'.format(dir=dir_name, file=file_data) for file_data in os.listdir(dir_name) if re.search(r'^(timing|metrics|metadata)\.csv$', file_data)]

        if len(csv_file_matches) != 3:
            message = '[ERROR]: {dir} does not contain exactly 3 csv files called timing.csv, metrics.csv, and metadata.csv.'.format(dir=dir_name)
            raise DatasetCsvsDoNotExistError(message)

        return csv_file_matches

    def __call__(self, parser, namespace, values, option_string=None):
        # Verify that the csvs exist
        csv_files = self.verify_dataset_csvs_existence(values)

        # Add the attribute
        setattr(namespace, self.dest, csv_files)