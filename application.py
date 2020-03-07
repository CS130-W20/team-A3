# Run a test server.
#from app import application
from __init__ import application
import sys 
if __name__ == '__main__':
	if len(sys.argv) == 2 and sys.argv[1] == "test":
		exit(0)
	application.run(host='0.0.0.0', port=8080, debug=True)
