from glob import glob
import numpy as np
import additional_scripts.helper_functions as helper_functions

# create config lists to determine the names of the input files for extracting ROIs in the first rule
conf = helper_functions.generate_config()

# directory for scripts
script_dir = config["path_to_scripts"]

# get indices of similar vector triplets from bvec files
with open(conf["bvecs"][0],'r') as file:
    lines = file.readlines()

numbers = [line.strip().split() for line in lines]
numbers = [[float(num) for num in line] for line in numbers]

#call function from helper_functions
zero_triplets, similar_triplets_list = helper_functions.get_similar_vectors(numbers)

# get length of bval content
# list of all bval files
bval_files = glob('origs/*bval')
# filter out files with "short" or "sorted" in name
filtered_files = [f for f in bval_files if "short" not in f and "sorted" not in f]
# select one file from filtered list
if filtered_files:
    selected_file = filtered_files[0]
    with open(selected_file, "r") as bval:
        content = bval.read()
        bval_list = content.split()
        length = len(bval_list)

    bval_length = length

# define wildcard content for rule "shorten_bvec_bval"
endings = [".bvec", ".bval"]
bvec_files = glob("origs/*.bvec")
bvec_files_cut = [x.replace(".bvec", "").replace("origs/", "") for x in bvec_files]
samples = bvec_files_cut

# rule all: rule, that takes the output of the last rule in the workflow as input
# -> beginning of backward search for files needed to fulfill the input requirements
# -> builds DAG: list of rules that have to be executed to obtain the input file(s) for rule "all"
rule all:
    input:
        #expand("con/dd{number}_m0000.nii.gz", number=config["b_values"])
        #expand("con/dd{number}_m{index}.nii.gz", index=[f"{i:04d}"  for i in range(69)], number=config["b_values"])
        #expand("con/dd{number}_v69.nii.gz", number=config["b_values"]),
        #expand("con/b0_{number}.nii.gz", number=config["b_values"]),
        #expand("{sample}_short{ext}", sample=samples, ext=endings),
        #"con/"+config["PA_names"][0]+"_roi.nii.gz"
      #  expand("bvecs_bvals/{sample}_short_sorted{ext}", sample=samples, ext=endings),
        #"acqparams.txt",
        #"index.txt",
        #"data69.nii.gz",
        #"b0_AP_PA.nii.gz",
        #"sorted_bvals_combined.bval",
        #"sorted_bvecs_combined.bvec",
        #"ec_data.nii.gz",
        #"dti_cp_bedpostx/nodif_brain_mask.nii.gz",
        "fit_tensor.nii.gz",
        "dti_cp_bedpostx.bedpostX/nodif_brain_mask.nii.gz"



# extract ROIs
rule extract_roi:
    input:
        lambda wc: [x for x in conf["niftis"] if f"DTI_{wc}" in x][0]
    output:
        "con/ddiff_{number}.nii.gz"
    params:
        roi_params=config["ROI_params"]
    shell:
        "fslroi {input} {output} {params.roi_params}"

# extract ROIs from PA
rule extract_pa_roi:
    input:
        conf["PA_niftis"][0]
    output:
        "con/" + conf["PA_names"][0] + "_roi.nii.gz"
    params:
        roi_params=config["ROI_params"]
    shell:
        "fslroi {input} {output} {params.roi_params}"

# list of output file names for rule "split_4D"
split_output = [f"con/dd{{number}}_{index:04d}.nii.gz" for index in range(bval_length)]

# split 4D files into separate 3D volumes
rule split_4D:
    input:
        "con/ddiff_{number}.nii.gz"
    output:
        split_output
    shell:
        "fslsplit {input} con/dd{wildcards.number}_ -t"

# read bvecs and store them in lists
bvec_lists = {b_value: [] for b_value in conf["b_values"]}

def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        numbers_list = []
        for line in file:
            numbers_str = line.split()
            numbers_list.extend([int(num) if '.' not in num else float(num) for num in numbers_str])
        return numbers_list


for b_value in conf["b_values"]:
    bvec_files = glob(f'origs/*{b_value}*.bvec')
    for file_path in bvec_files:
        bvec_lists[b_value].extend(read_file_to_list(file_path))

bvec_index = {b_value: np.arange(len(bvec_lists[b_value][:bval_length])) for b_value in bvec_lists}

# filter out integers -> everything but 0 stays
#def generate_triplet_input(wc):
#    bvec_in = [x for x in bvec_index[wc["number"]] if not isinstance(bvec_lists[wc["number"]][x], int)]
#    position = int(wc["index"]) * 3
#    file_numbers = bvec_in[position:position+3]
#    file_names = [f"con/dd{wc['number']}_{x:04d}.nii.gz" for x in file_numbers]
#    return file_names

