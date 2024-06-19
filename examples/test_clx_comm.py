from pycomm.ab_comm.clx import Driver as ClxDriver
import logging

from time import sleep


if __name__ == '__main__':

    logging.basicConfig(
        filename="ClxDriver.log",
        format="%(levelname)-10s %(asctime)s %(message)s",
        level=logging.DEBUG
    )
    c = ClxDriver()

    print( c['port'])
    print( c.__version__)


    if c.open('192.168.12.5'):
        while 1:
            try:
                # print(c.read_tag(['ControlWord']))
                # print(c.read_tag(['parts', 'ControlWord', 'Counts']))

                from flask import Flask, request
                app = Flask(__name__)

                @app.route('/insertDataToPlc', methods=['POST'])
                def insert_data_to_plc():
                    data_list = request.json
                    for item in data_list:
                        # Iterate over each key-value pair in the dictionary
                        for key, value in item.items():
                            # Check the type of the value
                            value_type = type(value)
                        #   print(f"Key: {key}, Value: {value}, Type: {value_type}")
                            # if isinstance(value_type,'str'):
                            if value_type is str:
                                value_type  = 'STRING'
                                print("if condition")
                                print(value_type)
                            elif value_type is float:
                                value_type='REAL'
                                # value_type = 'STRING'
                                print(value_type)
                            print(c.write_tag(key,value,value_type))
                    # print(data_list,type(data_list))
                    # for entry in data_list:
                    #     print(entry,type(entry))
                    #     print(c.write_tag(entry))

                    # return 'Data received successfully', 200


                
                # print(c.write_tag('caseGtinText', 1121, 'INT'))
                # print(c.write_tag(('bag_value', 12, 'DINT')))
                # print(c.write_tag(('Result', 23, 'INT')))
                # print(c.write_tag([('Result', 1996, 'INT')]))
                # print(c.write_tag([('Counts', -26, 'INT'), ('ControlWord', -30, 'DINT'), ('parts', 31, 'DINT')]))
                sleep(1)
            except Exception as e:
                c.close()
                print(e)
                pass

        # To read an array
        r_array = c.read_array("TotalCount", 1750)
        for tag in r_array:
            print (tag)

        c.close()
