from flask import Flask, jsonify, request, make_response, redirect
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False  # Set JSON formatting preference (optional)

# Initialize extensions
migrate = Migrate(app, db)
db.init_app(app)

# Initialize API
api = Api(app)

# Redirect the root URL to /plants
@app.route('/')
def home():
    return redirect('/plants')

# Resource for handling multiple plants
class Plants(Resource):
    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        data = request.get_json()

        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
            is_in_stock=data.get('is_in_stock', True)  # Default to True if not provided
        )

        db.session.add(new_plant)
        db.session.commit()

        return make_response(new_plant.to_dict(), 201)

# Resource for handling a plant by ID
class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first()
        if plant:
            return make_response(jsonify(plant.to_dict()), 200)
        return make_response(jsonify({"error": "Plant not found"}), 404)

    def patch(self, id):
        data = request.get_json()
        plant = Plant.query.filter_by(id=id).first()
        if plant:
            if 'is_in_stock' in data:
                plant.is_in_stock = data['is_in_stock']
                db.session.commit()
            return make_response(plant.to_dict(), 200)
        return make_response(jsonify({"error": "Plant not found"}), 404)

    def delete(self, id):
        plant = Plant.query.filter_by(id=id).first()
        if plant:
            db.session.delete(plant)
            db.session.commit()
            return make_response('', 204)
        return make_response(jsonify({"error": "Plant not found"}), 404)

# Add API resources
api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

# Main entry point
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create all tables if they don't exist yet
    app.run(port=5555, debug=True)
