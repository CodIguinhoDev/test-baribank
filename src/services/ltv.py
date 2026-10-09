import pandas as pd
from config.config import MAX_LTV_RATIO
from errors.message_error import (
    INVALID_REQUESTED_AMOUNT,
    MISSING_PROPERTY_VALUE,
    MISSING_REQUESTED_AMOUNT,
    INVALID_PROPERTY_VALUE,
)


def calculate_ltv(requested_amount: pd.Series, property_value: pd.Series) -> pd.Series:

    if property_value.isna().any():
        raise ValueError(MISSING_PROPERTY_VALUE)
    if requested_amount.isna().any():
        raise ValueError(MISSING_REQUESTED_AMOUNT)
    if (property_value <= 0).any():
        raise ValueError(INVALID_PROPERTY_VALUE)
    if (requested_amount <= 0).any():
        raise ValueError(INVALID_REQUESTED_AMOUNT)

    return requested_amount / property_value


def validate_ltv(ltv: pd.Series) -> pd.Series | bool:
    return ltv > MAX_LTV_RATIO


def classify_ltv(ltv: pd.Series) -> pd.Series:
    return pd.cut(
        ltv,
        bins=[-float("inf"), MAX_LTV_RATIO, float("inf")],
        labels=["Até 60%", "Acima de 60%"],
    )


def summarize_ltv(ltv: pd.Series) -> pd.Series:
    return pd.Series(
        {
            "total": ltv.size,
            "sem_ltv": ltv.isna().sum(),
            "negativos": (ltv < 0).sum(),
            "acima_60": (ltv > MAX_LTV_RATIO).sum(),
            "ate_60": (ltv <= MAX_LTV_RATIO).sum(),
        }
    )
