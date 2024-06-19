from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route('/listTags', methods=['GET'])
def list_tags():
    dummy_tags = {
        "tags": ["Tag1", "Tag2", "Tag3", "Tag4", "Tag5","Tag6", "Tag7", "Tag8", "Tag9", "Tag10","Tag11", "Tag12", "Tag13", "Tag14", "Tag15","Tag16", "Tag17", "Tag18", "Tag19", "Tag20","Tag21", "Tag22", "Tag23", "Tag24", "Tag25","Tag1", "Tag2", "Tag3", "Tag4", "Tag5","Tag1", "Tag2", "Tag3", "Tag4", "Tag5","Tag1", "Tag2", "Tag3", "Tag4", "Tag5","Tag1", "Tag2", "Tag3", "Tag4", "Tag5","Tag1", "Tag2", "Tag3", "Tag4", "Tag5"]
    }
    return jsonify(dummy_tags)

if __name__ == '__main__':
    app.run(debug=True, port=8083)

