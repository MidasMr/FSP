from pydantic import BaseModel, ConfigDict


class ConnectionBase(BaseModel):
    to_city_id: int
    distance: int


class ConnectionCreate(ConnectionBase):
    from_city_id: int


class ConnectionNestedCreate(ConnectionBase):
    pass


class Connection(ConnectionCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
