from errors.constants import REQUIRED_TREATMENT_COLUMNS
import pandas as pd


def clean_property_values(property_value: pd.Series) -> pd.Series:
    clear_value = property_value.str.replace("R$", "").str.strip()
    return pd.to_numeric(clear_value, errors="coerce")


def clean_entry_dates(date: pd.Series) -> pd.Series:
    clear_date = date.str.replace("/", "-").str.strip()
    return pd.to_datetime(clear_date, format="mixed", dayfirst=True, errors="coerce")


def normalize_origin_channel(categorical: pd.Series) -> pd.Series:
    text_normalized = categorical.str.strip().str.capitalize()
    return text_normalized


def remove_land_properties(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["tipo_imovel"] != "Terreno"]


def correct_invalid_funnel_stage(stage: pd.Series) -> pd.Series:
    return stage.replace(7, 6)


def apply_treatments(df: pd.DataFrame) -> pd.DataFrame:
    missing_columns = REQUIRED_TREATMENT_COLUMNS.difference(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Colunas necessárias para o tratamento ausentes: {missing}")

    df["valor_imovel"] = clean_property_values(df["valor_imovel"])
    df["data_entrada"] = clean_entry_dates(df["data_entrada"])
    df["canal_origem"] = normalize_origin_channel(df["canal_origem"])
    df["etapa_max_funil"] = correct_invalid_funnel_stage(df["etapa_max_funil"])

    df = remove_land_properties(df)

    return df
