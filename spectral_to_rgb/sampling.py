"""
Sampling-based multiplication (lamp * reflectance) routines.
"""
import numpy as np
from spectral_data import Spectrum


def sample_random(lamp: Spectrum, refl: Spectrum, n: int):
    """
    Randomly sample n wavelengths; return tuple (wl_samples, values),
    where values are lamp*refl at sampled wavelengths.
    """
    # Determine overlapping wavelength range
    min_wl = max(lamp.wl.min(), refl.wl.min())
    max_wl = min(lamp.wl.max(), refl.wl.max())
    # Draw uniform random samples
    wl_samples = np.random.uniform(min_wl, max_wl, n)
    # Interpolate spectra at sampled wavelengths
    lamp_vals = np.interp(wl_samples, lamp.wl, lamp.values)
    refl_vals = np.interp(wl_samples, refl.wl, refl.values)
    values = lamp_vals * refl_vals
    return wl_samples, values



def sample_hero(lamp: Spectrum, refl: Spectrum):
    """
    Single-wavelength "hero" sampling: pick one random λ, weight by total.
    Returns tuple (wl_sample, value).
    """
    # Use lamp spectrum as probability distribution
    probs = lamp.values / np.sum(lamp.values)
    chosen_idx = np.random.choice(len(lamp.wl), p=probs)
    wl = lamp.wl[chosen_idx]
    lamp_val = lamp.values[chosen_idx]
    refl_val = np.interp(wl, refl.wl, refl.values)
    value = lamp_val * refl_val
    return np.array([wl]), np.array([value])


def sample_fixed(lamp: Spectrum, refl: Spectrum, m: int):
    """
    Equidistant sampling at m midpoints across 380–730 nm.
    Returns tuple (wl_samples, values).
    """
    wl_samples = np.linspace(380, 730, m)
    lamp_vals = np.interp(wl_samples, lamp.wl, lamp.values)
    refl_vals = np.interp(wl_samples, refl.wl, refl.values)
    values = lamp_vals * refl_vals
    return wl_samples, values