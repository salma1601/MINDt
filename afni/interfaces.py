import os

import numpy as np
from nipype.interfaces import afni
from nipype.interfaces.base import BaseInterface, \
    BaseInterfaceInputSpec, traits, File, TraitedSpec, Directory
from nipype.utils.filemanip import split_filename
from nipype.interfaces.base import InputMultiPath, OutputMultiPath


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


class ControlTagRealignInputSpec(BaseInterfaceInputSpec):
    in_file = File(
        exists=True,
        mandatory=True,
        copyfile=True,
        desc='The filename of the input ASL 4D image.')
    paths = InputMultiPath(Directory(exists=True),
                           desc='Paths to add to matlabpath')
    register_to_mean = traits.Bool(
        False,
        usedefault=True,
        desc='Indicate whether realignment is done to the mean image')
    correct_tagging = traits.Bool(
        True,
        usedefault=True,
        desc='True/False correct for tagging artifact by zeroing the mean'
             ' difference between control and tag.')
    control_scans = traits.List(
        [],
        traits.Int(),
        desc='control frames numbers')
    tag_scans = traits.List(
        [],
        traits.Int(),
        desc='tag frames numbers')


class ControlTagRealignOutputSpec(TraitedSpec):
    realigned_files = File(exists=True,
                           desc='The resliced files')
    realignment_parameters = OutputMultiPath(
        File(exists=True),
        desc='Estimated translation and rotation parameters')


class ControlTagRealign(BaseInterface):
    """Realign ASL scans. Default parameters are those of the GIN
    pipeline.
    Notes
    -----
    This is a reimplementation of the realignement method from
    myrealign_pasl_2010.m of GIN toolbox.
    Examples
    --------
    from procasl import preprocessing
    realign = preprocessing.Realign()
    realign.inputs.in_file = 'functional.nii'
    realign.inputs.register_to_mean = False
    realign.inputs.correct_tagging = True
    out_realign = realign.run()
    print(out_realign.realigned files, out_realign.realignement_parameters)
    """
    input_spec = ControlTagRealignInputSpec
    output_spec = ControlTagRealignOutputSpec

    def _run_interface(self, runtime):
        # Set the realignement options
        realign = spm.Realign()
        realign.inputs.paths = self.inputs.paths
        realign.inputs.in_files = self.inputs.in_file
        realign.inputs.register_to_mean = self.inputs.register_to_mean
        realign.inputs.quality = 0.9
        realign.inputs.fwhm = 5.
        realign.inputs.separation = 4  # TODO: understand this parameter
        realign.inputs.interp = 2
        if self.inputs.correct_tagging:
            # Estimate the realignement parameters
            realign.inputs.jobtype = 'estimate'
            realign.run()
            parameters_file = realign.aggregate_outputs().get()[
                'realignment_parameters']
            rea_parameters = np.loadtxt(parameters_file)

            # Correct for tagging: equal means for control and tag scans
            n_scans = len(rea_parameters)
            if self.inputs.control_scans:
                control_scans = self.inputs.control_scans
            else:
                control_scans = range(0, n_scans, 2)

            if self.inputs.tag_scans:
                tag_scans = self.inputs.tag_scans
            else:
                tag_scans = range(1, n_scans, 2)

            gap = np.mean(rea_parameters[control_scans], axis=0) -\
                np.mean(rea_parameters[tag_scans], axis=0)
            rea_parameters[control_scans] -= gap / 2.
            rea_parameters[tag_scans] += gap / 2.

            # Save the corrected realignement parameters
            np.savetxt(parameters_file, rea_parameters, delimiter=' ')

            # Save the corrected transforms for each frame in spm compatible
            #  .mat. This .mat serves as header for spm in case of 4D files
            affine = spm_affine(self.inputs.in_file)
            rea_affines = np.zeros((4, 4, n_scans))
            for n_scan, param in enumerate(rea_parameters):
                rea_affines[..., n_scan] = params_to_affine(param).dot(affine)
            affines_file = os.path.splitext(self.inputs.in_file)[0] + '.mat'
            savemat(affines_file, dict(mat=rea_affines))
        else:
            realign.inputs.jobtype = 'estimate'
            realign.inputs.register_to_mean = self.inputs.register_to_mean
            realign.run()

        # Reslice and save the aligned volumes
        realign = spm.Realign()
        realign.inputs.paths = self.inputs.paths
        realign.inputs.in_files = self.inputs.in_file
        realign.inputs.jobtype = 'write'
        realign.run()
        return runtime

    def _list_outputs(self):
        outputs = self._outputs().get()
        fname = self.inputs.in_file
        _, base, _ = split_filename(fname)
        outputs["realignment_parameters"] = os.path.abspath(
            'rp_' + base + '.txt')
        outputs["realigned_files"] = os.path.abspath(
            'r' + base + '.nii')
        return outputs

