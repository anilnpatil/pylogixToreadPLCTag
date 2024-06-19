# from flask import Flask, request
# app = Flask(__name__)

# @app.route('/insertDataToPlc', methods=['POST'])
# def insert_data_to_plc():
#     data_list = request.json
#     for entry in data_list:
#         print(entry)
#     return 'Data received successfully', 200

# if __name__ == '__main__':
#     app.run(debug=True, port=8083)
from flask import Flask, request
app = Flask(__name__)

@app.route('/insertDataToPlc', methods=['POST'])
def insert_data_to_plc():
    data_list = request.json
    # print(data_list,type(data_list))
    for entry in data_list:
        print(entry,type(entry))

if __name__ == '__main__':
    app.run(debug=True, port=8083)