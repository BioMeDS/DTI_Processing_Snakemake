# Overview

Automated FSL-based processing pipeline for DTI (Diffusion Tensor Imaging) data. Specifically for non-brain images (e.g. images of DRG (Dorsal Root Ganglia))

## What does this pipeline do?
- optionally ROIs are extracted from the images, using `fslroi`
- all images with b-value 0 are extracted (in both AP and PA direction) and recombined for topup
- the AP and PA file (nifti, bvec, and bval) are concatenated for eddy
- config files for topup and eddy are created
- then topup and eddy are applied
- dtifit is applied to the eddy corrected data
- bedpostX is applied to the eddy corrected data

The workflow can be run with slurm (`--executor slurm`). Start it in the root of a [BIDS](https://bids.neuroimaging.io/index.html) dataset and all subjects and sessions with `dwi` images in `dir-AP` and `dir-PA` are processed. Outputs are stored under `derivatives/dti_smk`.


# Requirements

The listed versions are the ones this pipeline was developed with. It might work with other (particularly newer) versions.

- [FSL](https://fsl.fmrib.ox.ac.uk/fsl/docs/#/) (6.0.7.18)
- [Snakemake](https://snakemake.readthedocs.io/en/stable/) (9.9.0)
- (optional) [snakemake-executor-plugin-slurm](https://snakemake.github.io/snakemake-plugin-catalog/plugins/executor/slurm.html) (1.6.0)


# How to run it?

Navigate into the root of your [BIDS](https://bids.neuroimaging.io/index.html) dataset and run (adjusting the path to the Snakefile and number of cpus):

```bash
snakemake --snakefile /path/to/workflow/Snakefile --cores 6
```

If you are on a SLURM cluster (and you have `snakemake-executor-plugin-slurm` installed), you can run (again adjusting parameters as appropriate):

```bash
snakemake --snakefile /path/to/workflow/Snakefile --executor slurm --default-resources mem_mb=1000 cpus_per_task=2 runtime=60 --jobs 10 --latency-wait 60 
```

# Additional naming requirements

the full [BIDS](https://bids.neuroimaging.io/index.html) specification is not supported, yet.

There are currently still some limitations:
- the session level is not optional ([`_ses-<label>`](https://bids-specification.readthedocs.io/en/latest/appendices/entities.html#ses))
- the PhaseEncodingDirection has to be in `_dir-<label>` and only "AP" and "PA" are supported (in uppercase letters)
- no additional file name components are currently accepted (acq, rec, run, part, chunk)

# For developers

Install dependencies with:

```bash
uv sync
```

Run tests with:

```bash
uv run python -m unittest
```

## Contributing

Contributions are welcome, including but not limited to bug fixes, new features, documentation, and tests.