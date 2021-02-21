from flask import Flask, request
from flask_restful import Resource, Api
from train import predict_model, get_data

app = Flask(__name__)
api = Api(app)


class CoinSeerAPI(Resource):
    def get(self, crypto, model_id):
        num_days_to_predict = 20 - int(model_id)
        if model_id == "0":
            model_id = ""
        model_file_name = crypto + "_model-" + model_id + ".h5"
        actual_data, predicted_data = predict_model(crypto, model_file_name, num_days_to_predict)
        values = []
        for data in actual_data[:-num_days_to_predict]:
            values.append({"Actual": float(data[0])})

        for i in range(10 - int(model_id)):
            values.append({"Actual": float(actual_data[-num_days_to_predict + i:][0]),
                           "Predicted": float(predicted_data[0, i, 0])})

        for i in range(10):
            values.append({"Predicted": float(predicted_data[0, 10 - int(model_id) + i, 0])})

        # print(values)
        values.reverse()
        return values


class CoinSeerAPIGraph(Resource):
    def get(self, crypto, model_id):
        result = []
        num_days_to_predict = 20 - int(model_id)
        if model_id == "0":
            model_id = ""
        model_file_name = crypto + "_model-" + model_id + ".h5"
        actual_data, predicted_data = predict_model(crypto, model_file_name, num_days_to_predict)
        values = []

        for i in range(-10+int(model_id), 10):
            values.append({"x": str(i),
                           "y": float(predicted_data[0, i, 0])})

        print(values)
        return values


class DataAPIGraph(Resource):
    def get(self, crypto):
        result = []
        _, _, norm, actual_data = get_data(filename=crypto + ".csv", num_days_to_predict=1)
        actual_data *= norm
        print(actual_data.shape)
        values = []
        i = 0
        for data in actual_data:
            values.append({"x": str(-actual_data.shape[0]+i), "y": float(data[0])})
            i += 1
        return values[-100:]


api.add_resource(CoinSeerAPI, '/<string:crypto>/<string:model_id>')
api.add_resource(CoinSeerAPIGraph, '/graph/<string:crypto>/<string:model_id>')
api.add_resource(DataAPIGraph, '/graph/<string:crypto>')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
