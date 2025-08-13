from scripts.utils import get_bvals
from glob import glob
import os
import subprocess as sp


def get_b0_indices(filename):
    bvals = get_bvals(filename)
    return [i for i, x in enumerate(bvals) if float(x) == 0.0]


def get_b0_inputs(sub, ses, dir):
    indices = get_b0_indices(
        f"sub-{sub}/ses-{ses}/dwi/sub-{sub}_ses-{ses}_dir-{dir}_dwi.bval"
    )
    return [
        f"derivatives/dti_smk/sub-{sub}/ses-{ses}/b0/{dir}_{frame:04d}.nii.gz"
        for frame in indices
    ]


def all_outputs(skip_bedpostx=False):
    inputs = glob("sub-*/ses-*/dwi/*_dir-AP_dwi.nii.gz")
    outprefix = ["derivatives/dti_smk/" + "/".join(x.split("/")[:2]) for x in inputs]
    outfiles = [
        "eddy/ec_data.qc/qc.json",
        "dtifit/fit_tensor.nii.gz",
    ]
    if not skip_bedpostx:
        outfiles.append("bedpostx.bedpostX/nodif_brain_mask.nii.gz")
    return [f"{p}/{f}" for p in outprefix for f in outfiles]


def has_usable_gpu() -> bool:
    """Determine whether a gpu is available, that is usable for eddy and bedpostx
    The code for testing is adopted from $FSLDIR/bin/eddy (fsl version 6.0.7.18)

    Returns
    -------
    bool
        True if a usable GPU is found
    """
    fsldir = os.environ["FSLDIR"]
    find_cuda = os.path.join(fsldir, "bin", "find_cuda_exe")
    eddy_cuda = sp.check_output((find_cuda, "eddy_cuda"), text=True).strip()

    return eddy_cuda != ""
