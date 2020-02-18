# Run a test server.
#from app import application
from __init__ import application
if __name__ == '__main__':
	application.run(host='0.0.0.0', port=8080, debug=False)
