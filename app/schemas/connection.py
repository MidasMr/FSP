from pydantic import BaseModel


class ConnectionBase(BaseModel):
    from_city_id: int
    to_city_id: int
    distance: int


class ConnectionCreate(ConnectionBase):
    pass


class Connection(ConnectionBase):
    id: int

    class Config:
        from_attributes = True
