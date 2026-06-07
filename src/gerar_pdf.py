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
P("<b>Questão de pesquisa.</b> Trocar float64 por int8 num sistema embarcado de "
  "pouso faz a rede neural errar mais? E quanto isso custa em tempo de "
  "processamento? Essa é a pergunta que queremos responder. O cenário é um "
  "instrumento de bordo que precisa estimar, durante o pouso, quanto de pista "
  "ainda resta até a aeronave parar.")
P("<b>Objetivo geral.</b> Medir o quanto o padrão numérico usado nos cálculos da "
  "rede muda a qualidade da previsão e o tempo de treinamento. Para isso treinamos "
  "a mesma MLP duas vezes, uma em float64 e outra em int8, e comparamos.")
P("Como chegamos lá", "H2c")
P("Primeiro modelamos a física do pouso e usamos essas equações para gerar o "
  "dataset, já que aceleração de pouso não é constante e isso importa para a "
  "qualidade dos dados. Em seguida exploramos e preparamos esses dados, "
  "implementamos a MLP do zero para ter controle total sobre a precisão numérica, "
  "treinamos nos dois padrões medindo épocas, erro e tempo, e por fim discutimos "
  "o papel da pré-empção do sistema operacional sobre o que observamos.")

# ---- 2 ----
P("02 — CINEMÁTICA DO POUSO", "Kicker")
P("Equações cinemáticas do processo de pouso", "H1c")
P("Quando a aeronave toca a pista, três forças atuam contra o movimento: o "
  "arrasto do ar, o empuxo reverso das turbinas e a frenagem das rodas. O detalhe "
  "importante é que o arrasto cresce com o quadrado da velocidade e o reverso "
  "cresce com a velocidade, então a desaceleração muda o tempo todo durante o "
  "pouso. Ou seja, não é aceleração constante e as fórmulas de M.U.V. não servem "
  "aqui. Pela segunda lei de Newton:")
P("m · (dv/dt) = − F<sub>frenagem</sub> − F<sub>arrasto</sub>(v) − F<sub>reverso</sub>(v)", "Eq")
P("Cada força é:")
P("F<sub>arrasto</sub>(v) = ½ · ρ · C<sub>d</sub> · A · v<super>2</super>", "Eq")
P("F<sub>reverso</sub>(v) = k<sub>rev</sub> · v", "Eq")
P("F<sub>frenagem</sub> = μ · m · g", "Eq")
P("Juntando tudo, a velocidade obedece a uma equação diferencial não linear:")
P("dv/dt = − [ ½ρC<sub>d</sub>A·v<super>2</super> + k<sub>rev</sub>·v + μmg ] / m", "Eq")
P("A posição é a integral da velocidade. Como a aceleração depende da própria "
  "velocidade, não dá pra resolver com uma conta direta, então integramos numérica"
  "mente por Runge-Kutta de 4ª ordem com passo de 0,05 s. O gráfico abaixo mostra "
  "a aceleração variando ao longo do pouso, confirmando que o movimento é mesmo "
  "variado de forma não uniforme.")
story.append(Image(os.path.join(FIGS, "g4_fisica.png"), width=16*cm, height=5.8*cm))
P("Figura 1 — Velocidade e aceleração de um pouso simulado. "
  "A aceleração vai de cerca de −4,9 a −3,1 m/s².", "Cap")

# ---- 3 ----
story.append(PageBreak())
P("03 — DADOS", "Kicker")
P("Critérios de arrumação dos dados de pouso", "H1c")
P("Os dados são sintéticos, gerados a partir do modelo físico da seção anterior. "
  "Simulamos milhares de pousos variando massa da aeronave, coeficiente de "
  "arrasto, área de referência, atrito da pista e força do reverso, o que dá "
  "6 milhões de linhas com 5 atributos cada.")
tbl_attr = [["Atributo", "Descrição", "Unidade"],
            ["t", "tempo desde o toque", "s"],
            ["v", "velocidade instantânea", "m/s"],
            ["x", "distância percorrida na pista", "m"],
            ["a", "aceleração instantânea", "m/s²"],
            ["massa", "massa da aeronave no pouso", "kg"],
            ["dist_restante (alvo)", "distância de pista até parar", "m"]]
t = Table(tbl_attr, colWidths=[4.4*cm, 8*cm, 2.2*cm])
t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),colors.white),
    ("FONTNAME",(0,0),(-1,0),"Nunito-Bold"),("FONTNAME",(0,1),(-1,-1),"Nunito"),
    ("FONTSIZE",(0,0),(-1,-1),9),("GRID",(0,0),(-1,-1),0.4,CINZA),
    ("TEXTCOLOR",(0,1),(-1,-1),NAVY),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,OFFWHITE])]))
