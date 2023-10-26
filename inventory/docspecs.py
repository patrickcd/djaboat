from decimal import Decimal
from datetime import date

from pydantic import BaseModel, Field

class Boat(BaseModel):
    name: str
    design: str
    designer: str | None
    builder: str | None
    hull_number: str | None
    sail_number: str | None
    registration: str | None
    home_port: str | None
    ce_certificate: str | None
    year_commissioned: int | None
    year_launched: int | None
    construction: str | None
    loa: Decimal = Field(max_digits=4, decimal_places=1)
    lwl: Decimal = Field(max_digits=4, decimal_places=1)
    beam: Decimal  = Field(max_digits=4, decimal_places=1)
    draft: Decimal = Field(max_digits=3, decimal_places=1)
    displacement: int = Field(description="in kg")
    keel_type: str | None
    sail_area: Decimal = Field(max_digits=4, decimal_places=1)
    hull_speed: Decimal | None = Field(max_digits=3, decimal_places=1)
    travel_lifting_points: str | None


class Sail(BaseModel):
    luff_length: int
    leech_length: int
    foot_length: int


class RunningRigging(BaseModel):
    length: int
    diameter: int
    material: str
    year_rigged: int