# same as previous function, but isn't fixed for sets of three,
# takes indices of sublists of similar_triplets_list to determine which positions should be merged
def generate_set_merge_input(wc):
    bvec_in = [x for x in bvec_index[wc["number"]] if not isinstance(bvec_lists[wc["number"]][x], int)]
    position = int(wc["index"]) * 3
    for y in range(len(similar_triplets_list)):
        set_length = len(similar_triplets_list[y])
        file_numbers = bvec_in[position:position+set_length]
        file_names = [f"con/dd{wc['number']}_{x:04d}.nii.gz" for x in file_numbers]
    return file_names

# filter out float values -> only 0s stay
def generate_b0_input(wc):
    bvec_ind = [x for x in bvec_index[wc["number"]] if isinstance(bvec_lists[wc["number"]][x], int)]
    b0_file_names = [f"con/dd{wc['number']}_{x:04d}.nii.gz" for x in bvec_ind]
    return b0_file_names

#rule merge_triplet:
#    input:
#        generate_triplet_input
#    output:
#        "con/dd{number}_c{index}.nii.gz"
#    shell:
#        "fslmerge -t {output} {input}"

rule merge_sets:
    input:
        generate_set_merge_input
    output:
        "con/dd{number}_c{index}.nii.gz"
    shell:
        "fslmerge -t {output} {input}"

rule merge_b0:
    input:
        generate_b0_input
    output:
        "con/b0_{number}.nii.gz"
    shell:
        "fslmerge -t {output} {input}"

rule t_mean:
    input:
        "con/dd{number}_c{index}.nii.gz"
    output:
        "con/dd{number}_m{index}.nii.gz"
    shell:
        "fslmaths {input} -Tmean {output}"

# merge all dd... files into a single one
rule merge_files:
    input:
        lambda wc: expand("con/dd{number}_m{index}.nii.gz", index=[f"{i:04d}" for i in range(69)], number=[wc.number])
    output:
        "con/dd{number}_v69.nii.gz"
    shell:
        "fslmerge -t {output} {input}"

# rule to modify the bvec and bval files: shortens number of non-0 entries so that three become one
rule shorten_bvec_bval:
    input:
        "origs/{sample}{ext}"
    output:
        "bvecs_bvals/{sample}_short{ext}"
    shell:
        "python {script_dir}shorten_bval.py {input} {output}"

# rule to sort bval content -> first "0"s, then other values
rule sort_bval:
    input:
        "bvecs_bvals/{sample}_short{ext}"
    output:
        "bvecs_bvals/{sample}_short_sorted{ext}"
    shell:
        "python {script_dir}sort_bval.py {input} {output}"

def nii_to_bval(nifti):
    return nifti.replace(".gz", "").replace(".nii", "_short_sorted.bval").replace("origs", "bvecs_bvals")

def nii_to_bvec(nifti):
    return nifti.replace(".gz", "").replace(".nii", "_short_sorted.bvec").replace("origs", "bvecs_bvals")

def sort_by_bval(unsorted_list, bvals):
    return sorted(unsorted_list, key=lambda x: int(bvals[unsorted_list.index(x)]))


# rule to combine 500 and 800 bval (or other values)
rule combine_bvals:
    input:
        [nii_to_bval(x) for x in sort_by_bval(conf["niftis"], conf["b_values"])]
    output:
        "sorted_bvals_combined.bval"
    shell:
        "python {script_dir}combine_bvals.py {input}"

# do the same for bvecs
rule combine_bvecs:
    input:
        [nii_to_bvec(x) for x in sort_by_bval(conf["niftis"], conf["b_values"])]
    output:
        "sorted_bvecs_combined.bvec"
    shell:
        "python {script_dir}combine_bvecs.py {input}"


# rule to make acqparams and index files
rule create_configs:
    input:
        bval=expand("bvecs_bvals/{sample}_short.bval", sample=samples[0]),
        json=conf["jsons"][0],
        nii=conf["PA_niftis"][0]
    output:
        "acqparams.txt",
        "index.txt"
    shell:
        "python {script_dir}create_config_extended.py --bval {input.bval} --json {input.json} --nii {input.nii}"


def sort_niftis(unsorted_list):
    return sorted(unsorted_list, key=lambda x: int(x))

# merge b0s
rule merge_all_b0s:
    input:
        b0_AP = expand("con/b0_{number}.nii.gz", number=sort_niftis(conf["b_values"])),
        b0_PA = "con/" + conf["PA_names"][0] + "_roi.nii.gz"
    output:
        "b0_AP_PA.nii.gz"
    shell:
        "fslmerge -t {output} {input.b0_AP} {input.b0_PA}"

