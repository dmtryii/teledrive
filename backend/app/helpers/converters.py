from datetime import date, datetime


def str_to_date(s: str) -> date:
    try:
        return datetime.strptime(s, '%Y-%m-%d').date()
    except ValueError:
        raise ValueError('Invalid date format. Use YYYY-MM-DD format.')
    