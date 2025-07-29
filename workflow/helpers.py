from scripts.utils import get_bvals
from glob import glob


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


def all_outputs():
    inputs = glob("sub-*/ses-*/dwi/*_dir-AP_dwi.nii.gz")
    outprefix = ["derivatives/dti_smk/" + "/".join(x.split("/")[:2]) for x in inputs]
    outfiles = [
        "eddy/ec_data.qc/qc.json",
        "dtifit/fit_tensor.nii.gz",
        "bedpostx.bedpostX/nodif_brain_mask.nii.gz",
    ]
    return [f"{p}/{f}" for p in outprefix for f in outfiles]
