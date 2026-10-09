import pandas as pd

from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def format_currency(value: float) -> str:
    formatted = f"R$ {value:,.2f}"
    return formatted.replace(",", "X").replace(".", ",").replace("X", ".")


def format_value(
    value: object,
    column: str = "",
    indicator: str = "",
) -> str:
    if pd.isna(value):
        return "-"

    if isinstance(value, (int, float)):
        if column in ("conversion_rate", "taxa_conversao") or (
            indicator == "Taxa de conversão"
        ):
            return f"{value:.2%}".replace(".", ",")

        if column == "sum" or indicator in (
            "Valor total solicitado",
            "Valor solicitado das contratadas",
        ):
            return format_currency(value)

        if column in (
            "count",
            "propostas",
            "contratadas",
            "Total de propostas",
            "Total contratadas",
        ) or indicator in ("Total de propostas", "Total contratadas"):
            return f"{value:,.0f}".replace(",", ".")

        formatted = f"{value:,.2f}"
        return formatted.replace(",", "X").replace(".", ",").replace("X", ".")

    return str(value)


def dataframe_to_table(df: pd.DataFrame) -> list[list[str]]:
    table_data = [list(df.columns)]

    has_summary_columns = "Indicador" in df.columns and "Valor" in df.columns

    for row in df.itertuples(index=False, name=None):
        indicator = ""

        if has_summary_columns:
            indicator = str(row[df.columns.get_loc("Indicador")])

        table_data.append(
            [
                format_value(value, column, indicator)
                for column, value in zip(df.columns, row)
            ]
        )

    return table_data


