import pandas as pd


def analyze_conversion_by_ltv(df: pd.DataFrame) -> pd.DataFrame:
    analysis = df.groupby("faixa_ltv").agg(
        propostas=("id_proposta", "count"),
        contratadas=("status_final", lambda status: (status == "Contratada").sum()),
    )

    analysis["taxa_conversao"] = analysis["contratadas"] / analysis["propostas"]

    return analysis


def analyze_loss_by_status(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("status_final")["valor_solicitado"]
        .agg(["count", "sum"])
        .sort_values("sum", ascending=False)
    )


def analyze_conversion_by_year(df: pd.DataFrame) -> pd.DataFrame:
    annual = df.groupby(df["data_entrada"].dt.to_period("Y")).agg(
        propostas=("id_proposta", "count"),
        contratadas=("status_final", lambda x: (x == "Contratada").sum()),
    )

    annual["conversion_rate"] = annual["contratadas"] / annual["propostas"]

    return annual


def analyze_conversion_by_channel(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("canal_origem")
        .agg(
            propostas=("id_proposta", "count"),
            contratadas=("status_final", lambda x: (x == "Contratada").sum()),
        )
        .assign(conversion_rate=lambda data: (data["contratadas"] / data["propostas"]))
        .sort_values("conversion_rate", ascending=False)
    )


def analyze_score_by_contract(df: pd.DataFrame) -> pd.DataFrame:
    contracted = df[df["status_final"] == "Contratada"]["score_credito"]
    not_contracted = df[df["status_final"] != "Contratada"]["score_credito"]

    return pd.DataFrame(
        {
            "Contratada": contracted.describe(),
            "Não contratada": not_contracted.describe(),
        }
    )
