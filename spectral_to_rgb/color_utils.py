"""
Convert sampled spectra to color (XYZ → sRGB).
"""
import numpy as np
from utils import interpolate_to_grid, integrate_trapezoid

# Placeholder for CIE 1931 CMFs; loaded via load_cmf()
CMF_WL, xbar, ybar, zbar = None, None, None, None

def load_cmf(cmf_csv: str = 'data/cmf1931.csv'):
    """Initialize CMF arrays (e.g., from file with columns: wl, x, y, z)."""
    global CMF_WL, xbar, ybar, zbar
    data = np.loadtxt(cmf_csv, delimiter=',', comments='#', skiprows=1)
    CMF_WL = data[:, 0]
    xbar = data[:, 1]
    ybar = data[:, 2]
    zbar = data[:, 3]


def spectrum_to_xyz(wl_samples: np.ndarray, vals: np.ndarray) -> np.ndarray:
    """
    Compute X, Y, Z by integrating vals * CMFs over wl_samples.
    """
    if CMF_WL is None:
        raise RuntimeError("CMFs not loaded: call load_cmf() first.")
    # Interpolate val*cmf onto CMF_WL grid
    vals_interp = interpolate_to_grid(wl_samples, vals, CMF_WL)
    X = integrate_trapezoid(CMF_WL, vals_interp * xbar)
    Y = integrate_trapezoid(CMF_WL, vals_interp * ybar)
    Z = integrate_trapezoid(CMF_WL, vals_interp * zbar)
    return np.array([X, Y, Z])


def xyz_to_srgb(xyz: np.ndarray, apply_gamma: bool = True) -> np.ndarray:
    """
    Apply linear transform and optional gamma correction to get sRGB.
    """
    # sRGB D65 transform
    M = np.array([[ 3.2406, -1.5372, -0.4986],
                  [-0.9689,  1.8758,  0.0415],
                  [ 0.0557, -0.2040,  1.0570]])
    rgb_linear = M.dot(xyz)
    # Clip
    rgb_linear = np.clip(rgb_linear, 0, None)

    if not apply_gamma:
        return rgb_linear

    # Gamma correction
    def gamma(u):
        return 12.92*u if u <= 0.0031308 else 1.055*u**(1/2.4) - 0.055

    rgb = np.array([gamma(u) for u in rgb_linear])
    return rgb