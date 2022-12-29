from sources.application.handlers import AccessHandler, PollHandler
from sources.infrastructure.adapters.access import Authentication
from sources.infrastructure.adapters.access.repositories import UserRepository
from sources.infrastructure.adapters.polls.repositories import PollRepository


access_handler = AccessHandler(
    Authentication(),
    UserRepository(),
)
poll_handler = PollHandler(
    PollRepository(),
)
