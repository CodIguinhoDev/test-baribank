import pandas as pd


def check_dataset_structure(df: pd.DataFrame) -> tuple[int, int]:
    return df.shape


def check_data_types(df: pd.DataFrame) -> pd.Series:
    return df.dtypes


def find_invalid_property_values(df: pd.DataFrame) -> pd.Series:
    converted = pd.to_numeric(df["valor_imovel"], errors="coerce")
    return df.loc[converted.isna(), "valor_imovel"]


def summarize_property_values(df: pd.DataFrame) -> pd.Series:
    return pd.to_numeric(df["valor_imovel"], errors="coerce").describe()


def find_invalid_entry_dates(df: pd.DataFrame) -> pd.Series:
    date_converted = pd.to_datetime(df["data_entrada"], errors="coerce")
    return df.loc[date_converted.isna(), "data_entrada"]


def summarize_entry_dates(df: pd.DataFrame) -> pd.Series:
    return pd.to_datetime(df["data_entrada"], errors="coerce").describe()


def check_missing_values(df: pd.DataFrame) -> pd.Series:
    return df.isnull().sum()


def check_duplicate_ids(df: pd.DataFrame) -> int:
    return int(df["id_proposta"].duplicated().sum())


def check_duplicate_rows(df: pd.DataFrame) -> int:
    return int(df.duplicated().sum())


def check_categorical_values(df: pd.DataFrame, column: str) -> pd.Series:
    return df[column].value_counts().sort_index()


def check_numeric_summary(df: pd.DataFrame) -> pd.DataFrame:
    return df.describe()
