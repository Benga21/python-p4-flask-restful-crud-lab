#!/usr/bin/env python3

from app import app, db
from models import Plant

def seed_plants():
    # Clear existing plants
    Plant.query.delete()

    # List of plant data to seed
    plants = [
        Plant(name='Aloe', image='./images/aloe.jpg', price=11.50, is_in_stock=True),
        Plant(name='Cactus', image='./images/cactus.jpg', price=15.00, is_in_stock=True),
        Plant(name='Fern', image='./images/fern.jpg', price=10.00, is_in_stock=False),
        Plant(name='Bonsai', image='./images/bonsai.jpg', price=20.00, is_in_stock=True),
        Plant(name='ZZ Plant', image='./images/zz-plant.jpg', price=25.98, is_in_stock=False),
    ]

    try:
        # Add plants to the session and commit
        db.session.bulk_save_objects(plants)
        db.session.commit()
        print("Plants seeded successfully.")
    except Exception as e:
        db.session.rollback()  # Rollback the session on error
        print(f"An error occurred while seeding the plants: {e}")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables are created
        seed_plants()    # Seed the database with initial data
