from enums import ColTypeEnum
import sys
import numpy
import h5py
import csv

class CsvToHDF5():
    """A class that is used to add datasets and metadata to a hdf5 file from csv files.

    Although modified by me for my needs, most of the code was written by keithshep. You can find the 
    Github Gist here: https://gist.github.com/keithshep/61a2ea1f12d017ab13cd

    Attributes:
        csv_file_name (str): The path to the CSV file that will be imported
        hdf5_file (File): The HDF5 File object
        dataset_name (str): The dataset name to use when adding the table to HDF5. This could also be a 
            group name, depending on the context.
        len_diff_threshold (int): This specifies a threshold value for the difference between a columns 
            maximum string length and average string length
    """
    def __init__(self, hdf5_file, len_diff_threshold = sys.maxint):
       self.csv_file_name = None
       self.hdf5_file = hdf5_file
       self.dataset_name = None
       self.len_diff_threshold = len_diff_threshold

    def add_dataset_from_csv(self, csv_file_name, dataset_name):
        """Adds a new dataset from a csv to the current hdf5 file

        Params:
            csv_file_name (str): The path to the CSV file that will be imported
            dataset_name (str): The dataset name to use when adding the table to HDF5
        """
        # update vars
        self.csv_file_name = csv_file_name
        self.dataset_name = csv_file_name if dataset_name is None else dataset_name

        # add the dataset from csv to the hdf5 file
        self.__csv_to_hdf5()

    def add_metadata_from_csv(self, csv_file_name, dataset_name):
        """Adds metadata to a dataset from a csv to the current hdf5 file

        Params:
            csv_file_name (str): The path to the CSV file that will be imported
            dataset_name (str): The name of the dataset we will add metadata to
        """
        # update vars
        self.csv_file_name = csv_file_name
        self.dataset_name = csv_file_name if dataset_name is None else dataset_name

        # add the metadata to the hdf5 dataset
        self.__csv_to_hdf5_attrs()

    def __csv_to_hdf5_attrs(self):
        """Converts a CSV file into an HDF5 dataset's metadata
        """
        # We first want to assert that there is only two columns and they are like "attribute,value"
        csv_file = open(self.csv_file_name, 'rb')
        snp_anno_reader = csv.reader(csv_file)
        header = snp_anno_reader.next()
        col_count = len(header)
        assert col_count == 2
        assert header[0] == 'attribute'
        assert header[1] == 'value'

        # We then want to grab the dataset and add an attribute for every row
        print self.hdf5_file
        if self.dataset_name in self.hdf5_file:
            current_dset = self.hdf5_file[self.dataset_name]
            for row in snp_anno_reader:
                attribute, value = row[0], row[1]
                val_type = self.__infer_col_type(value)
                val_dtype = self.__to_numpy_dtype(val_type)
                native_val = self.__str_to_native(value, val_type)
                current_dset.attrs.create(attribute, native_val, dtype=val_dtype) 

        csv_file.close()

    def __csv_to_hdf5(self):
        """Converts a CSV file into an HDF5 dataset
        """
        if self.dataset_name not in self.hdf5_file:
            # the first pass through the CSV file is to infer column types
            csv_file = open(self.csv_file_name, 'rb')
            snp_anno_reader = csv.reader(csv_file)
            header = snp_anno_reader.next()
            col_count = len(header)
            max_str_lens = [0 for x in range(0, col_count)]
            avg_str_lens = [0 for x in range(0, col_count)]
            col_types = [ColTypeEnum.UNKNOWN for x in range(0, col_count)]
            row_count = 0
    
            for row in snp_anno_reader:
                assert len(row) == col_count
                curr_str_lens = map(len, row)
                max_str_lens = map(max, zip(max_str_lens, curr_str_lens))
                avg_str_lens = map(sum, zip(avg_str_lens, curr_str_lens))
                col_types = map(self.__most_specific_common_type, zip(map(self.__infer_col_type, row), col_types))
                row_count += 1
    
            csv_file.close()
            avg_str_lens = [float(x) / row_count for x in avg_str_lens]

            table_type = numpy.dtype(
                [self.__to_numpy_type_tuple(header[i], col_types[i], max_str_lens[i], avg_str_lens[i])
                    for i in range(0, col_count)])

            # the second pass through is to fill in the HDF5 structure
            hdf5_table = self.hdf5_file.create_dataset(self.dataset_name, (row_count,), dtype = table_type)
            csv_file = open(self.csv_file_name, 'rb')
            snp_anno_reader = csv.reader(csv_file)
            header = snp_anno_reader.next()
    
            for row_index in range(0, row_count):
                row = snp_anno_reader.next()
                row_val = [self.__str_to_native(row[i], col_types[i]) for i in range(0, col_count)]
                hdf5_table[row_index] = tuple(row_val)
    
            csv_file.close()

    def __infer_col_type(self, str_val):
        """Tries to guess a type from the string value

        Params:
            str_val (str): The string value we want to infer the type of

        Returns:
            ColTypeEnum: The inferred type from the string value
        """
        str_val = str_val.strip()
        try:
            int(str_val)
            return ColTypeEnum.INT
        except ValueError:
            try:
                float(str_val)
                return ColTypeEnum.FLOAT
            except ValueError:
                return ColTypeEnum.STRING

    def __most_specific_common_type(self, col_types):
        """From a list of column types, find the type that can be used to hold any values in the list.

        Params:
            col_types (list): List of inferred column types.

        Returns:
            ColTypeEnum: The most specific type that can hold any values in the list.
        """
        if ColTypeEnum.STRING in col_types:
            return ColTypeEnum.STRING
        elif ColTypeEnum.FLOAT in col_types:
            return ColTypeEnum.FLOAT
        elif ColTypeEnum.INT in col_types:
            return ColTypeEnum.INT
        else:
            return ColTypeEnum.UNKNOWN

    def __str_to_native(self, str_val, col_type):
        """Convert the given string value to the python native type

        Params:
            str_val (str): The string value we want to convert
            col_type (ColTypeEnum): The type we want to convert to

        Returns:
            variable: The converted value. Could be a str, int, or float.
        """
        if col_type == ColTypeEnum.STRING:
            return str_val
        elif col_type == ColTypeEnum.FLOAT:
            return float(str_val)
        elif col_type == ColTypeEnum.INT:
            return int(str_val)
        else:
            raise ValueError

    def __to_numpy_type_tuple(self, col_name, col_type, max_str_len, avg_str_len):
        """Return the corresponding numpy type for the given column type info

        Params:
            col_name (str): The name of the csv column
            col_type (ColTypeEnum): The type we want to convert to
            max_str_len (int): The maximum string length
            avg_str_len (int): The average string length

        Returns:
            tuple: The column name and the numpy type.
        """
        if col_type == ColTypeEnum.STRING:
            if max_str_len - avg_str_len > self.len_diff_threshold:
                return (col_name, h5py.special_dtype(vlen=str))
            else:
                return (col_name, numpy.str_, max_str_len)
        elif col_type == ColTypeEnum.FLOAT:
            return (col_name, 'f')
        elif col_type == ColTypeEnum.INT:
            return (col_name, 'i')
        else:
            raise ValueError

    def __to_numpy_dtype(self, col_type):
        """Returns a numpy.dtype from the ColType enum given.

        Params:
            col_type (ColTypeEnum): The type we want to convert to.

        Returns:
            numpy.dtype: The numpy data type inferred by the given ColType enum.
        """
        if col_type == ColTypeEnum.STRING:
            numpy.dtype(str)
        elif col_type == ColTypeEnum.FLOAT:
            numpy.dtype('f')
        elif col_type == ColTypeEnum.INT:
            numpy.dtype('i')
        else:
            raise ValueError