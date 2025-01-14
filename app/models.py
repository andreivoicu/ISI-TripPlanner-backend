from sqlalchemy import Column, BigInteger, String, Text, ForeignKey, DateTime, Enum, Float # type: ignore
from sqlalchemy.ext.declarative import declarative_base # type: ignore
from sqlalchemy.orm import relationship # type: ignore
import enum 

Base = declarative_base()

class PointType(enum.Enum):
    PARK = "park"
    MUSEUM = "museum"
    HISTORIC_SITES = "historic sites"
    RESTAURANT = "restaurant"
    PUB = "pub"
    CAFFE = "caffe"
    BAR = "bar"
    TOURIST_ATTRACTION = "tourist attraction"
    ART_GALERY = "art gallery"
    OTHER = "Other"

class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(Text, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    current_route = Column(BigInteger, ForeignKey('routes.id'), nullable=True)
    previous_routes = relationship(
        'Route', 
        back_populates='user', 
        cascade='all, delete-orphan', 
        foreign_keys='Route.user_id'  # Specify the foreign key column
    )

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"

    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
        }


class Route(Base):
    __tablename__ = 'routes'

    id = Column(BigInteger, primary_key=True, index=True)
    city = Column(String(100), nullable=False)
    timeSTAMP = Column(DateTime, nullable=True)
    total_time_spent = Column(BigInteger, nullable=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    points_of_interest = relationship('PointOfInterest', back_populates='route', cascade='all, delete-orphan', lazy='joined')

    user = relationship(
        'User', 
        back_populates='previous_routes', 
        foreign_keys='Route.user_id'  # Specify the foreign key column
    )

    def __repr__(self):
        return f"<Route(city={self.city}, timeSTAMP={self.timeSTAMP})>"

    def serialize(self):
        return {
            'id': self.id,
            'city': self.city,
            'timeSTAMP': self.timeSTAMP,
            'total_time_spent': self.total_time_spent,
            'user_id': self.user_id,
            'points_of_interest': [point.serialize() for point in self.points_of_interest],
            
        }

class PointOfInterest(Base):
    __tablename__ = 'points_of_interest'

    id = Column(BigInteger, primary_key=True, index=True)
    type = Column(Enum(PointType), nullable=True)
    name = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    time_spent = Column(BigInteger, nullable=True)
    route_id = Column(BigInteger, ForeignKey('routes.id'), nullable=True)
    price_range = Column(BigInteger, nullable=True)
    rating = Column(BigInteger, nullable=False)


    route = relationship('Route', back_populates='points_of_interest', lazy='joined')

    def __repr__(self):
        return f"<PointOfInterest(id={self.id}, route_id={self.route_id}, type={self.type}, latitude={self.latitude}, longitude={self.longitude})>"

    def serialize(self):
        return {
            'id': self.id,
            'type': None if self.type is None else self.type.value,
            'name': self.name,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'time_spent': self.time_spent,
            'route_id': self.route_id,
            'price_range': self.price_range,
            'rating': self.rating,
        }