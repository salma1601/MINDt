"""Bruker acqusition parameters utilities
"""
import re


def _get_acquisition_parameter(acquisition_filename, parameter_pattern):
    """Returns the value of the specfied parameter as a string.

    Parameters:
    -----------
    acquisition_filename: str
        Path to the acqp Bruker file.

    parameter_pattern: str
        Pattern for the name of the parameter.

    Returns:
    --------
    value: str
        Value of the parameter.
    """
    acquisition_data = open(acquisition_filename, 'r')
    acquisition_str = acquisition_data.read()
    matches = re.findall(parameter_pattern, acquisition_str)
    # Allow only a unique match
    if not matches:
        raise ValueError('no match for pattern {0} in file {1}'.format(
            acquisition_filename, parameter_pattern))
    elif len(matches) > 1:
        raise ValueError('multiple matches for pattern {0} in file {1}'.format(
            acquisition_filename, parameter_pattern))

    acquisition_data = open(acquisition_filename, 'r')
    acquisition_lines = acquisition_data.readlines()
    acquisition_data.close()
    for line_number, line in enumerate(acquisition_lines):
        match = re.findall(parameter_pattern, line)
        if match:
            return acquisition_lines[line_number + 1]


def get_slice_sepn(acquisition_filename):
    return float(_get_acquisition_parameter(acquisition_filename,
                                            'ACQ_slice_sepn=\( 1 \)'))


def get_slice_thick(acquisition_filename):
    return float(_get_acquisition_parameter(acquisition_filename,
                                            'ACQ_slice_thick='))
