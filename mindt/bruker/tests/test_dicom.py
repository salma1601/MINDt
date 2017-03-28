import os
from nose.tools import assert_raises, assert_true, assert_equal
import dicom

from mindt.bruker import dicoms

from pkg_resources import Requirement, resource_filename
test_dir = resource_filename(Requirement.parse("pydicom"), "dicom/testfiles")
testcharset_dir = resource_filename(Requirement.parse("pydicom"),
                                    "dicom/testcharsetfiles")

dicom_filename = os.path.join(test_dir, "MR_small.dcm")


def test_load_dcm():
    dcm = dicoms.load_dcm(dicom_filename)
    assert_true(isinstance(dcm, dicom.dataset.FileDataset))
    assert_equal(dcm, dicoms.load_dcm(dcm))
    assert_raises(TypeError, dicoms.load_dcm, 1.)


def test_get_slice_thikness():
    # Check error is raised for inexistant fields
    assert_raises(ValueError, dicoms._get_slice_thickness, dicom_filename)