def add_section(
    elements: list,
    title: str,
    df: pd.DataFrame,
    commentary: str = "",
) -> None:
    styles = getSampleStyleSheet()

    elements.append(Paragraph(title, styles["Heading2"]))
    elements.append(Spacer(1, 0.3 * cm))

    if commentary:
        elements.append(Paragraph(commentary, styles["BodyText"]))
        elements.append(Spacer(1, 0.3 * cm))

    table = Table(
        dataframe_to_table(df),
        repeatRows=1,
        hAlign="CENTER",
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#242C62")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("PADDING", (0, 0), (-1, -1), 6),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )

    elements.append(table)
    elements.append(Spacer(1, 0.6 * cm))


def describe_losses(df: pd.DataFrame) -> str:
    most_proposals = df["count"].idxmax()
    most_value = df["sum"].idxmax()

    return (
        f"O status com mais propostas é {most_proposals}, "
        f"com {df.loc[most_proposals, 'count']:.0f} registros. "
        f"Em valor solicitado, o maior total está em {most_value}, "
        f"com {format_currency(df.loc[most_value, 'sum'])}. "
        "Esses valores representam montantes solicitados, "
        "não prejuízos financeiros confirmados."
    )


def describe_conversion_by_year(df: pd.DataFrame) -> str:
    if len(df) < 2:
        return "Não há dados suficientes para comparar dois anos."

    first, last = df.iloc[0], df.iloc[-1]
    change = (last["conversion_rate"] - first["conversion_rate"]) * 100

    return (
        f"A conversão passou de {first['conversion_rate']:.2%} "
        f"em {df.index[0]} para {last['conversion_rate']:.2%} "
        f"em {df.index[-1]}, uma variação de {change:+.2f} "
        "pontos percentuais. "
        f"Foram analisadas {first['propostas']:.0f} propostas "
        f"no primeiro ano e {last['propostas']:.0f} no último."
    )


def describe_channels(df: pd.DataFrame) -> str:
    best = df["conversion_rate"].idxmax()
    worst = df["conversion_rate"].idxmin()

    return (
        f"O canal com maior conversão é {best}, com "
        f"{df.loc[best, 'conversion_rate']:.2%} "
        f"({df.loc[best, 'propostas']:.0f} propostas). "
        f"O menor resultado é de {worst}, com "
        f"{df.loc[worst, 'conversion_rate']:.2%} "
        f"({df.loc[worst, 'propostas']:.0f} propostas)."
    )


def describe_score(df: pd.DataFrame) -> str:
    contracted = df.loc["mean", "Contratada"]
    not_contracted = df.loc["mean", "Não contratada"]
    difference = contracted - not_contracted

    return (
        f"O score médio das propostas contratadas é {contracted:.2f}, "
        f"contra {not_contracted:.2f} nas não contratadas, "
        f"uma diferença de {difference:+.2f} pontos. "
        "Essa diferença indica uma associação, não comprova uma causa."
    )


def describe_conversion_by_ltv(df: pd.DataFrame) -> str:
    if "Até 60%" not in df.index or "Acima de 60%" not in df.index:
        return "Não há dados suficientes para comparar as faixas de LTV."

    lower_ltv = df.loc["Até 60%"]
    higher_ltv = df.loc["Acima de 60%"]

    difference = (lower_ltv["taxa_conversao"] - higher_ltv["taxa_conversao"]) * 100

    return (
        f"Propostas com LTV de até 60% apresentaram conversão de "
        f"{lower_ltv['taxa_conversao']:.2%}, enquanto propostas acima "
        f"de 60% apresentaram {higher_ltv['taxa_conversao']:.2%}. "
        f"A diferença foi de {difference:.2f} pontos percentuais. "
        "O resultado indica uma associação entre as faixas de LTV "
        "e a conversão, mas não comprova causalidade."
    )


def add_recommendations(
    elements: list,
    analysis_weekly: dict[str, pd.DataFrame],
) -> None:
    styles = getSampleStyleSheet()

    channels = analysis_weekly["conversao_por_canal"]
    worst_channel = channels["conversion_rate"].idxmin()
    worst_rate = channels.loc[worst_channel, "conversion_rate"]
    worst_count = channels.loc[worst_channel, "propostas"]

    score = analysis_weekly["score_por_contrato"]
    contracted_score = score.loc["mean", "Contratada"]
    not_contracted_score = score.loc["mean", "Não contratada"]
    score_difference = contracted_score - not_contracted_score

    ltv = analysis_weekly["conversao_por_ltv"]
    ltv_commentary = describe_conversion_by_ltv(ltv)

    losses = analysis_weekly["perdas_por_status"].drop(
        index="Contratada",
        errors="ignore",
    )
    top_losses = losses.nlargest(2, "sum")

    elements.append(Paragraph("Considerações", styles["Heading1"]))
    elements.append(Spacer(1, 0.3 * cm))

    recommendations = [
        (
            "<b>1. Investigar o canal com menor conversão.</b> "
            f"O canal {worst_channel} apresentou conversão de "
            f"{worst_rate:.2%}, com {worst_count:.0f} propostas. "
            "Recomenda-se investigar a qualidade dos leads, a documentação "
            "inicial e os motivos de não contratação."
        ),
        (
            "<b>2. Testar uma priorização baseada em indicadores.</b> "
            f"O score médio das contratadas foi {contracted_score:.2f}, "
            f"contra {not_contracted_score:.2f} nas não contratadas, "
            f"uma diferença de {score_difference:+.2f} pontos. "
            f"{ltv_commentary} "
            "Recomenda-se testar segmentações para orientar a análise, "
            "sem transformar esses indicadores em critérios automáticos "
            "de aprovação."
        ),
        (
            "<b>3. Investigar os principais status de não contratação.</b> "
            + " e ".join(
                f"{status} ({format_currency(value)})"
                for status, value in top_losses["sum"].items()
            )
            + ". Recomenda-se acompanhar as propostas sem retorno e "
            "investigar os motivos de desistência para identificar "
            "oportunidades de recuperação."
        ),
    ]

    for recommendation in recommendations:
        elements.append(Paragraph(recommendation, styles["BodyText"]))
        elements.append(Spacer(1, 0.3 * cm))


def generate_pdf(analysis_weekly: dict[str, pd.DataFrame]) -> Path:
    output_path = (
        Path(__file__).resolve().parent.parent.parent
        / "outputs"
        / "relatorio_analise.pdf"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=landscape(A4),
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
    )

    styles = getSampleStyleSheet()
    elements = []

    elements.append(
        Paragraph("Relatório Executivo — Análise de Crédito", styles["Title"])
    )
    elements.append(Spacer(1, 0.4 * cm))

    elements.append(
        Paragraph(
            "Este relatório apresenta os principais indicadores da base "
            "tratada, com foco na conversão, nas perdas, no desempenho "
            "dos canais de origem e na relação entre LTV e contratação.",
            styles["BodyText"],
        )
    )
    elements.append(Spacer(1, 0.6 * cm))

    add_section(
        elements,
        "Indicadores principais",
        analysis_weekly["resumo"],
    )

    losses = analysis_weekly["perdas_por_status"]
    add_section(
        elements,
        "Perdas por status",
        losses.reset_index(),
        describe_losses(losses),
    )

    annual = analysis_weekly["conversao_por_ano"].sort_index()
    add_section(
        elements,
        "Conversão por ano",
        annual.reset_index(),
        describe_conversion_by_year(annual),
    )

    channels = analysis_weekly["conversao_por_canal"]
    add_section(
        elements,
        "Conversão por canal",
        channels.reset_index(),
        describe_channels(channels),
    )

    score = analysis_weekly["score_por_contrato"]
    add_section(
        elements,
        "Score por situação da proposta",
        score.reset_index(),
        describe_score(score),
    )

    ltv = analysis_weekly["conversao_por_ltv"]
    add_section(
        elements,
        "Conversão por faixa de LTV",
        ltv.reset_index(),
        describe_conversion_by_ltv(ltv),
    )

    add_recommendations(elements, analysis_weekly)

    elements.append(Paragraph("Considerações finais", styles["Heading1"]))
    elements.append(
        Paragraph(
            "Os resultados ajudam a identificar oportunidades de melhoria "
            "no funil de crédito. As diferenças observadas devem ser "
            "investigadas considerando o período analisado e as limitações "
            "dos dados, pois associações não comprovam relações de causa "
            "e efeito.",
            styles["BodyText"],
        )
    )

    document.build(elements)

    return output_path
