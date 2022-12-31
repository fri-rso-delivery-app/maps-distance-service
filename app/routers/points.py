from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder

from app.db import db
from app.models.points import *
from app.models.jwt import *
from app.auth import get_current_user


TABLE = 'points'
table = db[TABLE]


router = APIRouter(
    prefix='/points',
    tags=['points'],
)


async def get_point(
    id: str | UUID,
    # enforce ownership + auth
    token: JWTokenData = Depends(get_current_user),
) -> Point:
    point = await table.find_one({'_id': str(id)})
    if not point: raise HTTPException(status_code=404, detail=f'Point not found')

    return Point(**point)


@router.post('/', response_model=PointRead)
async def create_point(*,
    point: PointCreate,
    token: JWTokenData = Depends(get_current_user),
):
    # create
    point_db = jsonable_encoder(Point(
        **point.dict(),
    ))
    new_point = await table.insert_one(point_db)
    created_point = await get_point(new_point.inserted_id, token)
    
    return created_point


@router.get('/', response_model=List[PointRead])
async def list_points(token: JWTokenData = Depends(get_current_user)):
    return await table.find().to_list(1000)


@router.get('/{id}', response_model=PointRead)
async def read_point(point: Point = Depends(get_point)):
    return point
