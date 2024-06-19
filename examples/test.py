# from pycomm.ab_comm.clx import Driver as ClxDriver
# import logging
# from time import sleep
# from flask import Flask, request

# app = Flask(__name__)

# # Create a ClxDriver instance
# c = ClxDriver()

# # Configure logging
# logging.basicConfig(
#     filename="ClxDriver.log",
#     format="%(levelname)-10s %(asctime)s %(message)s",
#     level=logging.DEBUG
# )

# # Open connection to the PLC
# if c.open('192.168.12.5'):
#     print("Connection to PLC established.")

# @app.route('/insertDataToPlc', methods=['POST'])
# def insert_data_to_plc():
#     try:
#         data_list = request.json
#         for item in data_list:
#             for key, value in item.items():
#                 # Check the type of the value
#                 value_type = type(value)
                
#                 if isinstance(value, str):
#                     value_type = 'STRING'
#                 elif isinstance(value, float):
#                     value_type = 'REAL'
#                 else:
#                     value_type = 'INT'  # Assuming it's an integer if not string or float
                
#                 # print(f"Writing tag: {key}, Value: {value}, Type: {value_type}")
#                 c.write_tag(key, value, value_type)
        
#         return "Data written to PLC successfully.", 200
#     except Exception as e:
#         print(e)
#         return "Error occurred while writing data to PLC.", 500

# # Close the connection to the PLC
# @app.route('/closeConnection', methods=['GET'])
# def close_connection():
#     c.close()
#     return "Connection to PLC closed successfully.", 200

# if __name__ == '_main_':
#     app.run(debug=True)
from builtins import Exception, float, isinstance, print, str, type
from pycomm.ab_comm.clx import Driver as ClxDriver
import logging
from time import sleep
from flask import Flask, request
app = Flask(__name__)

# Create a ClxDriver instance
c = ClxDriver()

# Configure logging
logging.basicConfig(
    filename="ClxDriver.log",
    format="%(levelname)-10s %(asctime)s %(message)s",
    level=logging.DEBUG
)

# Open connection to the PLC
if c.open('192.168.12.5'):
    print("Connection to PLC established.")

@app.route('/insertDataToPlc', methods=['POST'])
def insert_data_to_plc():
    try:
        data_list = request.json
        for item in data_list:
            for key, value in item.items():
                # Check the type of the value
                value_type = type(value)
                
                if isinstance(value, str):
                    value_type = 'STRING'
                    # Encode the string using ASCII encoding with error handling
                    value = value.encode('ascii', errors='ignore')
                elif isinstance(value, float):
                    value_type = 'REAL'
                else:
                    value_type = 'INT'  # Assuming it's an integer if not string or float
                
                # print(f"Writing tag: {key}, Value: {value}, Type: {value_type}")
                c.write_tag(key, value, value_type)
        
        return "Data written to PLC successfully.", 200
    except Exception as e:
        print(e)
        return "Error occurred while writing data to PLC.", 500

# Close the connection to the PLC
@app.route('/closeConnection', methods=['GET'])
def close_connection():
    c.close()
    return "Connection to PLC closed successfully.", 200

if __name__ == '__main__':
    app.run(debug=True, port=8083)