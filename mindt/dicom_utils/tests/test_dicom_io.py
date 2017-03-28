import os
from nose.tools import assert_raises
from mindt.dicom_utils import dicom_io
from pkg_resources import Requirement, resource_filename
test_dir = resource_filename(Requirement.parse("pydicom"), "dicom/testfiles")
testcharset_dir = resource_filename(Requirement.parse("pydicom"),
                                    "dicom/testcharsetfiles")

dicom_filename = os.path.join(test_dir, "MR_small.dcm")


def test_get_slice_thikness():
    # Check error is raised for inexistant fields
    assert_raises(ValueError, dicom_io._get_slice_thickness, dicom_filename)
