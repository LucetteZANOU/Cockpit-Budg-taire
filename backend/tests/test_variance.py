from dataclasses import dataclass
from decimal import Decimal

from app.services.variance import (
    compute_ecart_pourcentage,
    compute_ecart_valeur,
    summarize_variances,
)


@dataclass
class FakeLine:
    categorie: str
    montant_prevu: Decimal
    montant_realise: Decimal


def test_compute_ecart_valeur() -> None:
    assert compute_ecart_valeur(Decimal("1000"), Decimal("800")) == Decimal("-200")
    assert compute_ecart_valeur(Decimal("1000"), Decimal("1200")) == Decimal("200")


def test_compute_ecart_pourcentage() -> None:
    assert compute_ecart_pourcentage(Decimal("1000"), Decimal("800")) == Decimal("-20")


def test_compute_ecart_pourcentage_zero_prevu() -> None:
    assert compute_ecart_pourcentage(Decimal("0"), Decimal("500")) is None


def test_summarize_variances() -> None:
    lines = [
        FakeLine("Marketing", Decimal("1000"), Decimal("800")),
        FakeLine("Marketing", Decimal("500"), Decimal("500")),
        FakeLine("Ventes", Decimal("300"), Decimal("400")),
    ]
    summary = summarize_variances(lines)

    assert summary.total_prevu == Decimal("1800")
    assert summary.total_realise == Decimal("1700")
    assert summary.ecart_valeur == Decimal("-100")
    assert len(summary.par_categorie) == 2

    marketing = next(c for c in summary.par_categorie if c.categorie == "Marketing")
    assert marketing.total_prevu == Decimal("1500")
    assert marketing.total_realise == Decimal("1300")
