from ..db_queries import *

def get_pois():
    pois = get_points_of_interest()
    return jsonify([poi.serialize() for poi in pois])