def get_bvals(bval_file: str) -> list[str]:
    """Read b-values from a file to list of strings

    Parameters
    ----------
    bval_file : str
        path to bval file

    Returns
    -------
    list[str]
        b-values
    """
    with open(bval_file, "r") as file:
        bvals = file.readline().strip().split(" ")
    return bvals


def get_b0s(bval_file: str) -> int:
    """Get number of 0 values in bval file

    Parameters
    ----------
    bval_file : str
        path to bval file

    Returns
    -------
    int
        number of 0 (or 0.0) values in bval file
    """
    bvals = get_bvals(bval_file)
    b0s = len([x for x in bvals if float(x) == 0.0])
    return b0s
