from glob import glob

def get_similar_vectors(numbers):
    """
    Get indices of 0-vectors and indices of consecutive similar vectors in a list of vectors.
    Input vectors are given as list of lists with components in sublists (as lines read from the bvec file).
    A vector is considered similar to the previous one if it has the same numbers in the same order.
    Example:
    numbers = [
        [0, 1, 1, 1, 4, 4, 0, 7],
        [0, 2, 2, 2, 5, 5, 0, 8],
        [0, 3, 3, 3, 6, 6, 0, 9]
    ]
    get_similar_vectors(numbers) -> ([0,6], [[1, 2, 3], [4, 5], [7]])
    """
    zero_indices = []
    replicate_indices = []
    current_vector = []

    for i in range(len(numbers[0])):
        vector = [numbers[j][i] for j in range(3)]

        # Check if all numbers in triplet are 0
        if all(num == 0 for num in vector):
            zero_indices.append(i)
        else:
            # If the current triplet is not all zeros, check if it's similar to the previous one
            if i > 0 and vector == [numbers[j][i-1] for j in range(3)]:
                # If similar, append to the current list
                current_vector.append(i)
            else:
                # If not similar, append the current list to similar_triplets_lists and start a new list
                if current_vector:
                    replicate_indices.append(current_vector)
                current_vector = [i] # Start a new list with the current index

    # Append the last list of indices if it's not empty
    if current_vector:
        replicate_indices.append(current_vector)

    return zero_indices, replicate_indices

def generate_config():
    niftis = glob("origs/*DTI*AP*.nii*")
    print(niftis)
    b_niftis = [x.replace("origs/", "").replace("_AP", "").replace("_iso", ""). replace(".nii", "").replace(".gz", "").replace("_2.2", "") for x in niftis if "DTI" in x and not "_b0_" in x]
    sample_ids = [x.split("_DTI_")[0] for x in b_niftis]
    b_values = [x.split("_DTI_")[1] for x in b_niftis]
    shortbvals = glob("bvecs_bvals/*short.bval")
    PA_niftis = glob("origs/*PA*nii*")
    PA_names = [x.replace ("origs/", "").replace(".nii", "").replace(".gz", "").replace("_iso", "").replace("_2.2", "") for x in PA_niftis]
    jsons = glob("origs/*DTI*AP*json")
    bvecs = glob("origs/*.bvec")
    AP_b0s = [f for f in glob("*b0*.nii.gz") if not "PA" in f]
    return {"sample_ids": sample_ids, "b_values": b_values, "niftis": niftis, "shortbvals": shortbvals, "PA_niftis": PA_niftis, "PA_names": PA_names, "jsons": jsons, "bvecs": bvecs, "AP_b0s": AP_b0s}

def generate_config_oldprot():
    niftis = glob("origs/*diff*.nii*")
    b_niftis = [x.replace("origs/", "").replace("_74", "").replace("_long", "").replace("diff", "").replace("_AP", "").replace("_PA", "").replace("_iso", "").replace(".nii", "").replace(".gz", "") for x in niftis if not "_b0_" in x]
    sample_ids = [x.split("_ep2d_")[0] for x in b_niftis]
    b_values = [x.split("_ep2d_")[1] for x in b_niftis]
    shortbvals = glob("bvecs_bvals/*short.bval")
    PA_niftis = glob("origs/*PA*nii*")
    PA_names = [x.replace("origs/", "").replace("_74", "").replace("_long", "").replace("diff", "").replace("_AP", "").replace("_PA", "").replace("_iso", "").replace(".nii", "").replace(".gz", "") for x in PA_niftis]
    jsons = glob("origs/*diff*json")
    bvecs = glob("origs/*.bvec")
    #AP_b0s = [f for f in glob("*b0*.nii.gz") if not "PA" in f]
    return {"sample_ids": sample_ids, "b_values": b_values, "niftis": niftis, "shortbvals": shortbvals, "PA_niftis": PA_niftis, "PA_names": PA_names, "jsons": jsons, "bvecs": bvecs}#, "AP_b0s": AP_b0s}
