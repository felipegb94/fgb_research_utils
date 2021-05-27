## Standard Library Imports

## Library Imports
import numpy as np
from IPython.core import debugger
breakpoint = debugger.set_trace

## Local Imports
from .shared_constants import *

def gamma_tonemap(img, gamma = 1/2.2):
    assert(gamma <= 1.0), "Gamma should be < 1"
    assert(0.0 <= gamma), "Gamma should be non-neg"
    tmp_img = np.power(img, gamma)
    return tmp_img / tmp_img.max()