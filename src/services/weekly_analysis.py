import pandas as pd


def analyze_weekly_summary(
    loss_analysis: pd.DataFrame,
    conversion_analysis: pd.DataFrame,
    channel_analysis: pd.DataFrame,
    score: pd.DataFrame,
    ltv_analysis: pd.DataFrame,
) -> dict[str, pd.DataFrame]:

    total_proposals = loss_analysis["count"].sum()

    total_contracted = loss_analysis.loc["Contratada", "count"]

    if total_proposals > 0:
        conversion_rate = total_contracted / total_proposals
    else:
        conversion_rate = 0

    total_requested = loss_analysis["sum"].sum()

    contracted_requested = loss_analysis.loc["Contratada", "sum"]

    summary = pd.DataFrame(
        {
            "Indicador": [
                "Total de propostas",
                "Total contratadas",
                "Taxa de conversão",
                "Valor total solicitado",
                "Valor solicitado das contratadas",
            ],
            "Valor": [
                total_proposals,
                total_contracted,
                conversion_rate,
                total_requested,
                contracted_requested,
            ],
        }
    )

    return {
        "resumo": summary,
        "perdas_por_status": loss_analysis,
        "conversao_por_ano": conversion_analysis,
        "conversao_por_canal": channel_analysis,
        "score_por_contrato": score,
        "conversao_por_ltv": ltv_analysis,
    }
