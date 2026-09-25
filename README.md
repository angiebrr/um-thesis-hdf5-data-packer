# Thesis HDF5 data packer

> [!WARNING]
> Archived and no longer maintained; kept for reference. Written in 2016 for Python 2.7 (it uses `sys.maxint`), and the helper script has a hardcoded Windows path.

## Overview

A small Python tool I wrote for my master's thesis at the University of Montana. My [automated Pong benchmark](https://github.com/angiebrr/um-thesis-cspong-benchmarking) wrote each run's results as a folder of CSVs, and with runs across Windows, iOS, and Android for every experiment, that got hard to keep track of. This packs those folders into one HDF5 file, so the whole study's data lives in a single, self-describing dataset.

For each run folder, it:

- infers each CSV column's type (int, float, or string) and stores the table as an HDF5 dataset
- turns the run's metadata CSV into HDF5 attributes on that dataset
- files it under a group for the experiment (`/no_changes/looping`, `/optimization_case_studies/lock_free`, …) and the OS it ran on

`Helpers/procdir` runs the packer over every run folder in a directory.

The resulting dataset is attached to the [thesis repo](https://github.com/angiebrr/um-thesis-particle-optimization)'s release.

**Tech:** Python 2.7, h5py, NumPy

## Using it

```bash
pip install h5py numpy enum34
python Source/__main__.py <data_input_dir> <HDF5_output_file> <data_group> <OS>
```

`data_group` is one of the experiment groups in `Source/enums.py`, and `OS` is `WINDOWS`, `IOS`, or `ANDROID`. Run with `-h` for the rest of the options.
