from datetime import datetime


def normalize_number(value: str | None) -> float | None:
    if not value:
        return None

    normalized = value.strip().replace(".", "").replace(",", ".")

    try:
        return float(normalized)

    except ValueError:
        return None


def normalize_date(value: str | None) -> str | None:
    if not value:
        return None

    for date_format in ("%d/%m/%Y", "%d-%m-%Y"):
        try:
            date = datetime.strptime(value.strip(), date_format)
            return date.strftime("%Y-%m-%d")
        except ValueError:
            continue

    return None
