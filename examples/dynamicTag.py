from pylogix import PLC
import logging
from time import sleep
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
CORS(app)

# Create a PLC instance
plc = PLC()
is_connected = False  # Flag to track connection status

@app.route('/insertDataToPlc', methods=['POST'])
@cross_origin()
def insert_data_to_plc():
    global is_connected  # Access the global flag

    try:
        if not is_connected:  # Check if connection needs to be established
            plc.IPAddress = '192.168.12.5'  # Set PLC IP address
            is_connected = True

        # Get the JSON data from the request
        data_list = request.json

        # Collect all the write operations
        write_operations = []
        for item in data_list:
            for key, value in item.items():
                write_operations.append((key, value))

        # Perform all write operations
        for key, value in write_operations:
            try:
                plc.Write(key, value)
                print("Data written to PLC successfully for key: {}".format(key))
            except Exception as e:
                print("Error writing value: {}: {}".format(key, e))

        # Extract keys from data_list for the response
        keys = [key for key, _ in write_operations]

        return jsonify({"tags": keys}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error occurred while writing data to PLC.", "error": str(e)}), 500
    finally:
        if is_connected:
            plc.Close()
            is_connected = False
            print("Connection to PLC closed.")

@app.route('/closeConnection', methods=['GET'])
def close_connection():
    global is_connected
    if is_connected:
        plc.Close()
        is_connected = False
        print("Connection to PLC closed.")
    return jsonify({"message": "Connection to PLC closed successfully.", "error": None}), 200

@app.route('/readDataFromPlc', methods=['GET'])
@cross_origin()
def read_data_from_plc():
    global is_connected  # Access the global flag

    try:
        if not is_connected:  # Check if connection needs to be established
            plc.IPAddress = '192.168.12.5'  # Set PLC IP address
            is_connected = True

        # Define the keys you want to read from the PLC
        keys_to_read = [
            "caseGTINBarcode",
            "caseGTINReadable",
            "caseGTINText",
            "caseQty",
            "colorDescription",
            "commentLine1",
            "commentLine2",
            "commentLine3",
            "date",
            "endTime",
            "grossWeightKgs",
            "grossWeightLbs",
            "itemUPC",
            "itemUPCText",
            "labelIdentifier",
            "literalLabelName",
            "literalSONumber",
            "productionCode",
            "registeredTrademark",
            "resourceItemDescription",
            "resourceItemNu",
            "resourceItemNumberBarcode",
            "result",
            "resultDescription",
            "scheduleOlsnRelease",
            "scheduleOlsnReleaseBarcode",
            "sonumber",
            "sonumberBarcode",
            "starTtime"
        ]  # Example keys, you should replace these with actual keys

        data = {}
        for key in keys_to_read:
            try:
                response = plc.Read(key)
                if response.Status == 'Success':
                    data[key] = response.Value
                    print("Read from PLC: Key: {}, Value: {}".format(key, response.Value))
                else:
                    print("Failed to read key: {}, Status: {}".format(key, response.Status))
            except Exception as e:
                print("Error reading value: {}: {}".format(key, e))

        return jsonify({"tags": keys_to_read, "data": data}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error occurred while reading data from PLC.", "error": str(e)}), 500
    finally:
        if is_connected:
            plc.Close()
            is_connected = False
            print("Connection to PLC closed.")

@app.route('/readDataTagsFromPlc', methods=['GET'])
@cross_origin()
def read_data_tags_from_plc():
    global is_connected  # Access the global flag

    try:
        if not is_connected:  # Check if connection needs to be established
            plc.IPAddress = '192.168.12.5'  # Set PLC IP address
            is_connected = True

        # Read all available tags from the PLC
        tags_response = plc.GetTagList()
        if tags_response is None or tags_response.Value is None:
            raise Exception("Failed to get tag list from PLC.")

        tag_names = [tag.TagName for tag in tags_response.Value]

        data = {}
        for tag in tags_response.Value:
            try:
                response = plc.Read(tag.TagName)
                if response.Status == 'Success':
                    data[tag.TagName] = response.Value
                    print("Read from PLC: Key: {}, Value: {}".format(tag.TagName, response.Value))
                else:
                    print("Failed to read tag: {}, Status: {}".format(tag.TagName, response.Status))
            except Exception as e:
                print("Error reading value: {}: {}".format(tag.TagName, e))

        return jsonify({"tags": tag_names, "data": data}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error occurred while reading data from PLC.", "error": str(e)}), 500
    finally:
        if is_connected:
            plc.Close()
            is_connected = False
            print("Connection to PLC closed.")

if __name__ == '__main__':
    app.run(debug=True, port=8083)
