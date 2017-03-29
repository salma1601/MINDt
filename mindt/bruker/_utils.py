"""Bruker utilities
"""
import dicoms
import acquisition
import dicom
import os


def _add_prefix(prefix, in_file):
    """Adds a prefix to a filename
    Parameters
    ----------
    prefix : str
        Prefix to append to the filename
    in_file : str
        Input file name.
    Returns
    -------
    out_file : str
        Output file name
    """
    out_file = os.path.join(os.path.dirname(in_file),
                            prefix + os.path.basename(in_file))
    return out_file


def change_slice_thickness(in_dicom, acquisition_filename, out_dicom=None):
    """Returns the value of the specfied parameter as a string.

    Parameters:
    -----------
    in_dicom: str
        Path to the input dicom file.

    acquisition_filename: str
        Path to the acqp Bruker file.

    out_dicom: str, optional
        Path to the output dicom file.

    Returns:
    --------
    out_dicom: str
        Path to the output dicom file
    """
    if out_dicom is None:
        out_dicom = _add_prefix('fixed_', in_dicom)
    slice_seperation = acquisition.get_slice_sepn(acquisition_filename)
    slice_thickness = acquisition.get_slice_thick(acquisition_filename)
    if slice_seperation != slice_thickness:
        plan = dicoms.set_slice_thickness(in_dicom, slice_thickness)
        dicom.write_file(out_dicom, plan)
    else:
        out_dicom = in_dicom
        print('Nothing to change')

    return out_dicom
