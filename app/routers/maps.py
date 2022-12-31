import logging
from typing import List, Literal
from pydantic import Required
from fastapi import APIRouter, Depends, HTTPException, Query

from app.db import db
from app.models.maps import *
from app.models.jwt import *
from app.auth import get_current_user


TABLE = 'distances'
table = db[TABLE]


router = APIRouter(
    prefix='/distances',
    tags=['distances'],
)


#async def get_distance(
#    id: str | UUID,
#    # enforce ownership + auth
#    token: JWTokenData = Depends(get_current_user),
#) -> Distance:
#    distance = await table.find_one({'_id': str(id), 'user_id': str(token.user_id)})
#    if not distance: raise HTTPException(status_code=404, detail=f'Distance not found')
#
#    return Distance(**distance)


#@router.get('/', response_model=List[DistanceRead])
#async def list_distances(token: JWTokenData = Depends(get_current_user)):
#    return await table.find({'user_id': str(token.user_id)}).to_list(1000)


#@router.get('/{id}', response_model=DistanceRead)
#async def read_distance(distance: Distance = Depends(get_distance)):
#    return distance


#@router.delete('/{id}')
#async def delete_distance(distance: Distance = Depends(get_distance),):
#    await table.delete_one({'_id': str(distance.id)})
#
#    return { 'ok': True }


#
# Google maps stuff
#

from app.config import Settings, get_settings

import googlemaps

@router.get('/points_list', response_model=List[Distance])
async def read_distance_matrix(
    settings: Settings = Depends(get_settings),
    token: JWTokenData = Depends(get_current_user),
    coords: list[str] = Query(default=Required),
    mode: Literal[
        'driving',
        'walking',
        'bicycling',
        'transit'
    ] = Query(default='driving'),
):

    points = [parse_point(coord) for coord in coords]
    tuples = [(p.lat, p.lng) for p in points]

    gmaps = googlemaps.Client(key=settings.maps_api_key)
    
    g_distances = gmaps.distance_matrix(
        tuples, tuples,
        region=settings.maps_api_region,
    )

    distances = []
    for row, columns in enumerate(g_distances['rows']):
        for column, values in enumerate(columns['elements']):
            p1 = points[row]
            p1 = f'{p1.lat};{p1.lng}'
            p2 = points[column]
            p2 = f'{p2.lat};{p2.lng}'
            distances.append(
                Distance(
                    p1=p1, p2=p2,
                    distance=values['distance']['value'],
                    duration=values['duration']['value'],
                )
            )

    return distances
