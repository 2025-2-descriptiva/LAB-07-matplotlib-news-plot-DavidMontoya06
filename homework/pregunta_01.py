"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import os
from typing import Dict

import matplotlib.pyplot as plt
import pandas as pd


def _load_data(path: str) -> pd.DataFrame:
    """Leer CSV y usar la primera columna como índice (años)."""
    return pd.read_csv(path, index_col=0)


def _ensure_output_dir(path: str) -> None:
    """Crear carpeta si no existe (segura en Windows)."""
    os.makedirs(os.path.dirname(path), exist_ok=True)


def _style_axes(ax: plt.Axes) -> None:
    """Aplicar estilo minimalista a los ejes (sin spines ni eje y)."""
    ax.set_title("How people get their news", fontsize=16)
    # Ocultar spines no deseados y el eje Y para emular el ejemplo
    ax.spines["top"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.get_yaxis().set_visible(False)


def _plot_series(ax: plt.Axes, df: pd.DataFrame, colors: Dict[str, str], zorder: Dict[str, int], linewidths: Dict[str, int]) -> None:
    """Trazar cada columna del DataFrame como una línea con estilo predefinido."""
    for col in df.columns:
        ax.plot(df.index, df[col], color=colors[col], label=col, zorder=zorder[col], linewidth=linewidths[col])


def _annotate_endpoints(ax: plt.Axes, df: pd.DataFrame, colors: Dict[str, str], zorder: Dict[str, int]) -> None:
    """Añadir puntos y etiquetas en el primer y último año de la serie."""
    first_year = df.index[0]
    last_year = df.index[-1]

    for col in df.columns:
        # Punto y etiqueta al inicio
        ax.scatter(first_year, df.loc[first_year, col], color=colors[col], zorder=zorder[col])
        ax.text(
            first_year - 0.2,
            df.loc[first_year, col],
            f"{col} {df.loc[first_year, col]}%",
            color=colors[col],
            fontsize=8,
            ha="right",
            va="center",
            zorder=zorder[col],
        )

        # Punto y etiqueta al final
        ax.scatter(last_year, df.loc[last_year, col], color=colors[col], zorder=zorder[col])
        ax.text(
            last_year + 0.2,
            df.loc[last_year, col],
            f"{df.loc[last_year, col]}%",
            color=colors[col],
            fontsize=8,
            ha="left",
            va="center",
            zorder=zorder[col],
        )


def pregunta_01():
    """
    Siga las instrucciones del video https://youtu.be/qVdwpxG_JpE para
    generar el archivo `files/plots/news.png`.

    Un ejemplo de la grafica final esta ubicado en la raíz de
    este repo.

    El gráfico debe salvarse al archivo `files/plots/news.png`.

    """
    # Rutas de entrada/salida
    input_path = "files/input/news.csv"
    output_path = "files/plots/news.png"

    # Leer datos (el índice son los años)
    df = _load_data(input_path)

    # Configuraciones visuales (colores, orden y grosor por medio)
    colors = {
        "Newspaper": "grey",
        "Television": "dimgray",
        "Radio": "lightgrey",
        "Internet": "tab:blue",
    }

    zorder = {
        "Television": 1,
        "Newspaper": 1,
        "Internet": 2,
        "Radio": 1,
    }

    linewidths = {
        "Internet": 4,
        "Television": 2,
        "Newspaper": 2,
        "Radio": 2,
    }

    # Crear figura y eje
    fig, ax = plt.subplots(figsize=(8, 5))

    # Trazar series y decorar ejes
    _plot_series(ax, df, colors, zorder, linewidths)
    _style_axes(ax)

    # Anotar puntos iniciales y finales
    _annotate_endpoints(ax, df, colors, zorder)

    # Ajustar ticks x para mostrar los años
    ax.set_xticks(df.index)
    ax.set_xticklabels(df.index, ha="center")

    plt.tight_layout()

    # Guardar la figura en disco (asegurar carpeta)
    _ensure_output_dir(output_path)
    fig.savefig(output_path)
    plt.close(fig)