from pydantic import BaseModel, field_validator, model_validator

# RentalOutcome is the response the API sends back after a rental is created.
class RentalOutcome(BaseModel):
    user_id: int
    bike_id: int
    bike_battery: int

    # field_validator runs after the field is parsed.
    # It rejects the object if the battery is too low (e.g. data coming from the DB is bad).
    @field_validator("bike_battery")
    @classmethod
    def battery_must_be_at_least_20(cls, v: int) -> int:
        if v < 20:
            raise ValueError("Bike battery too low for rental.")
        return v


# RentalProcessing is what the client sends when requesting a rental.
class RentalProcessing(BaseModel):
    bike_battery: int
    user_id: int
    bike_id: int

    # model_validator(mode="after") runs once all fields are validated and set.
    # It lets us check conditions that involve multiple fields at once.
    @model_validator(mode="after")
    def validate_rental(self) -> "RentalProcessing":
        if self.bike_battery < 20:
            raise ValueError("Bike battery too low for rental.")
        return self