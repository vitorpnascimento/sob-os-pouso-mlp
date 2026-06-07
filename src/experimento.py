"""
Experimento principal: compara os padrões numéricos int8 vs float64
no treinamento da MLP que infere a distância de pista restante no pouso.

Gera os gráficos exigidos no item 4:
    - curva de treinamento (MSE x épocas) para cada padrão
    - métricas finais (MSE, MAE, R2)
    - tempo total de processamento em MINUTOS
"""

import os, time, json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
_FONTDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fonts")
for _f in ["Nunito-Regular.ttf", "Nunito-Bold.ttf", "Nunito-ExtraBold.ttf", "Nunito-Black.ttf"]:
    _p = os.path.join(_FONTDIR, _f)
    if os.path.exists(_p):
        fm.fontManager.addfont(_p)
try:
    plt.rcParams["font.family"] = "Nunito"
except Exception:
    pass

from gerar_dataset import gerar
from mlp import MLP

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "outputs")
FIGS = os.path.join(BASE, "figs")
os.makedirs(OUT, exist_ok=True); os.makedirs(FIGS, exist_ok=True)

# ----------------------------------------------------------------------------
# Config: N_LINHAS controla o tamanho. O enunciado fala em 6 milhões.
# Treinar a MLP no batch inteiro de 6M em NumPy é pesado; treinamos em uma
# AMOSTRA representativa (subsample) e DOCUMENTAMOS o dataset completo de 6M.
# ----------------------------------------------------------------------------
N_LINHAS_DATASET = int(os.environ.get("N_LINHAS", "6000000"))
N_AMOSTRA_TREINO = int(os.environ.get("N_AMOSTRA", "40000"))
N_HIDDEN = 16
EPOCAS = 1500


def metricas(y_true, y_pred):
    y_true = y_true.ravel(); y_pred = y_pred.ravel()
    mse = float(np.mean((y_true - y_pred) ** 2))
    mae = float(np.mean(np.abs(y_true - y_pred)))
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    r2 = float(1 - ss_res / ss_tot)
    return {"MSE": mse, "MAE": mae, "R2": r2}


