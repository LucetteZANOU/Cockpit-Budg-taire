from collections.abc import Iterable
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

TWO_PLACES = Decimal("0.01")


def compute_ecart_valeur(reference: Decimal, compare: Decimal) -> Decimal:
    return compare - reference


def compute_ecart_pourcentage(reference: Decimal, compare: Decimal) -> Decimal | None:
    if reference == 0:
        return None
    ecart_pct = (compare - reference) / reference * 100
    return ecart_pct.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)


@dataclass
class CentreCoutSummary:
    centre_cout: str
    total_prevu: Decimal
    total_reestime: Decimal | None
    total_realise: Decimal
    ecart_valeur: Decimal
    ecart_pourcentage: Decimal | None
    ecart_reestime_valeur: Decimal | None
    ecart_reestime_pourcentage: Decimal | None


@dataclass
class VarianceSummary:
    total_prevu: Decimal
    total_reestime: Decimal | None
    total_realise: Decimal
    ecart_valeur: Decimal
    ecart_pourcentage: Decimal | None
    ecart_reestime_valeur: Decimal | None
    ecart_reestime_pourcentage: Decimal | None
    par_centre_cout: list[CentreCoutSummary]


def _sum_reestime(lines: list) -> Decimal | None:
    if any(line.montant_reestime is None for line in lines):
        return None
    return sum((line.montant_reestime for line in lines), Decimal(0))


def summarize_variances(lines: Iterable) -> VarianceSummary:
    by_centre_cout: dict[str, list] = {}
    for line in lines:
        by_centre_cout.setdefault(line.centre_cout.nom, []).append(line)

    par_centre_cout = []
    total_prevu = Decimal(0)
    total_realise = Decimal(0)
    all_lines: list = []

    for centre_cout, cc_lines in by_centre_cout.items():
        cc_prevu = sum((line.montant_prevu for line in cc_lines), Decimal(0))
        cc_realise = sum((line.montant_realise for line in cc_lines), Decimal(0))
        cc_reestime = _sum_reestime(cc_lines)
        par_centre_cout.append(
            CentreCoutSummary(
                centre_cout=centre_cout,
                total_prevu=cc_prevu,
                total_reestime=cc_reestime,
                total_realise=cc_realise,
                ecart_valeur=compute_ecart_valeur(cc_prevu, cc_realise),
                ecart_pourcentage=compute_ecart_pourcentage(cc_prevu, cc_realise),
                ecart_reestime_valeur=(
                    compute_ecart_valeur(cc_prevu, cc_reestime) if cc_reestime is not None else None
                ),
                ecart_reestime_pourcentage=(
                    compute_ecart_pourcentage(cc_prevu, cc_reestime)
                    if cc_reestime is not None
                    else None
                ),
            )
        )
        total_prevu += cc_prevu
        total_realise += cc_realise
        all_lines.extend(cc_lines)

    total_reestime = _sum_reestime(all_lines)

    return VarianceSummary(
        total_prevu=total_prevu,
        total_reestime=total_reestime,
        total_realise=total_realise,
        ecart_valeur=compute_ecart_valeur(total_prevu, total_realise),
        ecart_pourcentage=compute_ecart_pourcentage(total_prevu, total_realise),
        ecart_reestime_valeur=(
            compute_ecart_valeur(total_prevu, total_reestime)
            if total_reestime is not None
            else None
        ),
        ecart_reestime_pourcentage=(
            compute_ecart_pourcentage(total_prevu, total_reestime)
            if total_reestime is not None
            else None
        ),
        par_centre_cout=par_centre_cout,
    )
