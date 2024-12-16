from sqlalchemy import Column, BigInteger, String, Text, ForeignKey, Enum # type: ignore
from sqlalchemy.ext.declarative import declarative_base # type: ignore
from sqlalchemy.orm import relationship # type: ignore
import enum 

Base = declarative_base()

class PointType(enum.Enum):
    PARK = "Park"
    MUSEUM = "Museum"
    HISTORIC_SITE = "Historic Site"
    RESTAURANT = "Restaurant"
    PUB = "Pub"
    CAFFE = "Caffe"
    BAR = "Bar"
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
    total_time_spent = Column(BigInteger, nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    points_of_interest = relationship('PointOfInterest', back_populates='route', cascade='all, delete-orphan')

    user = relationship(
        'User', 
        back_populates='previous_routes', 
        foreign_keys='Route.user_id'  # Specify the foreign key column
    )

    def __repr__(self):
        return f"<Route(city={self.city}, total_time_spent={self.total_time_spent})>"

    def serialize(self):
        return {
            'id': self.id,
            'city': self.city,
            'route': self.route,
            'total_time_spent': self.total_time_spent,
            'user_id': self.user_id,
        }

class PointOfInterest(Base):
    __tablename__ = 'points_of_interest'

    id = Column(BigInteger, primary_key=True, index=True)
    type = Column(Enum(PointType), nullable=False)
    location = Column(String(200), nullable=False)
    time_spent = Column(BigInteger, nullable=False)
    route_id = Column(BigInteger, ForeignKey('routes.id'), nullable=False)

    route = relationship('Route', back_populates='points_of_interest')

    def __repr__(self):
        return f"<PointOfInterest(type={self.type}, location={self.location})>"

    def serialize(self):
        return {
            'id': self.id,
            'type': self.type.value,
            'location': self.location,
            'time_spent': self.time_spent,
            'route_id': self.route_id,
        }