"""DICOM utilities
"""
import os
import collections
import dicom
from dicom.datadict import tag_for_name
from nilearn._utils.compat import _basestring


def _repr_dcms(dcms):
    """ Pretty printing of dcm or dcms.
    """
    if isinstance(dcms, _basestring):
        return dcms
    if isinstance(dcms, collections.Iterable):
        return '[%s]' % ', '.join(_repr_dcms(dcm) for dcm in dcms)

    try:
        return "%s(\nkeys=%s\n)" % \
               (dcms.__class__.__name__,
                repr(dcms.dir()))
    except:
        pass
    return repr(dcms)


def short_repr(dcms):
    """Gives a shorten version on dcms representation
    """
    this_repr = _repr_dcms(dcms)
    if len(this_repr) > 20:
        # Shorten the repr to have a useful error message
        this_repr = this_repr[:18] + '...'
    return this_repr


def load_dcm(dcm):
    """Load a dcm and check if it is a dicom FileDataset

    Parameters:
    -----------
    dcm: dcm-like object
        Dicom to load.

    Returns:
    --------
    dcm: dicom.dataset.FileDataset
        A loaded DICOM object.
    """
    if isinstance(dcm, _basestring):
        # dcm is a filename, we load it
        dcm = dicom.read_file(dcm)
    elif not isinstance(dcm, dicom.dataset.FileDataset):
        raise TypeError("Data given cannot be loaded because it is"
                        " not compatible with dicom format:\n" +
                        short_repr(dcm))
    return dcm


def check_dcm(dcm):
    if isinstance(dcm, _basestring):
        if not os.path.exists(dcm):
            raise ValueError("File not found: '%s'" % dcm)

    # Otherwise, it should be a filename or a FileDataset, we load it
    dcm = load_dcm(dcm)
    return dcm


def _check_name(dcm, name):
    """ Checks for a given name

    Parameters
    ----------
    dcm: dcm object
        DICOM to parse.

    Returns
    -------
    name_exists : boolean
        Whether or not the name exists in the given dataset.
    """
    tag = tag_for_name(name)
    name_exists = True
    if tag is None:
        name_exists = False

    dcm = check_dcm(dcm)
    if tag not in dcm:
        name_exists = False

    return name_exists


def _get_slice_thickness(dcm):
    """Changes the values of the slice thickness and pixel spacing in a given
    dcm object

    Parameters
    ----------
    dcm : dcm-like object
        dcm object to modify.

    Returns
    -------
    thickness : float
        Slice thickness in the DICOM
    """
    plan = check_dcm(dcm)
    if not _check_name(plan, 'SharedFunctionalGroupsSequence'):
        raise ValueError('Inexistant Shared Functional Groups Sequence in ' +
                         short_repr(dcm))

    functional_data = plan.SharedFunctionalGroupsSequence[0]
    if not _check_name(functional_data, 'PixelMeasuresSequence'):
        raise ValueError('Inexistant Pixel Measures Sequence in ' +
                         short_repr(dcm))

    pixel_data = functional_data.PixelMeasuresSequence[0]
    if not _check_name(pixel_data, 'SliceThickness'):
        raise ValueError('Inexistant Slice Thickness in ' + short_repr(dcm))

    return float(pixel_data.SliceThickness)


def set_slice_thickness(dcm, slice_thickness, copy=True):
    """Changes the values of the slice thickness and pixel spacing in a given
    dcm object

    Parameters
    ----------
    dcm : dcm-like object
        dcm object to modify.

    slice_thickness: float
        The slice thickness to set.

    copy : booleen, optional
        If True, a shallow copy of the dataset is used.

    Returns
    -------
    plan : dicom.dataset.FileDataset
        The modified dataset.
    """
    plan = check_dcm(dcm)
    if copy:
        plan.copy()

    if not _check_name(plan, 'SharedFunctionalGroupsSequence'):
        raise ValueError('Inexistant "Shared Functional Groups Sequence" in ' +
                         short_repr(dcm))

    functional_data = plan.SharedFunctionalGroupsSequence[0]
    if not _check_name(functional_data, 'PixelMeasuresSequence'):
        raise ValueError('Inexistant "Pixel Measures Sequence" in ' +
                         short_repr(dcm))

    pixel_data = functional_data.PixelMeasuresSequence[0]
    if not _check_name(pixel_data, 'SliceThickness'):
        raise ValueError('Inexistant "Slice Thickness" in ' + short_repr(dcm))

    # Set thickness value
    pixel_data.SliceThickness = str(slice_thickness)
    return plan
