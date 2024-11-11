from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, Field

# Define a type variable for generic typing
T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    data: Optional[T] = Field(
        None, description="Response data if the request is successful"
    )
    error: Optional[str] = Field(None, description="Error message if the request fails")

    class Config:
        arbitrary_types_allowed = True  # Allows custom types in the 'data' field
