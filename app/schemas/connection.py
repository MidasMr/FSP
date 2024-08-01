from pydantic import BaseModel, ConfigDict


class ConnectionBase(BaseModel):
    from_city_id: int
    to_city_id: int
    distance: int


class ConnectionCreate(ConnectionBase):
    pass


class Connection(ConnectionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
