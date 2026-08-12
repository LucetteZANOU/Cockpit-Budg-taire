from collections.abc import Iterable
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

TWO_PLACES = Decimal("0.01")


def compute_ecart_valeur(prevu: Decimal, realise: Decimal) -> Decimal:
    return realise - prevu


def compute_ecart_pourcentage(prevu: Decimal, realise: Decimal) -> Decimal | None:
    if prevu == 0:
        return None
    ecart_pct = (realise - prevu) / prevu * 100
    return ecart_pct.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)


@dataclass
class CategorySummary:
    categorie: str
    total_prevu: Decimal
    total_realise: Decimal
    ecart_valeur: Decimal
    ecart_pourcentage: Decimal | None


@dataclass
class VarianceSummary:
    total_prevu: Decimal
    total_realise: Decimal
    ecart_valeur: Decimal
    ecart_pourcentage: Decimal | None
    par_categorie: list[CategorySummary]


def summarize_variances(lines: Iterable) -> VarianceSummary:
    by_categorie: dict[str, list] = {}
    for line in lines:
        by_categorie.setdefault(line.categorie, []).append(line)

    par_categorie = []
    total_prevu = Decimal(0)
    total_realise = Decimal(0)

    for categorie, cat_lines in by_categorie.items():
        cat_prevu = sum((line.montant_prevu for line in cat_lines), Decimal(0))
        cat_realise = sum((line.montant_realise for line in cat_lines), Decimal(0))
        par_categorie.append(
            CategorySummary(
                categorie=categorie,
                total_prevu=cat_prevu,
                total_realise=cat_realise,
                ecart_valeur=compute_ecart_valeur(cat_prevu, cat_realise),
                ecart_pourcentage=compute_ecart_pourcentage(cat_prevu, cat_realise),
            )
        )
        total_prevu += cat_prevu
        total_realise += cat_realise

    return VarianceSummary(
        total_prevu=total_prevu,
        total_realise=total_realise,
        ecart_valeur=compute_ecart_valeur(total_prevu, total_realise),
        ecart_pourcentage=compute_ecart_pourcentage(total_prevu, total_realise),
        par_categorie=par_categorie,
    )
