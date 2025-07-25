from scripts.utils import get_bvals


def get_b0_indices(filename):
    bvals = get_bvals(filename)
    return [i for i, x in enumerate(bvals) if x == "0.0"]


def get_b0_inputs(sub, dir):
    indices = get_b0_indices(f"sub-{sub}/dwi/sub-{sub}_dir-{dir}_dwi.bval")
    return [
        f"derivatives/dti_smk/sub-{sub}/b0/{dir}_{frame:04d}.nii.gz"
        for frame in indices
    ]
