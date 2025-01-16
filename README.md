# Overview

Automated processing pipeline for DTI (Diffusion Tensor Imaging) data, specifically for images of DRG (Dorsal Root Ganglia)

## What does this pipeline do?
- ROIs are extracted from the images, using fslroi (the parameters can be set in `config.yml`)
- The original NIfTI files are split into single volumes and then remergd into two new files (One with all volumes recorded in AP direction with b-values in ascending order and one with all b0 volumes, in both AP and PA direction); 
- For datasets with multiple consecutive volumes with the same bvec entries, these volumes are shortened to one and their temporal mean is calculated
- The content of the bvec and bval files is rearranged in new files to match the new NIfTI files
- Config files for topup and eddy are created
- Then topup and eddy are applied
- A folder for DTIFit is created and copied for BEDPOSTX (they need the same input data, but different folders)
- BEDPOSTX and DTIFit are executed

The workflow can be run with SLURM in several directories simultaneously and takes about eight to ten hours to finish.


# Conda environment

`mamba env create -f environment.yml`


# Which of the two Snakemake files should you use?

There are two slightly different Snakemake workflows: 
- One workflow for datasets with one or more NIfTI files recorded in AP direction with different b-values, interspersed with b0 volumes and one NIfTI file in PA direction containing only b0 volumes and the corresponding bvec, bval and json files
- One workflow for datasets with one NIfTI file in AP and one NIfTI file in PA direction with different b-values, interspersed with b0 volumes and the corresponding bvec, bval and json files; these datasets don’t contain separate b0 NIfTI files

For the former, use the `DTI_Snakemake.smk` workflow and the `ROI_params` section in `config.yml` for the fslroi operation; For the latter, use the `DTI_Snakemake_old_prot.smk` workflow and the `ROI_old` section in `config.yml`.


# How should the data be named?

## For DTI_Snakemake.smk:

The NIfTI files for the volumes in AP direction should look something like this: `006_DTI_800_AP.nii.gz`

With:
- `006`: Sample ID
- `DTI`: Fixed part of the name between Sample ID and b-value
- `800`: B-value
- `AP`: Phase-encoding direction; fixed name part
- `nii.gz`: File name extension; `.gz` is optional
  
The corresponding .bval, .bvec and .json files should have the same names with the respective extension.

For the b0 volumes in PA direction, only a NIfTI and a .json file are necessary. They should be named after this scheme: `014_DTI_b0_PA` with the respective name extension

## For DTI_Snakemake_old_prot.smk:

All files should be named after this scheme: `017_ep2d_diff800_PA.ext`

With:
- `017`: Sample ID
- `ep2d`: Fixed value, used internally to split the filenames
- `diff800`: Fixed name part + b-value
- `PA`: Phase-encoding direction (either AP or PA)
  
## Naming flexibility

I will keep improving the workflow so that it allows for a more flexible naming of the input files. As of now, certain additional parts, like `_long`, `_iso`, or `_2.2` may also be contained in the file names without causing trouble.


# Config.yml

The configuration file `config.yml` allows you to set the path to the directory that contains all additional python scripts that are used in the workflow, as well as the parameters for fslroi (separately for both Snakefiles) and the max runtime for each SLURM job. 


# How to run the workflow

You can either navigate into the directory in which your raw data is located and then run the following command (Note that the directory needs a sub-directory called „origs“ that contains the raw data):

`snakemake --cores 2  -p --snakefile /path/to/snakefile --configfile /path/to/config.yml --latency-wait 1000` 

Or with SLURM: 

`snakemake --cores 2  -p --executor slurm --jobs 10 --default-resources mem_mb=1000 cpus_per_task=2 --snakefile /path/to/snakefile --configfile /path/to/config.yml --latency-wait 1000` 

Explanation of the parameters:
- `--cores`: Maximum number of cores used for parallel execution; this parameter is mandatory
- `-p`: Prints the shell commands executed by the Snakemake rules; not necessary to run the code, but very helpful to keep track of the progress and for debugging
- `--latency-wait`: Latency wait time in milliseconds; this is the time Snakemake waits for a job to finish before checking its status again. This helps reduce the load on cluster systems
- `--executor`: Job scheduler for cluster execution (SLURM in this case)
- `--default-resources`: Default resource requirements for all rules in the workflow:
  - `mem_mb`: Memory per task in MB
  - `cpus_per_task`: Number of CPUs per task
- `snakefile` and `configfile`: Paths to the respective files

Alterantively, if you have multiple directories in which you want to run the workflow, you can use the script `run_snakemake_in_multiple_dirs.sh`. In this script, you need to replace the default paths with the paths to your data, your snakefile and your config.yml file. 
The script needs to be open the whole time while the workflow is running (I know, that’s a bit inconvenient, sorry), so to prevent interruptions, it’s best to run it in a tmux or screen session.
