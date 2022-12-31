from pydantic import BaseModel


def parse_point(input: str):
    lat, lng = input.split(';')
    lat = float(lat)
    lng = float(lng)
    
    # cut to 4 decimals
    lat = '{:.4f}'.format(lat)
    lng = '{:.4f}'.format(lng)

    return StrPoint(lat=lat, lng=lng)

class StrPoint(BaseModel):
    lat: str
    lng: str

class Distance(BaseModel):
    p1: str
    p2: str
    distance: int
    duration: int