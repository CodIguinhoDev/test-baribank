from analysis.data_loader import load_dataset
from analysis.treatment import apply_treatments
from services.ltv import calculate_ltv, classify_ltv
from services.weekly_analysis import analyze_weekly_summary
from reports.pdf_report import generate_pdf
from analysis.funnel_analysis import (
    analyze_conversion_by_ltv,
    analyze_conversion_by_year,
    analyze_conversion_by_channel,
    analyze_loss_by_status,
    analyze_score_by_contract,
)


def run() -> None:
    try:
        dataset = load_dataset()
        processed_data = apply_treatments(dataset)

        processed_data["ltv"] = calculate_ltv(
            processed_data["valor_solicitado"], processed_data["valor_imovel"]
        )

        processed_data["faixa_ltv"] = classify_ltv(processed_data["ltv"])

        loss_analysis = analyze_loss_by_status(processed_data)
        conversion_analysis = analyze_conversion_by_year(processed_data)
        channel_analysis = analyze_conversion_by_channel(processed_data)
        score_analysis = analyze_score_by_contract(processed_data)
        ltv_analysis = analyze_conversion_by_ltv(processed_data)

        analysis_weekly = analyze_weekly_summary(
            loss_analysis,
            conversion_analysis,
            channel_analysis,
            score_analysis,
            ltv_analysis,
        )

        pdf_path = generate_pdf(analysis_weekly)

        print(f"PDF gerado em: {pdf_path}")

    except Exception as error:
        print("Algo deu errado", error)
