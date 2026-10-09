import re

from services.normalizer_data import normalize_date, normalize_number


def find_match(pattern: str, content: str):
    return re.search(pattern, content, re.IGNORECASE | re.MULTILINE)


def get_text(match):
    return match.group(1).strip().rstrip(".") if match else None


def extract_date(content: str):
    date_pattern = (
        r"(?:Vistoria realizada em|Vistoria efetuada em|Vistoria em|"
        r"Vistoria|Data da vistoria|Data de vistoria|Data da inspeção|"
        r"Data da visita técnica|Data do levantamento|"
        r"Inspeção presencial em|Inspeção em|Inspeção|Visita técnica)"
        r"\s*:?\s*(\d{2}[/-]\d{2}[/-]\d{4})"
    )

    match = find_match(date_pattern, content)

    if match:
        return normalize_date(match.group(1))

    months = {
        "janeiro": "01",
        "fevereiro": "02",
        "março": "03",
        "abril": "04",
        "maio": "05",
        "junho": "06",
        "julho": "07",
        "agosto": "08",
        "setembro": "09",
        "outubro": "10",
        "novembro": "11",
        "dezembro": "12",
    }

    match = find_match(
        r"\bEm\s+(\d{1,2})\s+de\s+"
        r"(janeiro|fevereiro|março|abril|maio|junho|julho|"
        r"agosto|setembro|outubro|novembro|dezembro)"
        r"\s+de\s+(\d{4})",
        content,
    )

    if match:
        day, month, year = match.groups()
        return f"{year}-{months[month.lower()]}-{int(day):02d}"

    return None


def extract_area(pattern: str, content: str):
    match = find_match(pattern, content)

    if not match:
        return None

    return normalize_number(match.group(1))


def extract_property_type(content: str):
    patterns = [
        r"^Tipo de imóvel\s*:\s*([^\n]+)",
        r"^Tipo de propriedade\s*:\s*([^\n]+)",
        r"^Identificação\s*:\s*([^\n]+)",
        r"^Imóvel\s*:\s*([^\n]+)",
        r"^Tipo\s*:\s*([^\n]+)",
        r"^Bem avaliando\s*:\s*([^\n]+)",
        r"^Objeto\s*:\s*([^\n]+)",
    ]

    for pattern in patterns:
        match = find_match(pattern, content)

        if not match:
            continue

        value = match.group(1).strip().rstrip(".")

        special_cases = [
            (r"^(apartamento residencial)\s+na\b.*", r"\1"),
            (r"^(apartamento)\s+no\b.*", r"\1"),
            (r"^(apartamento)\s*,.*", r"\1"),
            (r"^(imóvel rural)\s+denominado\b.*", r"\1"),
            (r"^(casa)\s*,.*", r"\1"),
        ]

        for special_pattern, replacement in special_cases:
            if re.match(special_pattern, value, re.IGNORECASE):
                return re.sub(
                    special_pattern,
                    replacement,
                    value,
                    flags=re.IGNORECASE,
                )

        return value

    patterns = [
        (r"\bTrata-se de uma\s+(casa térrea)\b", "group"),
        (r"\bvistoriamos a\s+(sala comercial)\s+\d+", "group"),
        (r"^Apartamento situado à\b", "apartamento"),
        (r"^Apartamento,", "apartamento"),
        (r"^Apartamento residencial na\b", "apartamento residencial"),
        (r"^Casa geminada,", "casa geminada"),
        (r"^Casa residencial na\b", "casa residencial"),
        (r"^Terreno para incorporação localizado na\b", "terreno"),
        (r"^Unidade comercial\s+\d+", "unidade comercial"),
    ]

    for pattern, result in patterns:
        match = find_match(pattern, content)

        if match:
            return match.group(1).strip() if result == "group" else result

    return None


def extract_address(content: str):

    match = find_match(
        r"^(?:Endereço do imóvel|Endereço|Localização do bem|Local)" r"\s*:\s*([^\n]+)",
        content,
    )

    if match:
        return get_text(match)

    patterns = [
        r"^Apartamento situado à\s*(.+)",
        r"^Casa geminada,\s*(.+)",
        r"^Casa residencial na\s*(.+)",
        r"^Terreno para incorporação localizado na\s*(.+)",
        r"^Apartamento,\s*(.+)",
        r"^Imóvel residencial:\s*casa,\s*(.+)",
        r"^Unidade comercial\s+\d+,\s*(.+)",
        r"^Objeto\s*:\s*apartamento residencial na\s*(.+)",
        r"^Objeto\s*:\s*apartamento na\s*(.+)",
        r"^Objeto\s*:\s*apartamento residencial\s+(.+)",
        r"^Objeto\s*:\s*imóvel rural denominado\s+(.+)",
        r"^Objeto\s*:\s*imóvel rural\s+(.+)",
        r"^Bem avaliando\s*:\s*apartamento no\s+(.+)",
    ]

    for pattern in patterns:
        match = find_match(pattern, content)

        if match:
            address = get_text(match)

            if pattern.startswith(r"^Objeto\s*:\s*imóvel rural"):
                address = re.sub(
                    r"^Sítio\s+([^.,]+)",
                    r"Sítio \1",
                    address,
                    flags=re.IGNORECASE,
                )

            return address

    match = find_match(
        r"vistoriamos a sala comercial\s+\d+,\s*([^\n]+)",
        content,
    )

    if match:
        return get_text(match)

    match = find_match(
        r"^Apartamento residencial na\s+([^\n]+)",
        content,
    )

    if match:
        return get_text(match)

    return None


