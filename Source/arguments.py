from argparse import ArgumentParser, ArgumentTypeError
from datetime import datetime
from enums import OSEnum, DataGroupEnum
import argument_actions as arg_actions
import sys

class Arguments(object):
    """Uses ArgumentParser to gather and parse arguments given by the user in the command line.

    Attributes:
        argParser (ArgumentParser): An ArgumentParser instance used to gather and parse the given arguments
        dataset_name (str): The dataset name to use when adding the table to HDF5
        len_diff_threshold (int): A threshold value for the difference between a columns maximum string length 
           and average string length
        data_input_csvs (list): A list of the paths of the csvs given from the input directory
        HDF5_output_file (str): The path to the HDF5 output file
        data_group (DataGroupEnum): The enum that represents the different types of data groups
        os (OSEnum): The enum that represents the OS the data was generated from
        full_dataset_name (str): The full path the datasets will be created in which includes the data group, the dataset name, and the OS
        full_dataset_name_no_os (str): The same thing as full_dataset_name, but without the OS group
    """
    def __init__(self):
        # Update the current time
        self.currTime = datetime.now().strftime("%b-%d-%Y_%H-%M-%S")

        # Setup arguments to parse
        self.argParser = ArgumentParser(description='Imports particle data into an HDF5 file from a folder containing csv files.')

        # Optional Arguments
        self.argParser.add_argument(
        '--dataset-name',
        dest    = 'dataset_name',
        help    = 'The dataset name to use when adding the table to HDF5')
        self.argParser.add_argument(
            '--len-diff-threshold',
            dest    = 'len_diff_threshold',
            type    = int,
            default = sys.maxint,
            help    = 'String data columns can either be fixed length or variable length. This parameter '
                      'specifies a threshold value for the difference between a columns maximum string '
                      'length and average string length. When the threshold is exceeded the column is '
                      'set to variable length. The default behavior is for all string columns to be '
                      'fixed length.')

        # Positional Arguments
        self.argParser.add_argument(
            'data_input_dir',
            action = arg_actions.DatasetCsvsExistAction,
            help = 'The data input directory. It is expecting a directory containing three csv files named '
                   'timing, metrics, and metadata.')
        self.argParser.add_argument(
            'HDF5_output_file',
            help = 'The HDF5 output file. It will not be truncated if it already exists, but it will create '
                   'it if it does not exist.')
        self.argParser.add_argument(
            'data_group',
            choices = [ enum.name for enum in DataGroupEnum],
            help = 'The group that this dataset belongs to. This will influence the location of the dataset.')
        self.argParser.add_argument(
            'OS',
            choices = [ enum.name for enum in OSEnum],
            help = 'The OS this data was ran on. This will influence the location of the dataset.')

        # Parse all arguments
        args = vars(self.argParser.parse_args())
        self.dataset_name = args['dataset_name']
        self.len_diff_threshold = args['len_diff_threshold']
        self.data_input_csvs = args['data_input_dir']
        self.HDF5_output_file = args['HDF5_output_file']
        self.data_group = DataGroupEnum[args['data_group']]
        self.OS = OSEnum[args['OS']]

        # Use the input directory as the dataset name if a dataset name isn't provided
        self.dataset_name = self.data_input_dir if self.dataset_name is None else self.dataset_name

        # Create the full dataset name
        self.full_dataset_name = '{group}/{name}/{OS}'.format(group=self.data_group.value, name=self.dataset_name, OS=self.OS.value)
        self.full_dataset_name_no_os = '{group}/{name}'.format(group=self.data_group.value, name=self.dataset_name)