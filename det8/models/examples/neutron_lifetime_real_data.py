"""Real neutron-lifetime measurement plot and RET assimilation.

This module holds the published neutron-lifetime measurements (not synthetic
roundings) and renders the beam-vs-bottle discrepancy, highlighting the J-PARC
electron-beam result that agrees with the bottle values rather than the proton
beam values. It also runs the aggregate Gaussian RET adapter on the three
modern precision values so the real-data posterior can be reported alongside
the plot.

The dataset is a curated, cited compilation. Total uncertainties are combined
in quadrature; the J-PARC systematic is asymmetric and is shown as such. The
averages are quoted from the J-PARC 2024 comparison (beam/proton 888.0+/-2.0 s,
bottle 878.4+/-0.5 s).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from det8.models.examples.neutron_lifetime import (
    assimilate_published_records,
)


@dataclass(frozen=True)
class Measurement:
    label: str
    year: float
    lifetime_s: float
    uncertainty_s: float
    uncertainty_down_s: float | None = None
    method: str = "bottle"
    readout: str = "survivor"
    citation: str = ""


def measurements() -> list[Measurement]:
    return [
        Measurement("Byrne 1996", 1996, 889.2, 4.8, method="beam", readout="proton",
                    citation="Phys. Rev. Lett. 76, 2849 (1996)"),
        Measurement("Serebrov 2005", 2005, 878.5, 0.8, method="bottle",
                    citation="Phys. Lett. B 605, 72 (2005)"),
        Measurement("Pichlmaier 2010", 2010, 880.7, 1.6, method="bottle",
                    citation="Phys. Lett. B 693, 221 (2010)"),
        Measurement("Steyerl 2012", 2012, 882.5, 1.6, method="bottle",
                    citation="Phys. Rev. C 85, 065503 (2012)"),
        Measurement("Yue 2013 (NIST)", 2013, 887.7, 2.2, method="beam", readout="proton",
                    citation="Phys. Rev. Lett. 111, 222501 (2013)"),
        Measurement("Arzumanov 2015", 2015, 880.2, 1.2, method="bottle",
                    citation="Phys. Lett. B 745, 79 (2015)"),
        Measurement("UCN\u03c4 2018", 2018, 877.7, 0.75, method="bottle",
                    citation="Science 360, 627 (2018)"),
        Measurement("UCN\u03c4 2021", 2021, 877.75, 0.36, method="bottle",
                    citation="Phys. Rev. Lett. 127, 162501 (2021)"),
        Measurement("J-PARC 2024", 2024, 877.2, 4.35, uncertainty_down_s=3.98,
                    method="beam", readout="electron",
                    citation="arXiv:2412.19519"),
    ]


def _errorbar(measurement: Measurement):
    if measurement.uncertainty_down_s is not None:
        return (
            [measurement.uncertainty_down_s],
            [measurement.uncertainty_s],
        )
    return ([measurement.uncertainty_s], [measurement.uncertainty_s])


def plot_neutron_lifetime(output_path: Path) -> Path:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    data = measurements()
    bottle = [m for m in data if m.method == "bottle"]
    beam_proton = [m for m in data if m.method == "beam" and m.readout == "proton"]
    beam_electron = [m for m in data if m.method == "beam" and m.readout == "electron"]

    fig, ax = plt.subplots(figsize=(9, 5.5))

    def scatter(items, marker, color, label, year_offset=0.0):
        years = [m.year + year_offset for m in items]
        values = [m.lifetime_s for m in items]
        down = [m.uncertainty_down_s if m.uncertainty_down_s is not None
                else m.uncertainty_s for m in items]
        up = [m.uncertainty_s for m in items]
        ax.errorbar(
            years, values,
            yerr=[down, up], fmt=marker, color=color, label=label,
            markersize=7, capsize=3, elinewidth=1.2, linestyle="none",
        )
        for m, year in zip(items, years):
            ax.annotate(
                m.label, (year, m.lifetime_s), textcoords="offset points",
                xytext=(0, 7), ha="center", fontsize=7,
            )

    scatter(bottle, "o", "#1f77b4", "bottle (trap)", year_offset=0.0)
    scatter(beam_proton, "s", "#d62728", "beam, proton", year_offset=0.35)
    scatter(beam_electron, "D", "#2ca02c", "beam, electron (J-PARC)", year_offset=0.35)

    ax.axhspan(878.4 - 0.5, 878.4 + 0.5, color="#1f77b4", alpha=0.10)
    ax.axhline(878.4, color="#1f77b4", alpha=0.55, linewidth=1, linestyle="--")
    ax.axhspan(888.0 - 2.0, 888.0 + 2.0, color="#d62728", alpha=0.10)
    ax.axhline(888.0, color="#d62728", alpha=0.55, linewidth=1, linestyle="--")
    ax.text(2024.6, 878.4, "bottle avg 878.4\u00b10.5 s", color="#1f77b4", fontsize=8,
            va="center", ha="left")
    ax.text(2024.6, 888.0, "beam/proton avg 888.0\u00b12.0 s", color="#d62728",
            fontsize=8, va="center", ha="left")

    ax.set_xlabel("publication year")
    ax.set_ylabel("neutron lifetime $\\tau_n$ (s)")
    ax.set_title("Neutron lifetime: beam vs bottle discrepancy")
    ax.set_xlim(1994, 2026.5)
    ax.set_ylim(875.5, 895.0)
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)
    return output_path


def run_neutron_lifetime_real_data(output_path: str | Path | None = None) -> dict:
    output = Path(output_path) if output_path else Path(
        "docs/neutron_lifetime_measurements.png"
    )
    plot_path = plot_neutron_lifetime(output)

    posterior, _ = assimilate_published_records()
    return {
        "measurements": [
            {
                "label": m.label,
                "year": m.year,
                "lifetime_s": m.lifetime_s,
                "uncertainty_s": m.uncertainty_s,
                "uncertainty_down_s": m.uncertainty_down_s,
                "method": m.method,
                "readout": m.readout,
                "citation": m.citation,
            }
            for m in measurements()
        ],
        "averages_s": {
            "bottle": 878.4,
            "bottle_uncertainty": 0.5,
            "beam_proton": 888.0,
            "beam_proton_uncertainty": 2.0,
        },
        "ret_real_data_posterior": dict(posterior.model_weights),
        "plot_path": str(plot_path),
    }


if __name__ == "__main__":
    result = run_neutron_lifetime_real_data()
    print(json.dumps(
        {
            "measurements": result["measurements"],
            "averages_s": result["averages_s"],
            "ret_real_data_posterior": result["ret_real_data_posterior"],
            "plot_path": result["plot_path"],
        },
        indent=2,
    ))
