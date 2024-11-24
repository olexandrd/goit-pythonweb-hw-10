from datetime import date
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber


class ContactModel(BaseModel):
    """
    Model representing a contact with various attributes.
    """

    name: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    email: EmailStr = Field(max_length=50)
    phone_number: PhoneNumber
    birstday: date
    notes: str | None = Field(max_length=500, default=None)
    model_config = ConfigDict(validate_number_format="E.164")


class ContactUpdate(ContactModel):
    done: bool


class ContactResponse(ContactModel):
    id: int
    name: str
    surname: str
    email: str
    phone_number: str
    birstday: date
    model_config = ConfigDict(from_attributes=True)