# adds elements of nested list together, [] as start value; default start value = 0 -> can't add lists to 0
def flatten_list(nested_list):
    return sum(nested_list, [])

# merge b0 from bvalue 1, non-b0 from bvalue 1, b0 from bvalue 2, non-b0 from bvalue 2 and so on
rule merge_all_AP_niftis:
    input:
        flatten_list([[f"con/b0_{number}.nii.gz", f"con/dd{number}_v69.nii.gz"] for number in sort_niftis(conf["b_values"])])
    output:
        "data69.nii.gz"
    shell:
        "fslmerge -t {output} {input}"


### topup ###

# path to config file:
b02b0 = script_dir+"b02b0_4.cnf"

rule topup:
    input:
        nifti = "b0_AP_PA.nii.gz",
        acqp = "acqparams.txt",
        config = b02b0
    output:
        coef = "topupres_fieldcoef.nii.gz",
        movpar = "topupres_movpar.txt",
        hifi = "hifi_b0.nii.gz"
    resources:
        runtime = 60
    shell:
        "topup --imain={input.nifti} --datain={input.acqp} --config={input.config} --out=topupres --iout={output.hifi}"

rule b0_t_mean:
    input:
        "hifi_b0.nii.gz"
    output:
        "hifi_b0_mean.nii.gz"
    shell:
        "fslmaths {input} -Tmean {output}"

rule b0_mask:
    input:
        "hifi_b0_mean.nii.gz"
    output:
        "hifi_b0_mean_mask.nii.gz"
    shell:
        "fslmaths {input} -mul 0 -add 1 {output}"


## eddy ##

rule eddy:
    input:
        image = "data69.nii.gz",
        mask = "hifi_b0_mean_mask.nii.gz",
        acqp = "acqparams.txt",
        index = "index.txt",
        bvec = "sorted_bvecs_combined.bvec",
        bval = "sorted_bvals_combined.bval",
    output:
        "ec_data.eddy_rotated_bvecs",
        "ec_data.nii.gz"
    resources:
        runtime = 600
    shell:
        "eddy --imain={input.image} --mask={input.mask} --acqp={input.acqp} --index={input.index} --bvecs={input.bvec} --bvals={input.bval} --topup=topupres --out=ec_data"


## DTIFIT ##

# in the following rules, several files just get copied into a new directory
rule copy_bvals:
    input:
        "sorted_bvals_combined.bval"
    output:
        "dti/bvals"
    shell:
        "cp {input} {output}"

rule copy_bvecs:
    input:
        "ec_data.eddy_rotated_bvecs"
    output:
        "dti/bvecs"
    shell:
        "cp {input} {output}"

rule copy_ec_data:
    input:
        "ec_data.nii.gz"
    output:
        "dti/data.nii.gz"
    shell:
        "cp {input} {output}"

rule copy_mask:
    input:
        mask="hifi_b0_mean_mask.nii.gz", #all other input is just there for this rule to be the last copy rule
        bvals="dti/bvals",
        bvecs="dti/bvecs",
        data="dti/data.nii.gz"
    output:
        "dti/nodif_brain_mask.nii.gz"
    shell:
        "cp {input.mask} {output}"

# make a copy of dti folder for bedpostx; bedpostx must be applied to data that dtifit has not been applied to
rule copy_dti_folder:
    input:
        "dti/nodif_brain_mask.nii.gz"
    output:
        "dti_cp_bedpostx/nodif_brain_mask.nii.gz"
    shell:
        "cp -R dti/* dti_cp_bedpostx"

# apply DTIFIT
rule dtifit:
    input:
        bvals = "dti/bvals",
        bvecs = "dti/bvecs",
        data = "dti/data.nii.gz",
        mask = "dti/nodif_brain_mask.nii.gz",
        mask_in_folder_copy = "dti_cp_bedpostx/nodif_brain_mask.nii.gz" #no input for this rule, but dti folder must be copied before this rule is executed
    output:
        "fit_tensor.nii.gz"
    shell:
        "dtifit -k {input.data} -o fit -m {input.mask} -r {input.bvecs} -b {input.bvals} --sse --save_tensor"


## BEDPOSTX ##
rule bedpostx:
    input:
        "dti_cp_bedpostx/nodif_brain_mask.nii.gz"
    output:
        "dti_cp_bedpostx.bedpostX/nodif_brain_mask.nii.gz"
    resources:
        runtime = 1000
    shell:
        "bedpostx dti_cp_bedpostx"
