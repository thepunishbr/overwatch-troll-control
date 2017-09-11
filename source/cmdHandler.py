import configparser
import subprocess
import os
import ctypes

CONFIG_FILE_PATH = "../config.txt"

class CmdHandler(object):
	"""docstring for CmdHandler"""

	def __init__(self):

		try:
			self.isAdmin = os.getuid() == 0
		except AttributeError:
			self.isAdmin = ctypes.windll.shell32.IsUserAnAdmin() != 0

		if not self.isAdmin:
			print("[Error] Run this program with admin rights. This is needed to access the 'netsh' tool.")

		self.valid_config = False
		self.on_off = False

		self.ow_path = ""
		self.rulename = ""
		self.ips = []


		self.loadConfig()

	def testOwExe(self):
		pass

	def loadConfig(self):

		cparser = configparser.ConfigParser()

		try :
			with open(CONFIG_FILE_PATH) as file:
				cparser.read(CONFIG_FILE_PATH)
				
				config = cparser._sections
				
				self.rulename = cparser.get("DEV", "firewall_rule_name")
				self.ips = cparser.get("DEV", "black_list_ips").split(",")
				map(int, self.ips)
				
				self.ow_path = cparser.get("USER", "overwatch_path")

				self.valid_config = True

		except IOError:
			raise ValueError('file "' + CONFIG_FILE_PATH + '" not found') from IOError

	def firewallON(self):
		if self.isAdmin:
			self.on_off = True
			self.execNetsh(self.resultString(self.on_off))
			return True

		return False

	def firewallOFF(self):
		if self.on_off:
			self.on_off = False
			self.execNetsh(self.resultString(self.on_off))
			return True

		return False

	def execNetsh(self, cmd):
		# os.system(cmd)

		output = subprocess.check_output(cmd, shell=True)
		
		print("[CMD] ", output)

	def resultString(self, on_off):
		on = self.netshString(on_off) + self.rulenameString() + self.actionString() + self.owpathString() + self.ipString()
		off = self.netshString(on_off) + self.rulenameString()

		return on if on_off else off

	def netshString(self, on_off):
		return 'netsh advfirewall firewall add rule ' if on_off else 'netsh advfirewall firewall delete rule '

	def ipString(self):
		string = 'remoteip='
		for num in self.ips:
			string = string + num + '.0.0.0-' + num + '.255.255.255,'

		string = string[:-1] + ' '

		return string

	def rulenameString(self):
		return 'name="' + self.rulename + '" '

	def actionString(self):
		return 'dir=out action=block '

	def owpathString(self):
		return 'program="' + self.ow_path + '" enable=yes '


		