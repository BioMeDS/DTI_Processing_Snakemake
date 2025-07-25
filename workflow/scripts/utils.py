def get_bvals(bval_file):
    with open(bval_file, "r") as file:
        bvals = file.readline().strip().split(" ")
    return bvals


def get_b0s(bval_file):
    bvals = get_bvals(bval_file)
    b0s = len([x for x in bvals if x == "0.0"])
    return b0s
