from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

todos = {}


class CoinSeerAPI(Resource):
    def get(self, crypto, model_id):
        return [{model_id: 12346}, {model_id: 12345}, {model_id: 0.122312}]


api.add_resource(CoinSeerAPI, '/<string:crypto>/<string:model_id>')


if __name__ == '__main__':
    app.run(debug=True, port=8000)
