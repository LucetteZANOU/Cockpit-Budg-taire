from dataclasses import dataclass
from decimal import Decimal

from app.services.variance import (
    compute_ecart_pourcentage,
    compute_ecart_valeur,
    summarize_variances,
)


@dataclass
class FakeCentreCout:
    nom: str


@dataclass
class FakeLine:
    centre_cout: FakeCentreCout
    montant_prevu: Decimal
    montant_realise: Decimal
    montant_reestime: Decimal | None = None


def test_compute_ecart_valeur() -> None:
    assert compute_ecart_valeur(Decimal("1000"), Decimal("800")) == Decimal("-200")
    assert compute_ecart_valeur(Decimal("1000"), Decimal("1200")) == Decimal("200")


def test_compute_ecart_pourcentage() -> None:
    assert compute_ecart_pourcentage(Decimal("1000"), Decimal("800")) == Decimal("-20")


def test_compute_ecart_pourcentage_zero_reference() -> None:
    assert compute_ecart_pourcentage(Decimal("0"), Decimal("500")) is None


def test_summarize_variances() -> None:
    lines = [
        FakeLine(FakeCentreCout("Marketing"), Decimal("1000"), Decimal("800")),
        FakeLine(FakeCentreCout("Marketing"), Decimal("500"), Decimal("500")),
        FakeLine(FakeCentreCout("Ventes"), Decimal("300"), Decimal("400")),
    ]
    summary = summarize_variances(lines)

    assert summary.total_prevu == Decimal("1800")
    assert summary.total_realise == Decimal("1700")
    assert summary.ecart_valeur == Decimal("-100")
    assert summary.total_reestime is None
    assert len(summary.par_centre_cout) == 2

    marketing = next(c for c in summary.par_centre_cout if c.centre_cout == "Marketing")
    assert marketing.total_prevu == Decimal("1500")
    assert marketing.total_realise == Decimal("1300")


def test_summarize_variances_with_reestime() -> None:
    lines = [
        FakeLine(FakeCentreCout("Marketing"), Decimal("1000"), Decimal("800"), Decimal("1100")),
        FakeLine(FakeCentreCout("Marketing"), Decimal("500"), Decimal("500"), Decimal("500")),
    ]
    summary = summarize_variances(lines)

    assert summary.total_reestime == Decimal("1600")
    assert summary.ecart_reestime_valeur == Decimal("100")

    marketing = summary.par_centre_cout[0]
    assert marketing.total_reestime == Decimal("1600")
    assert marketing.ecart_reestime_valeur == Decimal("100")


def test_summarize_variances_partial_reestime_is_none() -> None:
    lines = [
        FakeLine(FakeCentreCout("Marketing"), Decimal("1000"), Decimal("800"), Decimal("1100")),
        FakeLine(FakeCentreCout("Marketing"), Decimal("500"), Decimal("500"), None),
    ]
    summary = summarize_variances(lines)

    assert summary.total_reestime is None
    assert summary.par_centre_cout[0].total_reestime is None
