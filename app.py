from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.
    
    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""


@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})


@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)


@app.route("/users")
def users():
    users = db.get("users")
    data = {"users": users}

    team = request.args.get('team')
    if team != None:
        filteredUsers = [i for i in users if i["team"] == team]
        data["users"] =  filteredUsers
    return create_response(data)

@app.route("/users", methods = ['POST'])
def addUser():
    bodyParams = request.json
    if "name" not in bodyParams:
        return create_response(None, 422, "missing name")
    if "age" not in bodyParams:
        return create_response(None, 422, "missing age")
    if "team" not in bodyParams:
        return create_response(None, 422, "missing team")
    
    data = {"newUser": db.create("users", bodyParams)}
    return create_response(data, 201, "new user entered")

@app.route("/users/<id>")
def userById(id):
    user = db.getById("users", int(id) if id.isdigit() else id)
    if user == None:
        return create_response(None, 404, "doesn't exist a user with the provided id")
    data = {"user": user}
    return create_response(data)

@app.route("/users/<id>", methods = ['PUT'])
def updateUserById(id):
    user = db.getById("users", int(id) if id.isdigit() else id)
    if user == None:
        return create_response(None, 404, "doesn't exist a user with the provided id")
    
    bodyParams = request.json
    updateUser = db.updateById("users", int(id) if id.isdigit() else id, bodyParams)
    data = {"updatedUser": updateUser}
    return create_response(data, 201, "user updated")

@app.route("/users/<id>", methods = ['DELETE'])
def deleteUserById(id):
    user = db.getById("users", int(id) if id.isdigit() else id)
    if user == None:
        return create_response(None, 404, "doesn't exist a user with the provided id")
    
    db.deleteById("users", int(id) if id.isdigit() else id)
    return create_response(None, 201, "user deleted successfully")

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(debug=True)
