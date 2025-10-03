from can_reader import CANReader
from dbc_decoder import DBCDecoder
from visualizer import Visualizer


from rich.console import Console
from rich.text import Text


def main():
    reader = CANReader()
    decoder = DBCDecoder("../dbc/OX-004282_BEG_USS_COTS_V2_CAN_Matrix_external.dbc")

    vis = Visualizer(num_sensors=8)
    console = Console()

    try:
        while True:
            frame = reader.read_message()
            if frame:
                can_id, data = frame
                # Print the raw CAN message in green
                msg_text = Text(
                    f"Received CAN ID: 0x{can_id:X}, Data: {data}", style="green"
                )
                console.print(msg_text)
                decoded = decoder.decode(can_id, data)
                if decoded:
                    # Print the decoded message in cyan
                    decoded_text = Text(f"Decoded: {decoded}", style="cyan")
                    console.print(decoded_text)
                    # Assuming DBC has signals like USS_Sensor1, USS_Sensor2, ...
                    sensor_values = {k: v for k, v in decoded.items() if "Sensor" in k}
                    if sensor_values:
                        vis.update(sensor_values)
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        reader.close()


if __name__ == "__main__":
    main()
