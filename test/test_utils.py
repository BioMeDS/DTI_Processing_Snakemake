from workflow.scripts.utils import get_b0s


def test_get_b0s():
    # assert equal 6
    assert get_b0s("test/data/simple.bval") == 6
