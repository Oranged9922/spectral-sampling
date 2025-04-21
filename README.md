# Spectral Sampling and Color Conversion Tool

This project provides a spectral renderer utility that:

- Loads spectral power distributions (lamps) and surface reflectance data.
- Multiplies them using various sampling strategies.
- Converts the result to CIE XYZ and sRGB values.
- Outputs or compares results across different methods and parameters.

## Features

- Built-in support for multiple CIE luminaires and reflectance datasets.
- Three sampling strategies:
  - **Random wavelength sampling**
  - **Hero wavelength sampling** (single importance sample)
  - **Fixed equidistant sampling**
- Full CIE 1931 color space conversion.
- Optional gamma correction.
- CLI batch table output mode for RGB comparisons.

## Project Structure

```
spectral_to_rgb/
├── spectral_data.py     # Spectral file loading and representation
├── sampling.py          # Spectral multiplication via sampling
├── color_utils.py       # Spectrum to XYZ and RGB conversion
├── utils.py             # Interpolation and integration utilities
├── main.py              # Command-line interface
├── data/                # CSV files for lamps, reflectance, CMFs
```

## Usage

### 1. Run a Single Experiment

```bash
python main.py --lamp illuminant_A --refl A1_white --method fixed --count 20
```

Optional:

- Use `--no-gamma` to skip gamma correction.

### 2. Compare Multiple Spectra (Batch Table Mode)

```bash
python main.py --method random --count 100 --table
```

Prints a table with reflectance patches as rows and lamps as columns.

## Data Format

CSV files in `data/` must have two columns:

```
wavelength,value
```

Lines starting with `#` are ignored.

- CMF data must include `wavelength,x,y,z`.
- All spectra should cover overlapping regions (ideally 380–730 nm).

## Output Example

```
Method: fixed, Samples: 20, Time: 0.002s, RGB: [0.61 0.48 0.29]
```

## Requirements

- Python 3.11+
- NumPy

