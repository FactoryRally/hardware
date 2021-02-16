import os
import requests

ADDRESS_RANGE = list(range(1, 256))
ACCEPTABLE_RESPONSE_CODES = [200  # Success
	, 301  # Permanent redirect
	, 302  # Temporary redirect
	, 304  # Not modified
	, 403  # Forbidden
	, 404]  # Page not found


def get_current_ip():
	"""

	:return:
	"""
	ip = '192.168.0.137'
	print(ip)
	return ip


def ping_ip(ip):
	"""

	:param ip:
	:return:
	"""
	print("PING IP")
	return os.system('ping -c1 -W1 ' + ip + ' >/dev/null') == 0


def get_neighbor_ips(ip):
	""" Get all neighbor IP's for given IP """
	print("HERE NEIGHTBOR IP")
	ips = []
	if ip.count('.') == 3:
		base = ip[0:ip.rfind('.') + 1]
		for extension in ADDRESS_RANGE:
			neighbor = base + str(extension)
			# exclude currnt ip
			if neighbor != ip:
				ips.append(neighbor)
	return ips


def check_address(url, port, timeout=0):
	"""
	makes a http request to given url:port
	and returns status: True/False and message: 'OK'/'Connection refused'
	"""
	print("CHECK ADDRESS")
	try:
		h = requests.get(f"http://{url}:{port}")
		r = h.status_code
		return True
	except Exception as e:
		print(e.__str__())
	return False


def scan_ports(url, ports):
	""" Verify if url is responding to http requests on given ports """
	print("SCAN PORTS")
	messages = []
	status = check_address(url, '5050')
	if status:
		messages.append(url)
	return messages


def scan(ips=None, ports='5050'):
	""" Verify if urls are responding to http requests on given ports """
	print("SCAN ")
	if not ips:
		local_ip = get_current_ip()
		ips = get_neighbor_ips(local_ip)
	messages = []
	for ip in ips:
		if ping_ip(ip):
			messages.extend(scan_ports(ip, ports))
	if len(messages) > 0:
		for message in messages:
			print(message)
	else:
		print('No neighbors found.')


if __name__ == '__main__':
	scan()
