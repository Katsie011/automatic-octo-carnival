import matplotlib.pyplot as plt
from config import NUM_SENSORS, VIS_Y_MIN_CM, VIS_Y_MAX_CM, Y_LABEL


class Visualizer:
    def __init__(self, num_sensors=NUM_SENSORS):
        self.num_sensors = num_sensors
        self.values = [0] * num_sensors

        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.bars = self.ax.bar(range(num_sensors), self.values)
        self.ax.set_ylim(VIS_Y_MIN_CM, VIS_Y_MAX_CM)  # cm (5.5m = 550cm)
        self.ax.set_xticks(range(num_sensors))
        self.ax.set_xticklabels([f"S{i+1}" for i in range(num_sensors)])
        self.ax.set_ylabel(Y_LABEL)
        # Initialize text labels above bars
        self.texts = []
        for bar in self.bars:
            height = bar.get_height()
            txt = self.ax.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"{int(height)}",
                ha="center",
                va="bottom",
                fontsize=9,
                color="black",
            )
            self.texts.append(txt)

    def update(self, sensor_values):
        # sensor_values is a dict {sensor_1: val_cm, ...}
        # To avoid IndexError, only update up to self.num_sensors bars
        # and map the correct sensor values to each bar.
        # We expect keys like 'sens00De1FilteredDistance', ..., 'sens07De1FilteredDistance'
        # Map them to bar indices 0..num_sensors-1

        for i in range(self.num_sensors):
            key = f"sens{str(i).zfill(2)}De1FilteredDistance"
            val = sensor_values.get(key, 0)
            # If value is -1, treat as 0 (no detection)
            display_val = val if val != -1 else 0
            self.bars[i].set_height(display_val)
            # Update the text label above the bar
            self.texts[i].set_y(display_val + 5)  # 5 units above bar for visibility
            self.texts[i].set_text(f"{display_val}")

        plt.pause(0.001)
