import os
from dotenv import load_dotenv
from mobile_app import create_app

# Load environment variables from .env file
load_dotenv()

if __name__ == '__main__':
    # Set the WSGI application object on the application module
    app = create_app()

    # Get the port number from the environment variable or use the default port 5000
    port = int(os.getenv('PORT', 5000))

    # Start the development server
    app.run(host='0.0.0.0', port=port)