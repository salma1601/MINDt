import os
from nose.tools import assert_equal
from mindt.dicom_utils import dicom_io
from pkg_resources import Requirement, resource_filename
test_dir = resource_filename(Requirement.parse("pydicom"), "dicom/testfiles")
testcharset_dir = resource_filename(Requirement.parse("pydicom"),
                                    "dicom/testcharsetfiles")

dicom_filename = os.path.join(test_dir, "MR_small.dcm")


def test_set_slice_thikness():
    thickness = .11
    dcm = dicom_io.set_slice_thickness(dicom_filename, thickness, copy=True)

    assert_equal(thickness, dicom_io._get_slice_thickness(dcm))
