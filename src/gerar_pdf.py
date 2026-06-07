"""Gera o relatório PDF final com a identidade visual da Sob Solutions (itens 1 a 5)."""
import json, os, random
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                Table, TableStyle, PageBreak, Frame, PageTemplate,
                                NextPageTemplate)
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGS = os.path.join(BASE, "figs")
OUT = os.path.join(BASE, "outputs")
FONTS = os.path.join(BASE, "fonts")
res = json.load(open(os.path.join(OUT, "resultados.json")))

pdfmetrics.registerFont(TTFont("Nunito", os.path.join(FONTS, "Nunito-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Nunito-Bold", os.path.join(FONTS, "Nunito-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Nunito-XBold", os.path.join(FONTS, "Nunito-ExtraBold.ttf")))
pdfmetrics.registerFont(TTFont("Nunito-Black", os.path.join(FONTS, "Nunito-Black.ttf")))

NAVY = colors.HexColor("#1B2A4A")
VERDE = colors.HexColor("#2EC864")
OFFWHITE = colors.HexColor("#F4F7F2")
AMARELO = colors.HexColor("#FFD232")
CINZA = colors.HexColor("#8B949E")

styles = getSampleStyleSheet()
def mk(name, **kw): styles.add(ParagraphStyle(name, **kw))
mk("Just", fontName="Nunito", alignment=TA_JUSTIFY, fontSize=10.5, leading=15.5, spaceAfter=8, textColor=NAVY)
mk("H1c", fontName="Nunito-XBold", fontSize=16, spaceBefore=4, spaceAfter=9, textColor=NAVY, leading=19)
mk("Kicker", fontName="Nunito-Bold", fontSize=9, textColor=VERDE, spaceBefore=14, spaceAfter=2, leading=11)
mk("H2c", fontName="Nunito-Bold", fontSize=12, spaceBefore=9, spaceAfter=4, textColor=VERDE)
mk("Cap", fontName="Nunito", fontSize=9, alignment=TA_CENTER, textColor=CINZA, spaceAfter=14, leading=12)
mk("Eq", fontName="Nunito-Bold", fontSize=11.5, alignment=TA_CENTER, spaceBefore=6, spaceAfter=6, textColor=NAVY)
mk("Quote", fontName="Nunito-Bold", fontSize=12, alignment=TA_LEFT, textColor=VERDE, leading=16, leftIndent=10, spaceBefore=6, spaceAfter=10)
mk("CoverTitle", fontName="Nunito-Black", fontSize=23, alignment=TA_LEFT, textColor=colors.white, leading=27)
mk("CoverSub", fontName="Nunito-Bold", fontSize=11, alignment=TA_LEFT, textColor=VERDE, leading=15)
mk("CoverWhite", fontName="Nunito", fontSize=10.5, alignment=TA_LEFT, textColor=colors.white, leading=15)
mk("CoverGreen", fontName="Nunito-XBold", fontSize=11, alignment=TA_LEFT, textColor=VERDE, leading=15)

S = styles
story = []
def P(t, st="Just"): story.append(Paragraph(t, S[st]))
def SP(h=8): story.append(Spacer(1, h))


def desenhar_capa(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(NAVY); canvas.rect(0, 0, w, h, fill=1, stroke=0)
    random.seed(7)
    canvas.setFillColor(colors.white)
    for _ in range(70):
        canvas.circle(random.uniform(0, w), random.uniform(h*0.45, h),
                      random.choice([0.6, 0.9, 1.2]), fill=1, stroke=0)
    canvas.setFillColor(AMARELO)
    for _ in range(8):
        canvas.circle(random.uniform(0, w), random.uniform(h*0.5, h), 1.4, fill=1, stroke=0)
    canvas.setStrokeColor(VERDE); canvas.setLineWidth(1.5)
    canvas.ellipse(w*0.30, h*0.60, w*0.95, h*0.78, fill=0, stroke=1)
    canvas.setFillColor(VERDE); canvas.circle(w*0.62, h*0.69, 26, fill=1, stroke=0)
    canvas.setFillColor(NAVY); canvas.circle(w*0.585, h*0.70, 5, fill=1, stroke=0)
    canvas.setFillColor(VERDE); canvas.rect(0, 0, w, 8, fill=1, stroke=0)
    canvas.restoreState()


def rodape(canvas, doc):
    canvas.saveState()
    w, _ = A4
    canvas.setFont("Nunito", 8); canvas.setFillColor(CINZA)
    canvas.drawString(2.2*cm, 1.2*cm, "Sob Solutions · Tá sob controle.")
    canvas.drawRightString(w-2.2*cm, 1.2*cm, "Sistemas Operacionais · FIAP · 2026")
    canvas.setStrokeColor(VERDE); canvas.setLineWidth(1)
    canvas.line(2.2*cm, 1.5*cm, w-2.2*cm, 1.5*cm)
    canvas.restoreState()


# ---- CAPA ----
story.append(NextPageTemplate("corpo"))   # páginas seguintes usam 'corpo'
SP(150)
P("SOB SOLUTIONS · BRAND-ALIGNED REPORT", "CoverSub")
SP(10)
P("Influência de padrões numéricos<br/>(int8 vs float64) em rede neural<br/>"
  "MLP embarcada de pouso aeronáutico", "CoverTitle")
SP(18)
P("Disciplina de Sistemas Operacionais &nbsp;·&nbsp; FIAP", "CoverWhite")
P("Prof. Dr. José Gomes Salim Neto &nbsp;·&nbsp; Semestre 1 / 2026", "CoverWhite")
SP(22)
P("Tá sob controle.", "CoverGreen")
SP(40)
P("EQUIPE", "CoverSub")
SP(4)
for nome in ["Matheus Farias de Lima — RM554254",
             "Miguel Mauricio Parrado Patarroyo — RM554007",
             "Vitor Pinheiro Nascimento — RM553693",
             "Gabriel Leão — RM552642",
             "Pedro Henrique Nardaci Chaves — RM553988"]:
    P(nome, "CoverWhite")
story.append(PageBreak())

# ---- 1 ----
P("01 — QUESTÃO DE PESQUISA E OBJETIVOS", "Kicker")
P("Questão de pesquisa, objetivo geral e objetivos específicos", "H1c")
P("<b>Questão de pesquisa.</b> Em que medida a escolha do padrão numérico de "
  "representação dos dados e dos cálculos de uma rede neural — inteiro de 8 bits "
  "(int8) versus ponto flutuante de dupla precisão (float64) — afeta a qualidade "
  "das inferências e o tempo de processamento de um sistema embarcado que estima, "
  "em tempo real, a distância de pista restante durante o pouso de um jato comercial?")
P("<b>Objetivo geral.</b> Quantificar, por meio do treinamento de uma rede neural "
  "MLP simples, o impacto do padrão numérico (int8 vs float64) sobre a qualidade "
  "preditiva (MSE, MAE, R²), o número de épocas e o tempo total de processamento.")
P("Objetivos específicos — sequência de execução", "H2c")
P("1) Modelar a física do pouso por equações de movimento variado não "
  "uniformemente (aceleração não constante) e gerar um dataset sintético de "
  "6 milhões de linhas com 5 atributos;<br/>"
  "2) Explorar, tratar e preparar (normalizar) os dados;<br/>"
  "3) Implementar do zero uma MLP (1 camada oculta + 1 camada de saída, sigmoid "
  "em ambas) operando em float64 e em int8;<br/>"
  "4) Treinar nos dois padrões, registrando épocas, métricas e tempo em minutos;<br/>"
  "5) Comparar graficamente os resultados;<br/>"
  "6) Discutir o papel da pré-empção do sistema operacional sobre os resultados.")

# ---- 2 ----
P("02 — CINEMÁTICA DO POUSO", "Kicker")
P("Equações cinemáticas do processo de pouso", "H1c")
P("Após o toque na pista (touchdown), a aeronave desacelera sob a ação de três "
  "forças. Como duas delas dependem da velocidade, a aceleração resultante "
  "<b>não é constante</b>, caracterizando movimento variado não uniformemente "
  "(equações do M.U.V. não se aplicam). A segunda lei de Newton fornece:")
P("m · (dv/dt) = − F<sub>frenagem</sub> − F<sub>arrasto</sub>(v) − F<sub>reverso</sub>(v)", "Eq")
P("com cada termo dado por:")
P("F<sub>arrasto</sub>(v) = ½ · ρ · C<sub>d</sub> · A · v<super>2</super>", "Eq")
P("F<sub>reverso</sub>(v) = k<sub>rev</sub> · v", "Eq")
P("F<sub>frenagem</sub> = μ · m · g", "Eq")
P("Substituindo, obtém-se a equação diferencial não linear da velocidade:")
P("dv/dt = − [ ½ρC<sub>d</sub>A·v<super>2</super> + k<sub>rev</sub>·v + μmg ] / m", "Eq")
P("A posição é a integral da velocidade, dx/dt = v. Como dv/dt depende de v "
  "(termos em v² e v), a desaceleração varia continuamente ao longo do pouso. "
  "O sistema foi integrado numericamente pelo método de Runge-Kutta de 4ª ordem "
  "(passo de 0,05 s). A figura abaixo evidencia que a aceleração a(t) não é "
  "constante, confirmando o regime de movimento variado não uniformemente exigido.")
story.append(Image(os.path.join(FIGS, "g4_fisica.png"), width=16*cm, height=5.8*cm))
P("Figura 1 — Perfil de velocidade e aceleração de um pouso simulado. "
  "A aceleração varia de ~ −4,9 a ~ −3,1 m/s².", "Cap")

# ---- 3 ----
story.append(PageBreak())
P("03 — DADOS", "Kicker")
P("Critérios de arrumação dos dados de pouso", "H1c")
P("<b>Natureza dos dados.</b> Dataset sintético gerado a partir do modelo físico "
  "da seção 2, simulando milhares de pousos com parâmetros variados (massa, "
  "coeficiente de arrasto, área de referência, coeficiente de frenagem da pista e "
  "ganho do reverso), totalizando 6.000.000 de linhas e 5 atributos.")
tbl_attr = [["Atributo", "Descrição", "Unidade"],
            ["t", "tempo desde o toque", "s"],
            ["v", "velocidade instantânea", "m/s"],
            ["x", "distância percorrida na pista", "m"],
            ["a", "aceleração instantânea (não constante)", "m/s²"],
            ["massa", "massa da aeronave no pouso", "kg"],
            ["dist_restante (alvo)", "distância de pista até parar", "m"]]
t = Table(tbl_attr, colWidths=[4.4*cm, 8*cm, 2.2*cm])
t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),colors.white),
    ("FONTNAME",(0,0),(-1,0),"Nunito-Bold"),("FONTNAME",(0,1),(-1,-1),"Nunito"),
    ("FONTSIZE",(0,0),(-1,-1),9),("GRID",(0,0),(-1,-1),0.4,CINZA),
    ("TEXTCOLOR",(0,1),(-1,-1),NAVY),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,OFFWHITE])]))