story.append(t); SP(10)
P("Na exploração olhamos média, desvio e extremos de cada coluna para conferir se "
  "fazia sentido fisicamente: velocidade caindo de uns 75 m/s até parar, distância "
  "restante diminuindo até zero e aceleração sempre negativa. No tratamento "
  "tiramos valores infinitos ou ausentes e descartamos simulações curtas demais "
  "para serem úteis.")
P("Uma decisão importante na preparação: treinamos a rede numa amostra aleatória "
  "de 40 mil linhas, e não nas 6 milhões. Rodar a MLP que escrevemos em NumPy "
  "sobre o dataset inteiro a cada época seria pesado demais para o tempo que "
  "tínhamos, e 40 mil linhas já cobrem bem a variedade de pousos. Por fim "
  "normalizamos as features para o intervalo de 0 a 1, o que a sigmoide pede e "
  "ainda deixa a faixa controlada para a quantização int8 funcionar. Separamos "
  "80% para treino e 20% para teste.")

# ---- 4 ----
P("04 — RESULTADOS", "Kicker")
P("Resultados do treinamento: int8 vs float64", "H1c")
P("A rede tem uma camada oculta de 16 neurônios e sigmoide nas duas camadas. "
  "Treinamos com gradiente descendente e parada antecipada, que interrompe o "
  "treino quando o erro para de melhorar. A tabela traz os números dos dois "
  "padrões.")
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
P("Tabela 2 — Épocas, erro e tempo de processamento de cada padrão. Métricas "
  "sobre o alvo normalizado.", "Cap")
P("Vale ser honesto sobre o tamanho da diferença: o float64 ficou melhor, mas "
  "por pouco, com R² de 0,94 contra 0,93 do int8. A relação entre os dados e a "
  "resposta é simples o bastante para que a perda de precisão do int8 não derrube "
  "muito o resultado. O efeito aparece mais na forma da curva de treino do que no "
  "número final.")
story.append(Image(os.path.join(FIGS, "g1_curva_treino.png"), width=13*cm, height=8.1*cm))
P("Figura 2 — Erro ao longo das épocas. A curva do int8 treme mais, por causa do "
  "ruído de quantização, e para antes pela parada antecipada.", "Cap")
story.append(Image(os.path.join(FIGS, "g2_metricas.png"), width=16*cm, height=5.3*cm))
P("Figura 3 — Erro e R² finais. O float64 leva uma pequena vantagem nas três "
  "métricas.", "Cap")
story.append(Image(os.path.join(FIGS, "g3_tempo.png"), width=9*cm, height=6.7*cm))
P("Figura 4 — Tempo total. Em software o int8 saiu mais lento, porque cada passo "
  "ainda paga as contas de quantização.", "Cap")

# ---- 5 ----
story.append(PageBreak())
P("05 — PRÉ-EMPÇÃO DO SISTEMA OPERACIONAL", "Kicker")
P("Influência da pré-empção do sistema operacional", "H1c")
P("Um sistema operacional pré-emptivo pode parar uma tarefa no meio para dar a CPU "
  "a outra mais urgente. Num instrumento de avião, que é um ambiente de tempo real, "
  "isso pesa de dois jeitos sobre o que medimos aqui.")
P("Pelo lado que atrapalha: como o sistema fica intercalando tarefas, o tempo que "
  "medimos não depende só da conta que a rede faz, mas também das trocas de "
  "contexto e da espera pela CPU. As contas em int8 deveriam ser mais leves no "
  "hardware, mas na nossa implementação elas ainda carregam os passos de "
  "quantização, e sob pré-empção esses passos podem ser picados em mais pedaços. "
  "Isso ajuda a explicar por que o int8 não saiu mais rápido como se esperaria.")
P("Pelo lado que ajuda: é justamente a pré-empção que garante que a estimativa de "
  "pista, que é a tarefa crítica, receba a CPU na hora certa, passando na frente "
  "de rotinas menos importantes. Como o int8 ocupa menos memória e cada operação "
  "é mais barata, essa tarefa tem mais chance de caber numa única fatia de tempo "
  "do escalonador, o que reduz o risco de estourar um prazo. O preço disso é a "
  "precisão um pouco menor que vimos nos resultados.")
P("No fim, é uma escolha entre duas coisas: o float64 prevê melhor, o int8 é mais "
  "enxuto e se encaixa melhor num escalonador de tempo real. Num sistema embarcado "
  "de verdade, decidir entre os dois é equilibrar o quanto de exatidão você precisa "
  "contra a garantia de responder dentro do prazo.")
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
