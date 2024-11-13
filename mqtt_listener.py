import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        # Example of reading an environment variable
        mqtt_host = os.environ.get('MQTT_HOST')
        if not mqtt_host:
            logging.error('MQTT_HOST environment variable not set')
            return 1

        # Add more of your script logic here
        logging.info('MQTT Host: %s', mqtt_host)

        # Simulate some work
        logging.info('Starting MQTT listener...')
        # Your MQTT listener code here

        logging.info('MQTT listener started successfully')
        return 0

    except Exception as e:
        logging.exception('An error occurred: %s', e)
        return 1

if __name__ == '__main__':
    exit(main())