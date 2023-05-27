from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class AudiencePart:
    audience_id: int
    number: str
    total_seats: int


def parse_row_data_to_audience_part(id_, number, total_seats):
    return AudiencePart(id_, number, total_seats)
