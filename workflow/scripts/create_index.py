from snakemake.script import snakemake
from utils import get_bvals

ap_bval = snakemake.input[0]
pa_bval = snakemake.input[1]

index_file = snakemake.output[0]

bvals = get_bvals(ap_bval) + get_bvals(pa_bval)

with open(index_file, "w") as file:
    bval_counter = 0
    for b in bvals:
        if b == "0.0":
            bval_counter += 1
        file.write(f"{bval_counter}\n")
