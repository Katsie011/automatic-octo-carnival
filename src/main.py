"""
Currently terrible code.
Needs a rework, cleanup and extract configs to a config file.

But it is what it is. Gotta move fast
"""

from can_reader import CANReader
from dbc_decoder import DBCDecoder
from visualizer import Visualizer

from rich.console import Console
from rich.table import Table

import logging
import os
from typing import Any, Dict, Optional, Set, Tuple
from time import time

from config import (
    TARGET_SIGNALS,
    LOG_DIR,
    LOG_FILE_PATH,
    DBC_FILE_PATH,
    TABLE_UPDATE_INTERVAL,
    NUM_SENSORS,
)

console = Console()

# Work with a per-run copy of target signals to avoid mutating config globals
filtered_signals: Dict[str, Any] = TARGET_SIGNALS.copy()

# Set up logger to write decoded signals to ../logs/run_logs.txt
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE_PATH,
    filemode="a",
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("decoded_signals")


def _render_table(all_signal_names: Set[str], latest_values: Dict[str, Any]) -> None:
    """Render a table of known signals and their latest values."""
    if not all_signal_names:
        return
    table = Table(title="Filtered Distance Values")
    table.add_column("Signal", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    for signal_name in sorted(all_signal_names):
        value = latest_values.get(signal_name, "N/A")
        table.add_row(str(signal_name), str(value))
    console.clear()
    console.print(table)


def _normalize_for_visualizer(
    values: Dict[str, Any], num_sensors: int
) -> Dict[str, Any]:
    """
    Build a dict with keys expected by Visualizer:
    sens00..sens{num_sensors-1}De1FilteredDistance.

    Accepts either 1-based (sens01..sens08) or 0-based (sens00..sens07) inputs.
    Falls back to 0 for missing values and maps "Dist1" to sensor 0 if present.
    """
    normalized: Dict[str, Any] = {}
    for i in range(num_sensors):
        zero_based_key = f"sens{str(i).zfill(2)}De1FilteredDistance"
        one_based_key = f"sens{str(i + 1).zfill(2)}De1FilteredDistance"
        if zero_based_key in values:
            normalized[zero_based_key] = values[zero_based_key]
        elif one_based_key in values:
            normalized[zero_based_key] = values[one_based_key]
        else:
            normalized[zero_based_key] = 0

    # Optionally map Dist1 to sens00 if sens00 has no explicit value
    if num_sensors > 0:
        k0 = f"sens00De1FilteredDistance"
        if (k0 not in values or values.get(k0, 0) in (0, -1)) and ("Dist1" in values):
            normalized[k0] = values["Dist1"]

    return normalized


def main() -> None:
    reader = CANReader()
    decoder = DBCDecoder(DBC_FILE_PATH)
    vis = Visualizer(num_sensors=NUM_SENSORS)

    # Track known signal names and last non -1 values for display
    all_signal_names: Set[str] = set()
    latest_values: Dict[str, Any] = {}

    try:
        last_table_update: float = 0.0
        update_interval: float = TABLE_UPDATE_INTERVAL

        while True:
            frame: Optional[Tuple[int, bytes]] = reader.read_message()
            if not frame:
                continue

            can_id, data = frame
            decoded = decoder.decode(can_id, data)
            if not decoded:
                continue

            logger.info("Decoded signals: %s", decoded)

            updated: bool = False
            for key in TARGET_SIGNALS:
                if key in decoded:
                    filtered_signals[key] = decoded[key]
                    updated = True

            for key, value in filtered_signals.items():
                if value != -1:
                    all_signal_names.add(key)
                    latest_values[key] = value

            now = time()
            if all_signal_names and (now - last_table_update) >= update_interval:
                _render_table(all_signal_names, latest_values)
                last_table_update = now

            if updated:
                vis_values = _normalize_for_visualizer(filtered_signals, NUM_SENSORS)
                vis.update(vis_values)
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        try:
            reader.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
