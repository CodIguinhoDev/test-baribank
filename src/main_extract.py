import json

from extraction.reader import read_reports
from extraction.json_writer import save_reports
from services.field_extractor import extract_report_fields


def main() -> None:
    reports = read_reports()
    extracted_reports = []

    for filename, content in reports.items():
        extracted = extract_report_fields(content)
        extracted["arquivo"] = filename

        extracted_reports.append(extracted)

    json_path = save_reports(extracted_reports)

    print(f"Total de laudos processados: {len(extracted_reports)}")
    print(f"JSON gerado em: {json_path}")
    print(json.dumps(extracted_reports, ensure_ascii=False, indent=4))


if __name__ == "__main__":
    main()
