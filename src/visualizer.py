import matplotlib.pyplot as plt


class Visualizer:
    def __init__(self, num_sensors=8):
        self.num_sensors = num_sensors
        self.values = [0] * num_sensors

        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.bars = self.ax.bar(range(num_sensors), self.values)
        self.ax.set_ylim(0, 5000)  # mm (adjust per DBC scaling)
        self.ax.set_xticks(range(num_sensors))
        self.ax.set_xticklabels([f"S{i+1}" for i in range(num_sensors)])
        self.ax.set_ylabel("Distance [mm]")

    def update(self, sensor_values):
        # sensor_values is a dict {sensor_1: val_mm, ...}
        # To avoid IndexError, only update up to self.num_sensors bars
        # and map the correct sensor values to each bar.
        # We expect keys like 'sens00De1FilteredDistance', ..., 'sens07De1FilteredDistance'
        # Map them to bar indices 0..num_sensors-1

        for i in range(self.num_sensors):
            key = f"sens{str(i).zfill(2)}De1FilteredDistance"
            val = sensor_values.get(key, 0)
            self.bars[i].set_height(val if val != -1 else 0)

        plt.pause(0.001)
