import subprocess

failure = "Fehler"


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
        line_data = {"SSID": split_line[0], "RSSI": int(split_line[2]), "channel": split_line[3],
                     "HT": (split_line[4] == "Y"), "CC": split_line[5], "security": split_line[6]}
        scan_out_data[split_line[1]] = line_data
    list = []
    for key in scan_out_data.keys():
        list.append(scan_out_data.get(key).get('SSID'))
    return list


def connect_to_wlan(ssid, password):
    """
    This functions connects to a network.
    :param ssid: the SSID of the network
    :param password: the WPA passphrase of the given network
    :return: result of the command, e.g. if connection was successful
    """
    result = subprocess.run(['nmcli', "d", "wifi", "connect", ssid, "password", str(password)], stdout=subprocess.PIPE)
    return evaluate_result(result.stdout.decode('utf-8'))


def evaluate_result(result):
    """
    This function evaluates whether the connection to a network was a success or failure.
    :param result:
    :return:
    """
    if result.__contains__(failure):
        if result.__contains__("Not authorized to control networking."):
            return False, "Wrong Password entered"
        if result.__contains__("Es wurde kein Netzwerk mit SSID"):
            return False, "No Network with that SSID exists."
        return False, "Error"
    else:
        return True






