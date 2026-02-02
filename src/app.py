"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)
jackson_family = FamilyStructure("Jackson")

John = {
    "first_name": "John",
    "age": 33,
    "lucky_numbers": [7, 13, 22]
}

Jane = {
    "first_name": "Jane",
    "age": 35,
    "lucky_numbers": [10, 14, 3]
}

Jimmy = {
    "first_name": "Jimmy",
    "age": 5,
    "lucky_numbers": [1]
}

jackson_family.add_member(John)
jackson_family.add_member(Jane)
jackson_family.add_member(Jimmy)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/members/<int:member_id>', methods=['GET'])
def get_single_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if member:
            return jsonify(member), 200
        else:
            return jsonify({"error": "Member not found"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/members', methods=['POST'])
def create_member():
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        member_data = request.get_json()
        
        required_fields = ["first_name", "age", "lucky_numbers"]
        for field in required_fields:
            if field not in member_data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        if not isinstance(member_data["first_name"], str):
            return jsonify({"error": "first_name must be a string"}), 400
        if not isinstance(member_data["age"], int):
            return jsonify({"error": "age must be an integer"}), 400
        if not isinstance(member_data["lucky_numbers"], list):
            return jsonify({"error": "lucky_numbers must be a list"}), 400
        if "id" in member_data and not isinstance(member_data["id"], int):
            return jsonify({"error": "id must be an integer"}), 400
        
        result = jackson_family.add_member(member_data)
        
        if result:
            return jsonify(result), 200
        else:
            return jsonify({"error": "Failed to add member"}), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_single_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if not member:
            return jsonify({"error": "Member not found"}), 400
        jackson_family.delete_member(member_id)
        return jsonify({"done": True}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)