def extract_report_fields(content: str) -> dict:
    private_area = extract_area(
        r"Área (?:privativa|privada)\s*:?\s*([\d.,]+)\s*m?²?",
        content,
    )

    useful_area = extract_area(
        r"Área útil\s*:?\s*([\d.,]+)\s*m?²?",
        content,
    )

    built_area = extract_area(
        r"(?:Área (?:construída|edificada)|"
        r"Benfeitorias construídas)"
        r"\s*(?:aproximada)?\s*(?:de)?\s*:?\s*"
        r"([\d.,]+)\s*m\s*²?",
        content,
    )

    if built_area is None:
        built_area = extract_area(
            r"([\d.,]+)\s*m\s*²?\s+de área construída",
            content,
        )

    if built_area is None:
        built_area = extract_area(
            r"área construída\s+(?:de\s+)?([\d.,]+)\s*m\s*²?",
            content,
        )

    covered_area = extract_area(
        r"Área coberta\s*:?\s*([\d.,]+)\s*m?²?",
        content,
    )

    land_patterns = [
        r"(?:Área do terreno|Área territorial|Área do lote)"
        r"\s*:?\s*(?:de\s+)?([\d.,]+)\s*(m²|m2|ha)?",
        r"Superfície\s*:?\s*([\d.,]+)\s*(m²|m2|ha)?",
        r"Terreno\s*:\s*([\d.,]+)\s*(m²|m2|ha)?",
        r"Terreno\s+(?:com|de)\s+([\d.,]+)\s*(m²|m2|ha)\b",
        r"Lote\s+(?:com|de)\s+([\d.,]+)\s*(m²|m2|ha)\b",
    ]

    land_area = None

    for pattern in land_patterns:
        land_match = find_match(pattern, content)

        if land_match:
            land_area = normalize_number(land_match.group(1))
            unit = (land_match.group(2) or "").lower()

            if unit == "ha" and land_area is not None:
                land_area *= 10000

            break

    total_area = extract_area(
        r"Área total\s*:?\s*([\d.,]+)\s*m?²?",
        content,
    )

    alternative_total_area = extract_area(
        r"tabela interna registra\s+([\d.,]+)\s*m\s*²?",
        content,
    )

    construction_year_match = find_match(
        r"(?:Ano de construção|Ano das edificações|Ano informado|"
        r"Ano de conclusão|Construção|Construído em|Construída em|"
        r"Ano de construção informado pelo proprietário|Ano)"
        r"[^:\n]*\s*:?\s*(?:pelo proprietário:\s*)?(\d{4})\b",
        content,
    )

    if not construction_year_match:
        construction_year_match = find_match(
            r"Imóvel com\s+(\d{4})\s+de construção",
            content,
        )

    appraisal_value_match = find_match(
        r"(?:Valor de avaliação|Valor de mercado|Valor indicado|"
        r"Valor apurado|Valor venal adotado|Valor total da avaliação|"
        r"Estimativa de mercado|Avaliação final|Avaliação apresentada|"
        r"Valor estimado|Valor indicado pelo método comparativo|"
        r"Preço/valor de avaliação|Preço|Avaliação)"
        r"[^\n]*?(?:R\$\s*)"
        r"([\d.]+(?:,\d{2})?|\d+(?:\.\d{1,2})?)",
        content,
    )

    registry_match = find_match(
        r"^(?:Matrícula|Registro imobiliário|Registro)" r"\s*:?\s*(.+)",
        content,
    )

    registry = get_text(registry_match)

    if registry:
        if re.search(r"\bnão apresentada\b", registry, re.IGNORECASE):
            registry = None
        else:
            registry = (
                re.sub(
                    r"^(?:Matrícula|Registro imobiliário|Registro)"
                    r"\s*(?:n[º°.]?\s*)?:?\s*",
                    "",
                    registry,
                    flags=re.IGNORECASE,
                )
                .strip()
                .rstrip(".")
            )

    onus_match = find_match(
        r"^(?:Ônus e restrições|Ônus reais|Ônus|Gravames|Certidão)" r"\s*:?\s*([^\n]+)",
        content,
    )

    onus = get_text(onus_match)

    if onus is None:
        onus_patterns = [
            r"Não consta informação sobre ônus\.?",
            r"Não há menção a ônus\.?",
            r"A certidão consultada informa hipoteca ativa\.?",
            r"Consta alienação fiduciária[^\n]*",
            r"Há penhora averbada[^\n]*",
            r"A certidão indica inexistência de ônus reais[^\n]*",
        ]

        for pattern in onus_patterns:
            onus_match = find_match(pattern, content)

            if onus_match:
                onus = onus_match.group(0).strip().rstrip(".")
                break

    professional_match = find_match(
        r"^(?:Responsável técnico|Responsável pelo trabalho|"
        r"Avaliadora responsável|Responsável|Avaliador|Avaliadora|"
        r"Perito avaliador|Perita|RT|Elaborado por)"
        r"\s*:?\s*(.+)",
        content,
    )

    return {
        "tipo_imovel": extract_property_type(content),
        "endereco": extract_address(content),
        "areas_m2": {
            "privativa": private_area,
            "util": useful_area,
            "construida": built_area,
            "coberta": covered_area,
            "terreno": land_area,
            "total": total_area,
        },
        "area_total_alternativa_m2": alternative_total_area,
        "ano_construcao": (
            int(construction_year_match.group(1)) if construction_year_match else None
        ),
        "valor_avaliacao": normalize_number(
            appraisal_value_match.group(1) if appraisal_value_match else None
        ),
        "matricula": registry,
        "onus": onus,
        "data_vistoria": extract_date(content),
        "responsavel": get_text(professional_match),
    }