story.append(t); SP(10)
P("<b>Exploração.</b> Inspeção estatística (média, desvio, mínimos e máximos) de "
  "cada coluna e verificação da coerência física: velocidade decrescente de ~75 "
  "para 0 m/s, distância restante decrescente até zero e aceleração sempre negativa.")
P("<b>Tratamento.</b> Remoção de valores infinitos/ausentes (substituição de ±∞ por "
  "NaN seguida de descarte) e descarte de simulações degeneradas (com menos de 5 "
  "pontos de integração).")
P("<b>Preparação.</b> Para o treino seleciona-se uma amostra aleatória "
  "representativa (40.000 linhas) do dataset completo; as features são normalizadas "
  "por min-max para o intervalo [0,1] — passo essencial tanto para a função "
  "sigmoidal quanto para que a quantização int8 atue sobre uma faixa controlada. "
  "Divisão treino/teste de 80%/20%.")

# ---- 4 ----
P("04 — RESULTADOS", "Kicker")
P("Resultados do treinamento: int8 vs float64", "H1c")
P("A MLP (1 camada oculta com 16 neurônios, sigmoid em ambas as camadas) foi "
  "treinada com gradiente descendente e parada antecipada (early stopping). "
  "A tabela e os gráficos resumem os resultados.")
def fmt(m, k, casas=4): return f"{res[m][k]:.{casas}f}"
tbl = [["Padrão","Épocas","MSE","MAE","R²","Tempo (min)"],
       ["float64",str(res["float64"]["epocas"]),fmt("float64","MSE",5),fmt("float64","MAE"),fmt("float64","R2"),fmt("float64","tempo_min")],
       ["int8",str(res["int8"]["epocas"]),fmt("int8","MSE",5),fmt("int8","MAE"),fmt("int8","R2"),fmt("int8","tempo_min")]]
