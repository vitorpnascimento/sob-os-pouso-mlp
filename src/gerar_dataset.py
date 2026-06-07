"""
Geração do dataset sintético de pouso de aeronave.

MODELO FÍSICO (movimento variado NÃO uniformemente — aceleração não constante):

Durante o pouso, após o toque (touchdown), a aeronave desacelera por três forças
que dependem da velocidade, logo a aceleração NÃO é constante:

    m * dv/dt = -F_brake - F_drag(v) - F_reverse(v)

onde:
    F_drag(v)    = 0.5 * rho * Cd * A * v^2      (arrasto aerodinâmico ~ v^2)
    F_reverse(v) = k_rev * v                     (empuxo reverso ~ proporcional a v)
    F_brake      = mu * m * g                    (frenagem das rodas ~ aprox. constante)

Como F_drag e F_reverse dependem de v, a desaceleração a(t) = dv/dt varia ao longo
do tempo -> é um Movimento Variado NÃO Uniformemente. As equações do M.U.V.
(a = const) NÃO descrevem este sistema.

A equação diferencial é integrada numericamente (Runge-Kutta 4ª ordem).

5 ATRIBUTOS do dataset (conforme enunciado):
    1. t      -> tempo desde o touchdown (s)
    2. v      -> velocidade instantânea (m/s)
    3. x      -> distância percorrida na pista (m)
    4. a      -> aceleração instantânea (m/s^2), negativa (desaceleração)
    5. massa  -> massa da aeronave nesse pouso (varia entre pousos) (kg)

ALVO (y):
    dist_restante -> distância de pista que ainda falta até parar (m)
    (é o que o instrumento embarcado precisaria inferir em tempo real)
"""

import numpy as np
import pandas as pd

# Constantes físicas
G = 9.81          # gravidade (m/s^2)
RHO = 1.225       # densidade do ar ao nível do mar (kg/m^3)


def aceleracao(v, m, params):
    """Aceleração (desaceleração) instantânea. Depende de v -> não constante."""
    Cd = params["Cd"]
    A = params["A"]
    k_rev = params["k_rev"]
    mu = params["mu"]
    F_drag = 0.5 * RHO * Cd * A * v ** 2
    F_reverse = k_rev * v
    F_brake = mu * m * G
    return -(F_drag + F_reverse + F_brake) / m  # negativa


def simular_pouso(v0, m, params, dt=0.05, v_min=0.5):
    """Integra a EDO por RK4 até a aeronave quase parar. Retorna arrays t,v,x,a."""
    t_list, v_list, x_list, a_list = [], [], [], []
    t, v, x = 0.0, v0, 0.0
    while v > v_min and t < 120:
        a = aceleracao(v, m, params)
        t_list.append(t); v_list.append(v); x_list.append(x); a_list.append(a)
        # RK4 para v (x é integral de v)
        k1v = aceleracao(v, m, params)
        k1x = v
        k2v = aceleracao(v + 0.5 * dt * k1v, m, params)
        k2x = v + 0.5 * dt * k1v
        k3v = aceleracao(v + 0.5 * dt * k2v, m, params)
        k3x = v + 0.5 * dt * k2v
        k4v = aceleracao(v + dt * k3v, m, params)
        k4x = v + dt * k3v
        v = v + (dt / 6.0) * (k1v + 2 * k2v + 2 * k3v + k4v)
        x = x + (dt / 6.0) * (k1x + 2 * k2x + 2 * k3x + k4x)
        t += dt
    return (np.array(t_list), np.array(v_list),
            np.array(x_list), np.array(a_list))


def gerar(n_linhas=6_000_000, seed=42):
    """Gera o dataset com ~n_linhas simulando muitos pousos com parâmetros variados."""
    rng = np.random.default_rng(seed)
    Ts, Vs, Xs, As, Ms, Yr = [], [], [], [], [], []
    total = 0
    while total < n_linhas:
        # parâmetros variando por pouso (aeronave/condição diferente)
        v0 = rng.uniform(60, 80)        # velocidade de toque ~ 216-288 km/h
        m = rng.uniform(60000, 80000)   # massa (kg) tipo narrow-body
        params = {
            "Cd": rng.uniform(0.08, 0.12),
            "A": rng.uniform(120, 140),     # área de referência (m^2)
            "k_rev": rng.uniform(800, 1200),
            "mu": rng.uniform(0.25, 0.40),  # coef. frenagem (depende da pista)
        }
        t, v, x, a = simular_pouso(v0, m, params)
        if len(t) < 5:
            continue
        x_total = x[-1]
        dist_restante = x_total - x   # alvo
        Ts.append(t); Vs.append(v); Xs.append(x); As.append(a)
        Ms.append(np.full_like(t, m)); Yr.append(dist_restante)
        total += len(t)

    df = pd.DataFrame({
        "t": np.concatenate(Ts),
        "v": np.concatenate(Vs),
        "x": np.concatenate(Xs),
        "a": np.concatenate(As),
        "massa": np.concatenate(Ms),
        "dist_restante": np.concatenate(Yr),
    })
    return df.iloc[:n_linhas].reset_index(drop=True)


if __name__ == "__main__":
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 6_000_000
    print(f"Gerando dataset com ~{n:,} linhas...")
    df = gerar(n)
    print(df.head())
    print(f"Linhas: {len(df):,} | Colunas: {list(df.columns)}")
    df.to_parquet("/home/claude/projeto_so/outputs/dataset_pouso.parquet")
    print("Salvo em outputs/dataset_pouso.parquet")
