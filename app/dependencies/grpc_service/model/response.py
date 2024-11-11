from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class OrderRequest(BaseModel):
    num: int = Field(..., description="Unique identifier for the order request")


class OrderResponse(BaseModel):
    success: bool = Field(..., description="Indicates if the request was successful")
    data: Optional[Dict[str, Any]] = Field(
        None, description="Dictionary containing order details if request is successful"
    )
    error: Optional[str] = Field(None, description="Error message if the request fails")