t2 = Table(tbl, colWidths=[2.5*cm,2*cm,2.6*cm,2.6*cm,2.6*cm,2.7*cm])
t2.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),colors.white),
    ("FONTNAME",(0,0),(-1,0),"Nunito-Bold"),("FONTNAME",(0,1),(-1,-1),"Nunito"),
    ("TEXTCOLOR",(0,1),(-1,-1),NAVY),("FONTSIZE",(0,0),(-1,-1),9.5),("ALIGN",(0,0),(-1,-1),"CENTER"),
    ("GRID",(0,0),(-1,-1),0.4,CINZA),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,OFFWHITE])]))
story.append(t2); SP(6)
P("Tabela 2 — Métricas, épocas e tempo de processamento por padrão numérico. "
  "Métricas calculadas sobre o alvo normalizado.", "Cap")
story.append(Image(os.path.join(FIGS, "g1_curva_treino.png"), width=13*cm, height=8.1*cm))
P("Figura 2 — Curva de treinamento (MSE × épocas). A curva do int8 apresenta "
  "oscilações (ruído de quantização) ausentes no float64 e atinge a parada "
  "antecipada mais cedo.", "Cap")
story.append(Image(os.path.join(FIGS, "g2_metricas.png"), width=16*cm, height=5.3*cm))
P("Figura 3 — Métricas finais. O float64 alcança menor erro (MSE/MAE) e R² "
  "ligeiramente superior ao int8.", "Cap")
