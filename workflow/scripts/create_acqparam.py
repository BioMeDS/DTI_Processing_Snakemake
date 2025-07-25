import json
from snakemake.script import snakemake
from utils import get_b0s

ap_bval = snakemake.input[0]
ap_json = snakemake.input[1]
pa_bval = snakemake.input[2]
pa_json = snakemake.input[3]

acqparam = snakemake.output[0]


def get_readout_time(json_file):
    with open(json_file, "r") as file:
        metadata = json.load(file)
    # echo_spacing = metadata["DerivedVendorReportedEchoSpacing"]
    # pe_steps = metadata["PhaseEncodingSteps"]
    # readout_time = round(echo_spacing * (pe_steps - 1), 3)
    readout_time = metadata["TotalReadoutTime"]
    return readout_time


ap_readout_time = get_readout_time(ap_json)
pa_readout_time = get_readout_time(pa_json)
ap_b0s = get_b0s(ap_bval)
pa_b0s = get_b0s(pa_bval)
ap_line = f"0 1 0 {ap_readout_time}\n"
pa_line = f"0 -1 0 {pa_readout_time}\n"

with open(acqparam, "w") as file:
    for i in range(ap_b0s):
        file.write(ap_line)
    for i in range(pa_b0s):
        file.write(pa_line)
