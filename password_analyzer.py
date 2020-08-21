import utils
import config
from file_handler import FileHandler, make_file_name


def get_max_overlapping_keystrokes(packet):
    keyboard_state = (packet[5], packet[6])
    keyboard_state_eval = utils.try_eval_tuple(keyboard_state)
    overlapping_count = 0

    # structure: i;delta;sniff-intervals;modifier-scan-code;keys-scan-code;modifier;keys
    if keyboard_state_eval[0] != '':
        overlapping_count += 1

    for key in keyboard_state_eval[1]:
        if key != '':
            overlapping_count += 1

    return overlapping_count


class PasswordAnalyzer:

    def __init__(self):
        self.packet_list = []
        self.other_packet_lists = {}
        self.password = ""
        self.password_data = []
        self.observation_sequence = []
        self.used_password_id = -1
        self.max_overlapping_keystrokes = -1
        self.bluetooth_packet_count = 0

    def read_packet_list(self, handler):
        self.packet_list = handler.read_csv_to_list()

        del self.packet_list[0]
        self.bluetooth_packet_count += len(self.packet_list)

    def read_other_packet_lists(self, user_id, with_shift=False):
        handler = FileHandler()
        for password in config.passwords:
            str_password = str(password)
            if str_password == self.password:
                continue

            file_name = make_file_name(user_id, 4, str_password)
            handler.make_training_read_path_and_file(file_name, user_id, 4, str_password)
            packet_list = handler.read_csv_to_list()
            del packet_list[0]
            self.bluetooth_packet_count += len(packet_list)
            self.other_packet_lists[str_password] = packet_list

        if with_shift:
            for password in config.shift_passwords:
                str_password = str(password)
                if str_password == self.password:
                    continue

                file_name = make_file_name(user_id, 4, str_password)
                handler.make_training_read_path_and_file(file_name, user_id, 4, str_password)
                packet_list = handler.read_csv_to_list()
                del packet_list[0]
                self.bluetooth_packet_count += len(packet_list)
                self.other_packet_lists[str_password] = packet_list

        for password in config.random_passwords:
            str_password = str(password)
            if str_password == self.password:
                continue

            file_name = make_file_name(user_id, 5, str_password)
            handler.make_training_read_path_and_file(file_name, user_id, 5, str_password)
            packet_list = handler.read_csv_to_list()
            del packet_list[0]
            self.bluetooth_packet_count += len(packet_list)
            self.other_packet_lists[str_password] = packet_list

        if with_shift:
            for password in config.random_shift_passwords:
                str_password = str(password)
                if str_password == self.password:
                    continue

                file_name = make_file_name(user_id, 5, str_password)
                handler.make_training_read_path_and_file(file_name, user_id, 5, str_password)
                packet_list = handler.read_csv_to_list()
                del packet_list[0]
                self.bluetooth_packet_count += len(packet_list)
                self.other_packet_lists[str_password] = packet_list

    def set_password(self, password):
        self.password = str(password)

    def clear(self):
        self.password_data = []
        self.observation_sequence = []
        self.used_password_id = -1
        self.max_overlapping_keystrokes = -1

    def set_password_id(self, password_id):
        if int(password_id) != self.used_password_id:
            self.clear()
            self.used_password_id = int(password_id)

    def read_password_data(self, password_id=-1):
        if password_id != -1:
            self.set_password_id(password_id)

        i = 0
        for packet in self.packet_list:
            if self.used_password_id != int(packet[0]):
                continue
            self.password_data.append(packet)
            if i != int(packet[0]):
                i = int(packet[0])
            else:
                self.observation_sequence.append(packet[2])

    def calculate_max_overlapping_keystrokes(self, password_id=-1):
        if password_id != -1:
            self.set_password_id(password_id)

        for packet in self.packet_list:
            if self.used_password_id == int(packet[0]):
                continue

            overlapping_count = get_max_overlapping_keystrokes(packet)

            if overlapping_count > self.max_overlapping_keystrokes:
                self.max_overlapping_keystrokes = overlapping_count

        for password in self.other_packet_lists:
            for packet in self.other_packet_lists[password]:
                overlapping_count = get_max_overlapping_keystrokes(packet)

                if overlapping_count > self.max_overlapping_keystrokes:
                    self.max_overlapping_keystrokes = overlapping_count
