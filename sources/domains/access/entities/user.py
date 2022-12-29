from dataclasses import dataclass, field

from phonenumbers import PhoneNumber, parse

from common.domains.entity import Entity


@dataclass(eq=False)
class User(Entity):
    email: str
    first_name: str = field(default=None)
    last_name: str = field(default=None)
    phone: PhoneNumber = field(default=None)

    @classmethod
    def create(
        cls,
        *args,
        phone: PhoneNumber | str = None,
        region: str = None,
        **kwargs,
    ):
        if isinstance(phone, str):
            phone = parse(phone, region=region)

        return cls(*args, phone=phone, **kwargs)