story.append(Image(os.path.join(FIGS, "g3_tempo.png"), width=9*cm, height=6.7*cm))
P("Figura 4 — Tempo total de processamento. O int8, neste experimento de "
  "software, foi mais lento por exigir as operações extra de quantização.", "Cap")

# ---- 5 ----
story.append(PageBreak())
P("05 — PRÉ-EMPÇÃO DO SISTEMA OPERACIONAL", "Kicker")
P("Influência da pré-empção do sistema operacional", "H1c")
P("Um sistema operacional <b>pré-emptivo</b> pode interromper (preemptar) uma "
  "tarefa em execução para ceder a CPU a outra de maior prioridade, segundo o "
  "escalonador. Em um instrumento embarcado de aeronave — ambiente típico de tempo "
  "real — essa característica tem dois efeitos sobre o treinamento e a inferência "
  "da rede neural deste estudo.")
P("<b>Possível interferência.</b> Como a pré-empção intercala a execução de "
  "múltiplas tarefas, o tempo total de processamento medido (Figura 4) passa a "
  "depender não só do custo aritmético do padrão numérico, mas também das trocas "
  "de contexto e da espera por CPU. Operações em int8, embora individualmente mais "
  "baratas em hardware, envolvem aqui passos extras de quantização; sob pré-empção, "
  "esses passos podem ser fatiados em mais janelas de execução, ampliando a "
  "variabilidade e, eventualmente, o tempo total — coerente com o observado, em "
  "que o int8 não foi mais rápido.")
P("<b>Possível colaboração.</b> Por outro lado, a pré-empção é justamente o que "
  "garante que a inferência da distância de pista — tarefa crítica — receba a CPU "
  "no instante necessário, preemptando rotinas secundárias. Em representação int8, "
  "de menor footprint de memória e menor custo por operação, a tarefa de inferência "
  "tende a caber dentro de uma única fatia de tempo (quantum) do escalonador, "
  "reduzindo o risco de perder um deadline em tempo real. Assim, a pré-empção "
  "colabora para a previsibilidade temporal, ainda que o padrão int8 sacrifique "
  "parte da precisão numérica (maior MSE/MAE, menor R²).")
P("<b>Síntese.</b> Os resultados sugerem um compromisso (trade-off): o float64 "
  "oferece maior qualidade de inferência, enquanto o int8 favorece economia de "
  "memória e granularidade de execução adequada a um escalonador pré-emptivo, ao "
  "custo de degradação controlada da precisão. A escolha do padrão numérico em um "
  "sistema embarcado pré-emptivo deve, portanto, equilibrar exigências de "
  "exatidão e de garantia de tempo real.")
SP(16)
P("Missão cumprida — tá sob controle.", "Quote")

doc = SimpleDocTemplate(os.path.join(OUT, "Relatorio_SO_pouso.pdf"),
                        pagesize=A4, topMargin=2*cm, bottomMargin=2*cm,
                        leftMargin=2.2*cm, rightMargin=2.2*cm,
                        title="Relatorio SO - Sob Solutions", author="Sob Solutions")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="n")
doc.addPageTemplates([
    PageTemplate(id="capa", frames=[frame], onPage=desenhar_capa),
    PageTemplate(id="corpo", frames=[frame], onPage=rodape),
])
doc.build(story)
print("PDF gerado:", os.path.join(OUT, "Relatorio_SO_pouso.pdf"))
