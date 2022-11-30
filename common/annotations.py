from dataclasses import dataclass


entity = dataclass(eq=False)
value_object = dataclass(order=True, frozen=True)
