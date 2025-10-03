import os

# Sensors and signals
NUM_SENSORS = 8


"""
Filtered distance signals
Response is slow, about 1-2 seconds. But does change as expected when tested with a checkerboard. 
"""
TARGET_SIGNALS = {
    f"sens{str(i).zfill(2)}De1FilteredDistance": -1 for i in range(1, 9)
}  # use unfiltered for better response.
# TODO this is currently unused and needs to be fully centralised
# Additional signals that seem to be from the first sensor
TARGET_SIGNALS["Dist1"] = -1

# Paths
_BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DBC_FILE_PATH = os.path.abspath(
    os.path.join(_BASE_DIR, "../dbc/OX-004282_BEG_USS_COTS_V2_CAN_Matrix_external.dbc")
)
LOG_DIR = os.path.abspath(os.path.join(_BASE_DIR, "../logs"))
LOG_FILE_NAME = "run_logs.txt"
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE_NAME)

# Timings
TABLE_UPDATE_INTERVAL = 0.2  # seconds

# Visualization
VIS_Y_MIN_CM = 0
VIS_Y_MAX_CM = 550
Y_LABEL = "Distance [cm]"
