## Standard Library Imports

## Library Imports
import numpy as np
import torch
import torch.nn
from IPython.core import debugger
breakpoint = debugger.set_trace

## Local Imports



def softmax_scoring(scores, gt_indeces, beta=300., eps=1, axis=-1):
    '''
        apply softmax to scores to make into probability distribution
        then use the gt_indeces to take a look at the softmax scores of each sample in the +/- eps neightborhood
        return the sum of these scores
    '''
    assert(eps >= 0),'eps should be non-negative'
    softmax_scores = torch.nn.functional.softmax(scores*beta, dim=axis)
    n_scores = (2*eps)+1
    (min_idx, max_idx) = (0, scores.shape[axis])
    for i in range(n_scores):
        offset = -1*eps + i
        indeces = torch.clamp(gt_indeces + offset, min=min_idx, max=max_idx-1)
        selected_scores = softmax_scores.gather(axis, indeces.long().unsqueeze(axis))
    return selected_scores.sum()