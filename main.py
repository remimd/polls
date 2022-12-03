from uuid import uuid4

from sources.domains.polls.entities import Poll


def main():
    uuid = uuid4()
    poll1 = Poll("Hello?", id=uuid)
    poll2 = Poll("Hello?")
    assert poll1 != poll2


if __name__ == "__main__":
    main()
