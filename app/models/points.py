from pydantic import BaseModel


from ._common import CommonBase, CommonBaseRead


# common (base, read, write)
class PointBase(BaseModel):
    lat: float
    lon: float

# db-only overrides
class Point(CommonBase, PointBase):
    pass

# create-only overrides
class PointCreate(PointBase):
    pass

# read-only overrides
class PointRead(CommonBaseRead, PointBase):
    pass