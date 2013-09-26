# -*- coding: utf-8 -*-
"""
@date 09-26-13
"""
import socket, threading, sys, getopt, time


class Server( threading.Thread ):
	"""
	"""
	def __init__( self, ip, port ):
		threading.Thread.__init__(self)
		self.ip = ip
		self.port = port		
		self.start()

	def run(self):
		tcp = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		tcp.bind( ( self.ip, self.port ) )
		tcp.listen(1)

		conn, client = tcp.accept()
		print 'Connected by ', client

		while True:
			try:
				msg = conn.recv(1024)
				if not msg: break
				print client, msg
			except Exception, e:
				break

		conn.close()
		print "The connection with {0} was closed ".format( client )



class Connect( threading.Thread ):
	"""
	"""
	def __init__( self, ip, port ):
		threading.Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.start()

	def run(self):
		tcp = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

		def connect():
			try:
			   tcp.connect( (self.ip, self.port) )
			except Exception, e:
				print e
				time.sleep(1)
				connect()

		connect()

		msg = raw_input()

		while  msg <> '@close' : #tecla
			tcp.send( msg )
			msg = raw_input()
			sys.stdout.flush()

		tcp.close()




def help():
	print """
--------------------------------------------------------
Help window	

--------------------------------------------------------
"""
	sys.exit()



def main(argv):
	receive = None
	send = None

	try:
		opts, args = getopt.getopt(argv,"ho:c:", ["help", "open=", "connect="])
	except getopt.GetoptError:
		help()

	for opt, arg in opts:

		if opt in ('-h', '--help'):
			#chama a tela de ajuda
			help()

		elif opt in ("-o", "--open"):
			receive = Server( arg[:arg.find(':')], int( arg[arg.find(':')+1:]) )

		elif opt in ("-c", "--connect"):
			send = Connect( arg[:arg.find(':')], int( arg[arg.find(':')+1:]) )

if __name__ == "__main__":
	main(sys.argv[1:])




