from pathlib import Path
import pandas as pd

DATASET_PATH: Path = Path(__file__).parent.parent / "data" / "propostas_credito.csv"


def load_dataset() -> pd.DataFrame:
    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Arquivo de entrada não encontrado")

    try:
        dataset = pd.read_csv(DATASET_PATH)

    except pd.errors.EmptyDataError as error:
        raise ValueError("O arquivo CSV está vazio.") from error

    except pd.errors.ParserError as error:
        raise ValueError(
            "Não foi possível interpretar a estrutura do arquivo CSV."
        ) from error

    except OSError as error:
        raise OSError(f"Não foi possível ler o arquivo: {DATASET_PATH}") from error

    if dataset.empty:
        raise ValueError("O arquivo CSV não contém registros.")

    return dataset
