from typing import ClassVar as _ClassVar
from typing import Optional as _Optional

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message

DESCRIPTOR: _descriptor.FileDescriptor

class OrderRequest(_message.Message):
    __slots__ = ("order",)
    ORDER_FIELD_NUMBER: _ClassVar[int]
    order: str
    def __init__(self, order: _Optional[str] = ...) -> None: ...

class OrderResponse(_message.Message):
    __slots__ = ("order_status",)
    ORDER_STATUS_FIELD_NUMBER: _ClassVar[int]
    order_status: str
    def __init__(self, order_status: _Optional[str] = ...) -> None: ...
