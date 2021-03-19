import socket
from multiprocessing import Process, Queue
import time

"""
Tools to scan network from python.
Mostly taken from stack overflow and mixed together.
Author: Julian Kolesik <jkolesik at jkolesik@student.tgm.ac.at>
Source: Sammy Pfeiffer <Sammy.Pfeiffer at student.uts.edu.au>
"""

def get_own_ip():
    """
    Get the own IP, even without internet connection.
    From https://stackoverflow.com/a/1267524
    """
    return "192.168.0.132"


class NetworkScanner:
    """
    This class scans the network for a server instance and returns the matching IP address.
    """

    def check_server(self, address, port):
        """
        Check an IP and port for it to be open, store result in queue.
        Based on https://stackoverflow.com/a/32382603
        :param: address: the address to check if a server is running
        :param: port: the port to check if a server is running
        :param: queue: the queue in which the processes are running
        """
        # Create a TCP socket
        s = socket.socket()
        try:
            s.connect((address, port))
            self.q.put((True, address, port))
        except socket.error as e:
            self.q.put((False, address, port))

    def check_subnet_for_open_port(self, subnet, port, timeout=3.0):
        """
        Check the subnet for open port IPs.
        :param subnet: the subnet to check
        :param port: the port to check
        :param timeout: the timeout time for each connection try
        :returns [str]: List of IPs with port open found.
        """
        self.q = Queue()
        self.processes = []
        for i in range(1, 255):
            ip = subnet + '.' + str(i)
            print(ip)
            p = Process(target=self.check_server, args=(ip, port))
            self.processes.append(p)
            p.start()
            print(i)
        # Give a bit of time...
        time.sleep(timeout)

        found_ips = []
        for idx, p in enumerate(self.processes):
            # If not finished in the timeout, kill the process
            if p.exitcode is None:
                p.terminate()
            else:
                # If finished check if the port was open
                open_ip, address, port = self.q.get()
                if open_ip:
                    found_ips.append(address)

        #  Cleanup processes
        for idx, p in enumerate(self.processes):
            p.join()

        return found_ips

    def check_own_subnet_for_open_port(self, port):
        """
        Check our own subnet for open port.
        :param: port: the port to check for in the subnet
        :returns: all ips with open port 5050
        """
        own_ip = get_own_ip()
        print("Got own ip: " + str(own_ip))
        ip_split = own_ip.split('.')
        subnet = ip_split[:-1]
        subnetstr = '.'.join(subnet)
        return self.check_subnet_for_open_port(subnetstr, port)


if __name__ == '__main__':
    network_scanner = NetworkScanner()
    print(network_scanner.check_own_subnet_for_open_port(5050))
