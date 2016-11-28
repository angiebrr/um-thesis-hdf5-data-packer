from argparse import ArgumentParser, ArgumentTypeError, Action
from datetime import datetime
import sys, os

class NotADirError(Exception):
    """ Raised when the argument is not a directory.
    """
    pass

class DirExistsAction(Action):
    '''A custom action that ensures that the input directory exists.

    This verifies: 
    - The argument to be a directory. If not, raise a NotADirError exception.
    '''

    def verify_is_dir(self, dir_name):
        # Verify that the argument is a directory
        if not os.path.isdir(dir_name):
            message = '[ERROR]: {dir} is not a directory.'.format(dir=dir_name)
            raise NotADirError(message)

        return dir_name

    def __call__(self, parser, namespace, values, option_string=None):
        # Verify that it is a dir
        dir_name = self.verify_is_dir(values)

        # Add the attribute
        setattr(namespace, self.dest, dir_name)

class Arguments(object):
    """Uses ArgumentParser to gather and parse arguments given by the user in the command line.

    Attributes:
        argParser (ArgumentParser): An ArgumentParser instance used to gather and parse the given arguments
        data_input_dir (str): The data input directory.
        hdf5_file (str): The path to the hdf5 file.
        dataset_group (str): The group that the datasets belong to.
        os (str): The OS the data was ran on.
    """
    def __init__(self):
        # Update the current time
        self.currTime = datetime.now().strftime("%b-%d-%Y_%H-%M-%S")

        # Setup arguments to parse
        self.argParser = ArgumentParser(description='Uses the hdf5 packer to process a directory of results.')

        # Positional Arguments
        self.argParser.add_argument(
            'data_input_dir',
            action = DirExistsAction,
            help = 'The data input directory. It is expecting to be a directory of directories holding CSVs')
        self.argParser.add_argument(
            'hdf5_file',
            help = 'The path to the HDF5 file.')
        self.argParser.add_argument(
            'dataset_group',
            help = 'The group that the datasets belong to.')
        self.argParser.add_argument(
            'os',
            help = 'The OS the data was ran on.')


        # Parse all arguments
        args = vars(self.argParser.parse_args())
        self.data_input_dir = args['data_input_dir']
        self.hdf5_file = args['hdf5_file']
        self.dataset_group = args['dataset_group']
        self.os = args['os']