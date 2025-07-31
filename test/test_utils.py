from workflow.scripts.utils import get_b0s, get_bvals


def test_get_bvals():
    expected_bvals = [
        "0",
        "0.0",
        "0",
        "500",
        "500",
        "500",
        "0",
        "200",
        "200.0",
        "200",
        "0",
        "100",
        "100",
        "100",
        "0",
    ]
    assert get_bvals("test/data/simple.bval") == expected_bvals


def test_get_b0s():
    # assert equal 6
    assert get_b0s("test/data/simple.bval") == 6
