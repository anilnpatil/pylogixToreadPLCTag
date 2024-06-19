from pycomm.ab_comm.clx import Driver as ClxDriver
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from time import sleep

app = Flask(__name__)
CORS(app)

# Create a ClxDriver instance
c = ClxDriver()
is_connected = False  # Flag to track connection status

@app.route('/insertDataToPlc', methods=['POST'])
@cross_origin()
def insert_data_to_plc():
    global is_connected  # Access the global flag

    try:
        if not is_connected:  # Check if connection needs to be established
            c.open('192.168.12.5')  # Open connection to the PLC (only once)
            print("Connection to PLC established.")
            is_connected = True

        c.forward_open()  # Initialize the session

        # Get the JSON data from the request
        data_list = request.json

        # Iterate through the data and process it
        for item in data_list:
            for key, value in item.items():
                # Convert value to string regardless of its type
                str_value = str(value)
                
                print("Writing to PLC: Key: {}, Value: {}".format(type(key), type(str_value)))
                
                # Write string value to PLC
                key = key.encode('utf-8')
                str_value = str_value.encode('utf-8')
                try:
                    c.write_string(key, str_value)
                    print("Read String Value is", c.read_string(key))
                    print("Data written to PLC successfully for key: {}".format(key.decode('utf-8')))
                except Exception as e:
                    print("Error writing string {}: {}".format(key.decode('utf-8'), e))
                sleep(1)

        return jsonify({"message": "Data written to PLC successfully.", "error": None}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error occurred while writing data to PLC.", "error": str(e)}), 500
    finally:
        if is_connected:
            c.close()
            is_connected = False
            print("Connection to PLC closed.")

@app.route('/readDataFromPlc', methods=['POST'])
@cross_origin()
def read_data_from_plc():
    global is_connected  # Access the global flag

    try:
        if not is_connected:  # Check if connection needs to be established
            c.open('10.60.85.21')  # Open connection to the PLC (only once)
            print("Connection to PLC established.")
            is_connected = True

        c.forward_open()  # Initialize the session

        # Get the JSON data from the request
        tags = request.json

        # Dictionary to store the read values
        read_values = {}

        # Iterate through the tags and read their values from the PLC
        for tag in tags:
            try:
                read_value = c.read_tag(tag)
                read_values[tag] = read_value
                print("Read from PLC: Tag: {}, Value: {}".format(tag, read_value))
            except Exception as e:
                print("Error reading tag {}: {}".format(tag, e))
                read_values[tag] = "Error: {}".format(e)

        return jsonify({"message": "Data read from PLC successfully.", "data": read_values, "error": None}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error occurred while reading data from PLC.", "error": str(e)}), 500
    finally:
        if is_connected:
            c.close()
            is_connected = False
            print("Connection to PLC closed.")

@app.route('/listTags', methods=['GET'])
@cross_origin()
def list_tags():
    global is_connected  # Access the global flag

    try:
        if not is_connected:  # Check if connection needs to be established
            c.open('192.168.12.5')  # Open connection to the PLC (only once)
            print("Connection to PLC established.")
            is_connected = True

        c.forward_open()  # Initialize the session

        # Fetch the list of tags from the PLC
        try:
            tags = c.get_tag_list()
            # If tags are bytes, convert them to a list of strings in a readable format
            if isinstance(tags, bytes):
                tags = tags.decode('latin1')  # Using 'latin1' to avoid UTF-8 errors
            return jsonify({"message": "Tags retrieved successfully.", "tags": tags, "error": None}), 200
        except Exception as e:
            print("Error retrieving tags:", e)
            return jsonify({"message": "Error occurred while retrieving tags from PLC.", "error": str(e)}), 500

    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error occurred while connecting to PLC.", "error": str(e)}), 500
    finally:
        if is_connected:
            c.close()
            is_connected = False
            print("Connection to PLC closed.")

@app.route('/closeConnection', methods=['GET'])
def close_connection():
    global is_connected
    if is_connected:
        c.close()
        is_connected = False
        print("Connection to PLC closed.")
    return jsonify({"message": "Connection to PLC closed successfully.", "error": None}), 200

if __name__ == '__main__':
    app.run(debug=True, port=8083)
