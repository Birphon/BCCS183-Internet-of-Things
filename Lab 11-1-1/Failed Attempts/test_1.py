from realhttp import *
from time import *

def get_contacts( context, request, reply ):
	print(  "gc: " + request.url() + " @ " + request.ip() )
	reply.setContent("contacts...")
	reply.setStatus(200)
	reply.end()

def get_login( context, request, reply ):
	print(  "Get_Login: " + request.url() + " @ " + request.ip() )
	reply.sendFile('index.html')
	reply.setStatus(200)
	reply.end()
		
def post_login( context, request, reply ):
	print(  "Post_Login: " + request.url() + " @ " + request.ip() )
	reply.setContent("posted data ...")
	print(request.body)
	reply.setStatus(200)
	reply.end()
		
def post_data( context, request, reply ):
	print(  "pd: " + request.url() + " @ " + request.ip() )
	reply.setContent("posted data ...")
	reply.setStatus(200)
	reply.end()
	
def get_services( context, request, reply ):
	print(  "rs: " + request.url() + " @ " + request.ip() )
	reply.setContent("services...")
	reply.setStatus(200)
	reply.end()
	
def default_posts( context, request, reply ):
	print(  "dp: " + request.url() + " @ " + request.ip() )
	reply.setContent("posted content ignored...")
	reply.setStatus(200)
	reply.end()
	
def default_gets( context, request, reply ):
	print(  "dg: " + request.url() + " @ " + request.ip() )
	url = request.url()
	if '/' in url and '.' in url:
		reply.sendFile(url)			
	else:
		reply.sendNotFound();

def main():
	server = RealHTTPServer()
	print( "Server started: %s"%( server.start(8765) ) )
	print( "Server listening: %s"%( server.isListening() ) )
	server.route("/login", ["GET"], get_login)
	server.route("/login", ["POST"], get_login)
	server.route("/contacts/*", ["GET"], get_contacts)
	server.route("/services/*", ["GET"], get_services)
	server.route("/data/*", ["POST"], post_data)
	server.route("*", ["POST"], default_posts)
	server.route("*", ["GET"], default_gets)

	# don't let it finish
	while True:
		sleep(3600)

if __name__ == "__main__":
	main()
