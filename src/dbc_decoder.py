import cantools

class DBCDecoder:
    def __init__(self, dbc_path):
        self.db = cantools.database.load_file(dbc_path)

    def decode(self, can_id, data):
        try:
            msg = self.db.get_message_by_frame_id(can_id)
            if msg:
                decoded = msg.decode(bytes(data))
                return decoded
        except Exception:
            return None
