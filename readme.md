kybuz — Ultrasonic Sensor Array (8x) • CAN • DBC • Live Visualization

### Overview
This repo interfaces with an array of 8 ultrasonic sensors over CAN, decodes messages using a DBC, and visualizes each sensor’s filtered distance in a live bar chart. It also logs decoded signal values to `logs/run_logs.txt`.

### Key Components
- **CAN interface**: `PCANBasic` wrapper used by `src/can_reader.py`
- **DBC decoding**: `cantools` via `src/dbc_decoder.py`, using `dbc/OX-004282_BEG_USS_COTS_V2_CAN_Matrix_external.dbc`
- **Visualization**: `matplotlib` via `src/visualizer.py` (8 bars, one per sensor)
- **Application loop**: `src/main.py`

### Requirements
- Python 3.10+
- macOS (tested on Darwin 24.x)
- Python deps: see `requirements.txt`
- CAN USB interface supported by the included `PCANBasic.py`/`libs/PCBUSB 3`

Install Python dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If needed on macOS, install the PCBUSB library provided in `libs/PCBUSB 3` (see `libs/PCBUSB 3/install.txt` and `install.sh`).

### Run
Connect the CAN adapter, then:

```bash
python src/main.py
```

- The DBC path is currently set in `src/main.py`:
  - `../dbc/OX-004282_BEG_USS_COTS_V2_CAN_Matrix_external.dbc`
  - Update this path if you relocate the DBC.
- The app prints a Rich table of filtered signals and opens a live bar chart labeled `S1..S8`.
- Logs of decoded signals are appended to `logs/run_logs.txt`.

### Signals
Main filtered distance signals consumed by the visualizer:
- `sens00De1FilteredDistance` … `sens07De1FilteredDistance`
- `Dist1` is also tracked due to naming differences in the DBC.
Units are centimeters (y-axis up to 550 cm by default).

### Project Layout (selected)
- `src/can_reader.py` — CAN receive loop using `PCANBasic`
- `src/dbc_decoder.py` — DBC lookup + decode via `cantools`
- `src/visualizer.py` — 8-bar live plot of distances
- `src/main.py` — wires CAN → DBC → filter/display, and logging
- `dbc/` — DBC file(s)
- `libs/PCBUSB 3/` — vendor library and examples
- `logs/` — runtime logs

### Troubleshooting
- No data: verify CAN adapter is recognized and bus is active at 250 kbit/s (default in `can_reader`).
- DBC decode failures: ensure the CAN IDs match the DBC; update the DBC path if moved.
- Plot not updating: confirm filtered signals appear in the console table; check for `-1` values (treated as no detection).

### Notes
- Update `src/main.py` if you want to switch between filtered and unfiltered signals.
- Sensor count is set to 8 in `src/visualizer.py` and `src/main.py`.


# TODO & Short Term Roadmap:
- [ ] Get this working on the ivory
  - [ ] Fix wiring?
  - [ ] Test 4 sensors at a time to determine if one is broken
- [ ] Add detection of obstacles
- [ ] Get 2D mapping working
  - [ ] Configure sensors
  - [ ] Change from linear to 2D array mechanically
  - [ ] Read and visualise obstacles from sensor map return values