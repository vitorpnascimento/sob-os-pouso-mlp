"""
Rede Neural MLP simples implementada do ZERO em NumPy.

Arquitetura (conforme enunciado):
    - 1 camada oculta
    - 1 camada de saída
    - função de transferência SIGMOIDAL em AMBAS as camadas

O objetivo do trabalho é comparar o efeito do PADRÃO NUMÉRICO usado nos cálculos:

    * float64  -> ponto flutuante de dupla precisão (referência de qualidade)
    * int8     -> inteiro de 8 bits via aritmética de PONTO FIXO quantizado

Em sistemas embarcados (instrumentos de aeronave), usar int8 economiza memória e
acelera o processamento, mas a faixa dinâmica minúscula (-128..127) introduz erro
de quantização severo. Aqui simulamos isso de forma controlada e medimos o impacto
em qualidade (MSE / MAE / R2), número de épocas e tempo total.
"""

import time
import numpy as np


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))


def sigmoid_deriv_from_output(s):
    return s * (1.0 - s)


# ----------------------------------------------------------------------------
# Quantização de ponto fixo para int8
# ----------------------------------------------------------------------------
def quantizar_int8(x, escala):
    """Converte float -> int8 usando uma escala fixa, com saturação em [-127,127]."""
    q = np.round(x * escala)
    q = np.clip(q, -127, 127)
    return q.astype(np.int8)


def desquantizar(q, escala):
    """int8 -> float (volta ao domínio real para poder calcular)."""
    return q.astype(np.float64) / escala


class MLP:
    """MLP 1 camada oculta. modo='float64' (referência) ou 'int8' (ponto fixo)."""

    def __init__(self, n_in, n_hidden, modo="float64", escala=64.0, seed=0):
        self.modo = modo
        self.escala = escala  # quantos níveis int por unidade real
        rng = np.random.default_rng(seed)
        # Inicialização pequena (Xavier-ish)
        self.W1 = rng.normal(0, 1.0 / np.sqrt(n_in), size=(n_in, n_hidden))
        self.b1 = np.zeros(n_hidden)
        self.W2 = rng.normal(0, 1.0 / np.sqrt(n_hidden), size=(n_hidden, 1))
        self.b2 = np.zeros(1)

    def _maybe_quant(self, M):
        """No modo int8, simula o efeito de armazenar/usar pesos em int8:
        quantiza e desquantiza, introduzindo erro de quantização nos cálculos."""
        if self.modo == "int8":
            return desquantizar(quantizar_int8(M, self.escala), self.escala)
        return M

    def forward(self, X):
        W1 = self._maybe_quant(self.W1)
        W2 = self._maybe_quant(self.W2)
        self.z1 = X @ W1 + self.b1
        self.a1 = sigmoid(self.z1)            # sigmoid na camada oculta
        if self.modo == "int8":
            # ativação 0..1 mapeada em poucos níveis int8 (baixa resolução real):
            # usamos 32 níveis (5 bits efetivos) para a ativação embarcada
            niveis = 32.0
            self.a1 = desquantizar(quantizar_int8(self.a1, niveis), niveis)
        self.z2 = self.a1 @ W2 + self.b2
        self.a2 = sigmoid(self.z2)            # sigmoid na camada de saída
        return self.a2

    def train(self, X, y, epocas=200, lr=0.5, paciencia=15, verbose=False):
        y = y.reshape(-1, 1)
        hist = []
        melhor = np.inf
        sem_melhora = 0
        t0 = time.perf_counter()
        for ep in range(epocas):
            out = self.forward(X)
            erro = out - y
            mse = float(np.mean(erro ** 2))
            hist.append(mse)
            # backprop
            d2 = erro * sigmoid_deriv_from_output(out)
            dW2 = self.a1.T @ d2 / len(X)
            db2 = d2.mean(axis=0)
            d1 = (d2 @ self._maybe_quant(self.W2).T) * sigmoid_deriv_from_output(self.a1)
            dW1 = X.T @ d1 / len(X)
            db1 = d1.mean(axis=0)
            self.W1 -= lr * dW1; self.b1 -= lr * db1
            self.W2 -= lr * dW2; self.b2 -= lr * db2
            # early stopping
            if mse < melhor - 1e-6:
                melhor = mse; sem_melhora = 0
            else:
                sem_melhora += 1
                if sem_melhora >= paciencia:
                    if verbose: print(f"  early stop ep {ep}")
                    break
        tempo = time.perf_counter() - t0
        return {"hist": hist, "epocas": ep + 1, "tempo_s": tempo, "mse_final": hist[-1]}

    def predict(self, X):
        return self.forward(X)
