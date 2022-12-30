from pydantic import EmailStr

from ._common import CommonBaseRead

# user "read" model - from auth service
class UserRead(CommonBaseRead):
    username: str
    full_name: str | None
    email: EmailStr
