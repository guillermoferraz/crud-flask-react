from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost/pythonreactdb'
mongo = PyMongo(app)

CORS(app)


db = mongo.db.users

@app.route('/users', methods=['POST'])
def createUser():
    #print(request.json)
    id = db.insert({
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password']
    })
    print(str(ObjectId(id)))
    #return 'recived'
    return jsonify(str(ObjectId(id)))

@app.route('/users', methods=['GET'])
def getUsers():
    users = []
    for doc in db.find():
        users.append({
            '_id': str(ObjectId(doc['_id'])),
            'name': doc['name'],
            'email': doc['email'],
            'password': doc['password']
        })
    #return 'recived'
    return jsonify(users)

@app.route('/user/<id>', methods=['GET'])
def getUser(id):
    user = db.find_one({'_id': ObjectId(id)})
    #print(id)
    print(user)
    #return 'recived'
    return jsonify({
        '_id': str(ObjectId(user['_id'])),
        'name': user['name'],
        'email': user['email'],
        'password': user['password'],
    })

@app.route('/users/<id>', methods=['DELETE'])
def deleteUser(id):
    #print(id)
    db.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg': 'user deleted'})

@app.route('/users/<id>', methods=['PUT'])
def upadteUser(id):
    #print(id)
    #print(request.json)
    db.update_one({'_id': ObjectId(id)}, {'$set': {
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password']
    }})
    return jsonify({'msg': 'User updated'})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
