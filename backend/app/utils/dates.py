from datetime import date, datetime


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()
