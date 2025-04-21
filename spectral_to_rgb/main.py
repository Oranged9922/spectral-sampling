"""
Command-line interface for running spectral sampling experiments.
"""
import argparse
import time
import numpy as np
from spectral_data import load_builtin_spectra
from sampling import sample_random, sample_hero, sample_fixed
from color_utils import load_cmf, spectrum_to_xyz, xyz_to_srgb

def run_experiment(lamp_name, refl_name, method, count):
    # load data
    spec = load_builtin_spectra()
    lamp = spec[lamp_name]
    refl = spec[refl_name]

    # sampling and timing
    t0 = time.time()
    wl_vals = {
        'random': lambda: sample_random(lamp, refl, count),
        'hero': lambda: sample_hero(lamp, refl),
        'fixed': lambda: sample_fixed(lamp, refl, count),
    }[method]()
    t1 = time.time()

    # color conversion
    xyz = spectrum_to_xyz(*wl_vals)
    rgb = xyz_to_srgb(xyz, apply_gamma=True)

    print(f"Method: {method}, Samples: {count}, Time: {t1-t0:.3f}s, RGB: {rgb}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Run spectral sampling experiments. Specify a lamp spectrum, a reflectance spectrum, sampling method, and sample count.'
    )
    parser.add_argument(
        '--lamp', required=False,
        help='Name of the luminance spectrum (e.g., illuminant_A, illuminant_D65, F11)'
    )
    parser.add_argument(
        '--refl', required=False,
        help='Name of the reflectance spectrum (e.g., E2_dark_skin, F4_green, A1_white)'
    )
    parser.add_argument(
        '--method', choices=['random','hero','fixed'], default='random', required=False,
        help='Sampling method: random (n random wavelengths), hero (single representative wavelength), or fixed (m evenly-spaced samples)'
    )
    parser.add_argument(
        '--count', type=int, default=100,
        help='Number of samples (n for random & fixed; ignored for hero)'
    )
    parser.add_argument(
        '--table', action='store_true',
        help='Output a summary table for all built-in lamp and reflectance combinations.'
    )
    parser.add_argument(
        '--no-gamma', action='store_true',
        help='Disable gamma correction in XYZ to sRGB conversion.'
    )
    args = parser.parse_args()
    load_cmf()

    # Batch table output
    if args.table:
        spec = load_builtin_spectra()
        lamps = ['illuminant_A', 'illuminant_D65', 'F11']
        refls = ['E2_dark_skin', 'F4_green', 'G4_red', 'H4_yellow', 'J4_cyan', 'A1_white']

        col_width = 22
        header = '| {:<6} |'.format('') + ''.join(f' {{:<{col_width}}} |'.format(l.replace('illuminant_', '')) for l in lamps)
        sep = '|' + '-' * 8 + '|' + '|'.join(['-' * (col_width + 2)] * len(lamps)) + '|'

        print(header)
        print(sep)
        for r in refls:
            label = r.split('_')[0]
            row_vals = []
            for l in lamps:
                lamp = spec[l]
                refl = spec[r]
                wl_samples, vals = {
                    'random': lambda: sample_random(lamp, refl, args.count),
                    'hero':   lambda: sample_hero(lamp, refl),
                    'fixed':  lambda: sample_fixed(lamp, refl, args.count),
                }[args.method]()
                xyz = spectrum_to_xyz(wl_samples, vals)
                rgb = xyz_to_srgb(xyz, apply_gamma=not args.no_gamma)
                row_vals.append(f"{rgb[0]:.2f}, {rgb[1]:.2f}, {rgb[2]:.2f}")
            row = '| {:<6} |'.format(label) + ''.join(f' {{:<{col_width}}} |'.format(val) for val in row_vals)
            print(row)
    else:
        # Single experiment
        if not args.lamp or not args.refl:
            parser.error('Must specify --lamp and --refl for single experiment mode')
        run_experiment(args.lamp, args.refl, args.method, args.count)
