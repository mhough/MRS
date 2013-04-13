import os
import tempfile

import numpy as np
import numpy.testing as npt
import matplotlib
matplotlib.use('agg')

import MRS.utils as ut
import MRS


def test_mrs_analyze():
    """
    Test the command line utility
    """
    mrs_path = MRS.__path__[0]
    out_name = tempfile.NamedTemporaryFile().name
    # Check that it runs through:
    cmd = 'mrs-analyze.py pure_gaba_P64024.7 %s.csv'%out_name
    npt.assert_equal(os.system(cmd),0)

    # XXX We might want to analyze the output file here...
