#### Standard Library Imports

#### Library imports
import numpy as np
from IPython.core import debugger
breakpoint = debugger.set_trace

#### Local imports
from .signalproc_ops import circular_conv

def vectorize_tensor(tensor, axis=-1):
	'''
		Take an N-Dim Tensor and make it a 2D matrix. Leave the first or last dimension untouched, and basically squeeze the 1st-N-1
		dimensions.
		This is useful when applying operations on only the first or last dimension of a tensor. Makes it easier to input to different
		number of pytorch functions.
	'''
	assert((axis==0) or (axis==-1)), 'Error: Input axis needs to be the first or last axis of tensor'
	tensor_shape = tensor.shape
	n_untouched_dim = tensor.shape[axis]
	n_elems = int(round(tensor.size / n_untouched_dim))
	if(axis == -1):
		return (tensor.reshape((n_elems, n_untouched_dim)), tensor_shape)
	else:
		return (tensor.reshape((n_untouched_dim, n_elems)), tensor_shape)

def unvectorize_tensor(tensor, tensor_shape):
	'''
		Undo vectorize_tensor operation
	'''
	return tensor.reshape(tensor_shape)

def to_nparray( a ):
	'''
		cast to np array. If a is scalar, make it a 1D 1 element vector
	'''
	a_arr = np.array(a)
	# if it was a scalar add dimension
	if(a_arr.ndim == 0): return a_arr[np.newaxis]
	# otherwise simply return the new nparray
	return a_arr

def extend_tensor_circularly(tensor, axis=-1):
	'''
		Take a tensor of any dimension and create a new tensor that is 3x longer along the speified axis
		We take concatenate 3 copies of the tensor along the specified axis 
	'''
	return np.concatenate((tensor, tensor, tensor), axis=axis)

def get_extended_domain(domain, axis=-1):
	'''
		Take a domain defined between [min_val, max_val] with n elements. Extend it along both directions.
		So if we have the domain = [0, 1, 2, 3]. Then we output: [-4,-3,-2,-1,  0,1,2,3,  4,5,6,7] 
	'''
	n = domain.shape[axis]
	min_val = domain.min(axis=axis)
	assert(min_val >= 0), "get_extended_domain currentl only works for non-negative domains"
	max_val = domain.max(axis=axis)
	delta = domain[1] - domain[0]
	domain_left = domain-(max_val + delta)
	domain_right = domain+(max_val + delta)
	return np.concatenate((domain_left, domain, domain_right), axis=axis)

def normalize_signal(v, axis=-1): return v / v.sum(axis=axis, keepdims=True)

def gaussian_pulse(time_domain, mu, width, circ_shifted=True):
	'''
		Generate K gaussian pulses with mean=mu and sigma=width.
		If circ_shifted is set to true we create a gaussian that wraps around at the boundaries.
	'''
	mu_arr = to_nparray(mu)
	width_arr = to_nparray(width)
	assert((width_arr.size==1) or (width_arr.size==mu_arr.size)), "Input mu and width should have the same dimensions OR width should only be 1 element"
	if(circ_shifted):
		ext_time_domain = get_extended_domain(time_domain)
		ext_pulse = np.exp(-1*np.square((ext_time_domain[np.newaxis,:] - mu_arr[:, np.newaxis]) / width_arr[:, np.newaxis]))
		n_bins = time_domain.shape[-1]
		pulse = ext_pulse[...,0:n_bins] + ext_pulse[...,n_bins:2*n_bins] + ext_pulse[...,2*n_bins:3*n_bins]
	else:
		pulse = np.exp(-1*np.square((time_domain[np.newaxis,:] - mu_arr[:, np.newaxis]) / width_arr[:, np.newaxis]))
	return normalize_signal(pulse.squeeze(), axis=-1)

def expgaussian_pulse_erfc(time_domain, mu, sigma, exp_lambda):
    if(exp_lambda is None): return gaussian_pulse(time_domain, mu, sigma)
    mu_arr = to_nparray(mu)
    sigma_sq = np.square(sigma)
    mu_minus_t = mu_arr[:, np.newaxis] - time_domain[np.newaxis,:]  
    lambda_sigma_sq = exp_lambda*sigma_sq
    erfc_input = (mu_minus_t + lambda_sigma_sq) / sigma
    pulse = exp_lambda*np.exp(0.5*exp_lambda*(lambda_sigma_sq + 2*mu_minus_t))*scipy.special.erfc(erfc_input)
    return normalize_signal(pulse.squeeze(), axis=-1)

def expgaussian_pulse_conv(time_domain, mu, sigma, exp_lambda):
    gauss_pulse = gaussian_pulse(time_domain, mu, sigma)
    if(exp_lambda is None): return gauss_pulse
    exp_decay = np.exp(-1*exp_lambda*time_domain)[np.newaxis,:]
    expgauss_pulse = circular_conv(exp_decay, gauss_pulse, axis=-1)
    return normalize_signal(expgauss_pulse.squeeze(), axis=-1)