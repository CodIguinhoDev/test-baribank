from pathlib import Path

LAUDOS_PATH = Path(__file__).resolve().parent.parent / "data" / "laudos_avaliacao"


def read_reports() -> dict[str, str]:
    if not LAUDOS_PATH.is_dir():
        raise FileNotFoundError(f"Pasta de laudos não encontrada: {LAUDOS_PATH}")

    files = sorted(LAUDOS_PATH.glob("*.txt"))

    if not files:
        raise FileNotFoundError(f"Nenhum arquivo TXT encontrado em: {LAUDOS_PATH}")

    reports: dict[str, str] = {
        file.name: file.read_text(encoding="utf-8") for file in files
    }

    return reports
