import subprocess

def return_all_wifi_connections():
    """
    This function returns all currently available wifi access points.
    :return: list with all wifi SSIDs
    """
    result = subprocess.run(['nmcli', "d", "wifi", "list"], stdout=subprocess.PIPE)
    scan_out_lines = str(result).split("\\n")[1:-1]
    scan_out_data = {}
    for each_line in scan_out_lines:
        split_line = [e for e in each_line.split(" ") if e != ""]
        line_data = {"SSID": split_line[0], "RSSI": int(split_line[2]),
                     "HT": (split_line[4] == "Y"), "CC": split_line[5]}
        scan_out_data[split_line[1]] = line_data
    ssid_list = []
    for key in scan_out_data.keys():
        ssid_list.append(scan_out_data.get(key).get('SSID'))
    return ssid_list


def connect_to_wlan(ssid, password):
    """
    This functions connects to a network.
    :param ssid: the SSID of the network
    :param password: the WPA passphrase of the given network
    :return: result of the command, e.g. if connection was successful
    """
    result = subprocess.run(['nmcli', "d", "wifi", "connect", ssid, "password", password], stdout=subprocess.PIPE).returncode
    print(result)
    return evaluate_result(result)


def evaluate_result(result):
    """
    This function evaluates whether the connection to a network was a success or failure.
    :param result: the output of the
    :return:
    """
    if not result == 0:
        if result == 10:
            return False, "No Network with that SSID exists."
        if result == 8:
            return False, "NetworkManager not running!"
        if result == 2:
            return False, "Invalid user input!"
        if result in (1, 3, 4, 5, 6):
            return False, "Something went wrong!"
    else:
        return True, "Connection established!"







