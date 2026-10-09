import json
from pathlib import Path

OUTPUT_PATH = (
    Path(__file__).resolve().parent.parent.parent / "outputs" / "laudos_extraidos.json"
)


def save_reports(reports: list[dict]) -> Path:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(reports, file, ensure_ascii=False, indent=4)

    return OUTPUT_PATH
