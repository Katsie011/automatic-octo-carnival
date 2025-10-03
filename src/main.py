from can_reader import CANReader
from dbc_decoder import DBCDecoder
from visualizer import Visualizer

from rich.console import Console
from rich.table import Table

import logging
import os

console = Console()

"""
Filtered distance signals
Response is slow, about 1-2 seconds. But does change as expected when tested with a checkerboard. 
"""
TARGET_SIGNALS = {f"sens{str(i).zfill(2)}De1FilteredDistance": -1 for i in range(1, 9)}
# TARGET_SIGNALS = {f"sens{str(i).zfill(2)}De1Distance": -1 for i in range(0, 13)} # unfiltered is quite noisy

TARGET_SIGNALS["Dist1"] = (
    -1
)  # don't know why this is named differently in the DBC but it seems to correspond to sens01De1Distance
filtered_signals = TARGET_SIGNALS

# Set up logger to write decoded signals to ../logs/run_logs.txt
log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../logs"))
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "run_logs.txt")
logging.basicConfig(
    filename=log_file,
    filemode="a",
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("decoded_signals")


def main():
    reader = CANReader()
    decoder = DBCDecoder(
        "../dbc/OX-004282_BEG_USS_COTS_V2_CAN_Matrix_external.dbc"
    )  # TODO: Replace hardcoded path.
    vis = Visualizer(num_sensors=8)

    import time

    # Keep track of all possible sens0XDe1FilteredDistance signals seen so far
    all_signals = set()
    signal_values = {}

    try:
        last_table_update = 0
        update_interval = 0.2  # 200ms

        while True:
            frame = reader.read_message()
            if frame:
                can_id, data = frame
                decoded = decoder.decode(can_id, data)
                if decoded:
                    # Log the decoded signals to the log file
                    logger.info(f"Decoded signals: {decoded}")

                    # Collect all sens0XDe1FilteredDistance values
                    # Filter signals using the names in TARGET_SIGNALS
                    # Update filtered_signals in-place with any new values from decoded
                    updated = False
                    for k in TARGET_SIGNALS:
                        if k in decoded:
                            filtered_signals[k] = decoded[k]
                            updated = True

                    # Update the set of all signals and their latest values
                    for k, v in filtered_signals.items():
                        if v != -1:
                            all_signals.add(k)
                            signal_values[k] = v

                    # Only update and print the table if we have any signals
                    now = time.time()
                    if all_signals and (now - last_table_update) >= update_interval:
                        # Re-create the table each time to avoid IndexError
                        table = Table(title="Filtered Distance Values")
                        table.add_column("Signal", style="cyan", no_wrap=True)
                        table.add_column("Value", style="magenta")
                        # Add rows for all known signals, sorted
                        for k in sorted(all_signals):
                            v = signal_values.get(k, "N/A")
                            table.add_row(str(k), str(v))
                        # Only print the table if there are rows to display
                        num_rows = len(all_signals)
                        print(f"table.rows={num_rows}")
                        if num_rows > 0:
                            console.clear()
                            console.print(table)
                        last_table_update = now

                    # Use the filtered_signals dict for the sensor values
                    # Only update the visualizer if any values have changed
                    if updated:
                        console.print("Filtered signals are:", filtered_signals)
                        vis.update(filtered_signals)
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        reader.close()


if __name__ == "__main__":
    main()
