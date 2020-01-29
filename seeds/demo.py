from flask_seeder import Seeder, Faker, generator

from flask_uber_clone.rider.models import Route, PendingOrder


# All seeders inherit from Seeder
class DemoSeeder(Seeder):
    # run() will be called by Flask-Seeder
    def run(self):
        # Create a new Faker and tell it how to create User objects
        route_faker = Faker(
            cls=Route,
            init={
                "x1": generator.Integer(start=-50, end=50),
                "y1": generator.Integer(start=-50, end=50),
                "x2": generator.Integer(start=-50, end=50),
                "y2": generator.Integer(start=-50, end=50),
            }
        )

        order_faker = Faker(
            cls=PendingOrder,
            init={
                "rider_id": 1,
                "route_id": 0,
                "people_count": generator.Integer(start=1, end=9),
            }
        )

        # Create 5 users
        for order in order_faker.create(1000):
            print(order)
            route = route_faker.create()[0]
            self.db.session.add(route)
            self.db.session.flush()
            order.route_id = route.id
            self.db.session.add(order)
