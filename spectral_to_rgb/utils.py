"""
Helper functions: interpolation, numerical integration, etc.
"""
import numpy as np

def interpolate_to_grid(src_wl, src_values, target_wl) -> np.ndarray:
    """Interpolate src_values onto target_wl grid using linear interpolation."""
    return np.interp(target_wl, src_wl, src_values)


def integrate_trapezoid(wl, vals) -> float:
    """Simple trapezoidal integration"""
    return np.trapezoid(vals, wl)