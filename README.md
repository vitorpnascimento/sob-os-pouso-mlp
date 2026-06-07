<div align="center">

### Influência de padrões numéricos (int8 vs float64) em rede neural MLP embarcada — Pouso aeronáutico

**Tá sob controle.**

Disciplina de **Sistemas Operacionais** · FIAP · Prof. Dr. José Gomes Salim Neto · Semestre 1/2026

</div>

---

##  Equipe
| Integrante | RM |
|------------|-----|
| Matheus Farias de Lima | RM554254 |
| Miguel Mauricio Parrado Patarroyo | RM554007 |
| Vitor Pinheiro Nascimento | RM553693 |
| Gabriel Leão | RM552642 |
| Pedro Henrique Nardaci Chaves | RM553988 |

---

## Sobre o projeto
Quantifica como o **padrão numérico** (`int8` vs `float64`) usado no treinamento de
uma rede neural MLP afeta a **qualidade da inferência**, o **número de épocas** e o
**tempo de processamento** de um sistema embarcado que estima, em tempo real, a
distância de pista restante durante o pouso de um jato comercial.

##  Questão de pesquisa
Em que medida a escolha entre `int8` e `float64` afeta a qualidade das inferências
e o tempo de processamento de um sistema embarcado pré-emptivo de pouso?

##  Modelo físico (movimento variado NÃO uniformemente)
A desaceleração no pouso depende da velocidade (arrasto ∝ v², reverso ∝ v, frenagem ≈ const.),
logo a aceleração **não é constante** — não se aplica o M.U.V. A EDO é integrada por
Runge-Kutta de 4ª ordem:

```
dv/dt = -[ ½·ρ·Cd·A·v² + k_rev·v + μ·m·g ] / m
dx/dt = v
```

## Dataset
Sintético, **6.000.000 de linhas**, 5 atributos: `t, v, x, a, massa` → alvo `dist_restante`.

## Rede neural
MLP do zero em NumPy: 1 camada oculta (16 neurônios) + 1 saída, **sigmoid em ambas**.
Treinada em `float64` (referência) e `int8` (ponto fixo quantizado).

## Resultados (resumo)
| Padrão | Épocas | MSE | MAE | R² | Tempo (min) |
|--------|--------|-----|-----|----|-------------|
| float64 | 1500 | 0.00255 | 0.0390 | 0.9397 | 0.266 |
| int8 | 1407 | 0.00291 | 0.0397 | 0.9312 | 0.294 |

O `float64` atinge maior qualidade; o `int8` sofre degradação controlada por ruído
de quantização. Discussão sobre pré-empção do SO no relatório PDF.

##  Como executar
```bash
pip install -r requirements.txt
cd src
python experimento.py    # treina, mede tempo e gera os gráficos
python gerar_pdf.py      # monta o relatório PDF com a identidade Sob Solutions
```
Variáveis opcionais: `N_LINHAS` (tamanho do dataset), `N_AMOSTRA` (amostra de treino).

## Estrutura
```
src/
  gerar_dataset.py   # modelo físico + geração do dataset sintético
  mlp.py             # MLP em NumPy (float64 e int8)
  experimento.py     # treino comparativo, métricas e gráficos
  gerar_pdf.py       # relatório PDF (branding Sob Solutions)
fonts/               # Nunito (fonte da marca)
figs/                # gráficos gerados
outputs/             # resultados.json e relatório PDF
```

---
<div align="center">

**Sob Solutions** · Brand Book v4.0 · 2025 · *Missão cumprida — tá sob controle.*

</div>
