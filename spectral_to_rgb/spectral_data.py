"""
Load and represent spectral distributions (lamps & reflectances).
"""
import numpy as np
import os
import glob

class Spectrum:
    def __init__(self, wavelengths: np.ndarray, values: np.ndarray):
        """
        wavelengths: 1D array of wavelengths in nm
        values: spectral power or reflectance at those wavelengths
        """
        if wavelengths.shape != values.shape:
            raise ValueError("Wavelengths and values must have the same shape.")
        self.wl = wavelengths
        self.values = values


def load_spectrum_from_csv(path: str) -> Spectrum:
    """
    Read a two-column CSV: wavelength (nm), value.
    Ignores lines starting with '#'.
    """
    data = np.loadtxt(path, delimiter=',', comments='#', skiprows=1)
    wavelengths = data[:, 0]
    values = data[:, 1]
    return Spectrum(wavelengths, values)


def load_builtin_spectra(data_dir: str = 'data') -> dict:
    """
    Load all CSV spectra from a directory.
    Returns dict[name, Spectrum], where name is the filename without extension.
    """
    spectra = {}
    for filepath in glob.glob(os.path.join(data_dir, '*.csv')):
        name = os.path.splitext(os.path.basename(filepath))[0]
        spectra[name] = load_spectrum_from_csv(filepath)
    return spectra