def main():
    print("=" * 60)
    print("1) GERANDO / CARREGANDO DATASET")
    print("=" * 60)
    path = os.path.join(OUT, "dataset_pouso.parquet")
    t0 = time.perf_counter()
    if os.path.exists(path):
        df = pd.read_parquet(path)
        print(f"Carregado: {len(df):,} linhas")
    else:
        df = gerar(N_LINHAS_DATASET)
        df.to_parquet(path)
        print(f"Gerado: {len(df):,} linhas em {time.perf_counter()-t0:.1f}s")

    # ----- exploração / tratamento / preparação (item 3) -----
    print("\nResumo estatístico:")
    print(df.describe().round(2).to_string())
    # remove eventuais NaN/inf
    df = df.replace([np.inf, -np.inf], np.nan).dropna()

    # amostra para treino (subsample aleatório representativo)
    dfa = df.sample(n=min(N_AMOSTRA_TREINO, len(df)), random_state=7).reset_index(drop=True)

    feats = ["t", "v", "x", "a", "massa"]
    X = dfa[feats].values.astype(np.float64)
    y = dfa["dist_restante"].values.astype(np.float64)

    # normalização min-max para [0,1] (preparação) — necessária p/ sigmoid e p/ int8
    Xmin, Xmax = X.min(0), X.max(0)
    Xn = (X - Xmin) / (Xmax - Xmin + 1e-12)
    ymin, ymax = y.min(), y.max()
    yn = (y - ymin) / (ymax - ymin + 1e-12)

    # split treino/teste
    n = len(Xn); idx = np.random.default_rng(7).permutation(n)
    corte = int(0.8 * n)
    tr, te = idx[:corte], idx[corte:]
    Xtr, Xte, ytr, yte = Xn[tr], Xn[te], yn[tr], yn[te]

    resultados = {}
    historico = {}
    print("\n" + "=" * 60)
    print("2) TREINAMENTO NOS DOIS PADRÕES NUMÉRICOS")
    print("=" * 60)
    for modo in ["float64", "int8"]:
        print(f"\n--- Treinando padrão: {modo} ---")
        escala = 16.0 if modo == "float64" else 8.0
        net = MLP(n_in=len(feats), n_hidden=N_HIDDEN, modo=modo, escala=escala, seed=1)
        info = net.train(Xtr, ytr, epocas=EPOCAS, lr=1.5, paciencia=60)
        pred = net.predict(Xte)
        m = metricas(yte, pred)
        resultados[modo] = {
            "epocas": info["epocas"],
            "tempo_min": info["tempo_s"] / 60.0,
            "tempo_s": info["tempo_s"],
            **m,
        }
        historico[modo] = info["hist"]
        print(f"  épocas={info['epocas']}  tempo={info['tempo_s']:.2f}s "
              f"({info['tempo_s']/60:.4f} min)")
        print(f"  MSE={m['MSE']:.5f}  MAE={m['MAE']:.5f}  R2={m['R2']:.4f}")

    # salva resultados
    with open(os.path.join(OUT, "resultados.json"), "w") as f:
        json.dump(resultados, f, indent=2)

    # ----------------------------------------------------------------
    # GRÁFICOS (item 4)
    # ----------------------------------------------------------------
    cor = {"float64": "#1B2A4A", "int8": "#2EC864"}

    # G1: curva de treinamento
    plt.figure(figsize=(8, 5))
    for modo in ["float64", "int8"]:
        plt.plot(historico[modo], label=f"{modo} ({resultados[modo]['epocas']} épocas)",
                 color=cor[modo], lw=2)
    plt.xlabel("Época"); plt.ylabel("MSE (escala normalizada)")
    plt.title("Curva de treinamento — int8 vs float64")
    plt.legend(); plt.grid(alpha=0.3); plt.tight_layout()
    plt.savefig(os.path.join(FIGS, "g1_curva_treino.png"), dpi=130); plt.close()

    # G2: métricas finais (barras)
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    for ax, met in zip(axes, ["MSE", "MAE", "R2"]):
        vals = [resultados["float64"][met], resultados["int8"][met]]
        ax.bar(["float64", "int8"], vals, color=[cor["float64"], cor["int8"]])
        ax.set_title(met); ax.grid(alpha=0.3, axis="y")
        for i, v in enumerate(vals):
            ax.text(i, v, f"{v:.4f}", ha="center", va="bottom", fontsize=9)
    plt.suptitle("Métricas finais por padrão numérico")
    plt.tight_layout(); plt.savefig(os.path.join(FIGS, "g2_metricas.png"), dpi=130); plt.close()

    # G3: tempo de processamento em minutos
    plt.figure(figsize=(6, 4.5))
    vals = [resultados["float64"]["tempo_min"], resultados["int8"]["tempo_min"]]
    plt.bar(["float64", "int8"], vals, color=[cor["float64"], cor["int8"]])
    for i, v in enumerate(vals):
        plt.text(i, v, f"{v:.4f} min", ha="center", va="bottom", fontsize=10)
    plt.ylabel("Tempo total (minutos)")
    plt.title("Tempo total de processamento")
    plt.grid(alpha=0.3, axis="y"); plt.tight_layout()
    plt.savefig(os.path.join(FIGS, "g3_tempo.png"), dpi=130); plt.close()

    # G4: exemplo do perfil físico de um pouso (mostra a(t) não constante)
    from gerar_dataset import simular_pouso
    t, v, x, a = simular_pouso(75, 70000,
                               {"Cd": 0.1, "A": 130, "k_rev": 1000, "mu": 0.32})
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    ax[0].plot(t, v, color="#2c7"); ax[0].set_title("Velocidade v(t)")
    ax[0].set_xlabel("t (s)"); ax[0].set_ylabel("v (m/s)"); ax[0].grid(alpha=0.3)
    ax[1].plot(t, a, color="#c72"); ax[1].set_title("Aceleração a(t) — NÃO constante")
    ax[1].set_xlabel("t (s)"); ax[1].set_ylabel("a (m/s²)"); ax[1].grid(alpha=0.3)
    plt.suptitle("Perfil físico de um pouso (movimento variado não uniformemente)")
    plt.tight_layout(); plt.savefig(os.path.join(FIGS, "g4_fisica.png"), dpi=130); plt.close()

    print("\n" + "=" * 60)
    print("RESULTADOS FINAIS")
    print("=" * 60)
    print(json.dumps(resultados, indent=2))
    print("\nGráficos salvos em figs/")
    return resultados


if __name__ == "__main__":
    main()
