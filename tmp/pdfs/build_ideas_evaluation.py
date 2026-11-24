from __future__ import annotations

from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path("/Users/asal/Documents/roblox dev")
OUT = ROOT / "output/pdf/Roblox_10_Game_Ideas_Evaluation_RU.pdf"

FONT_DIR = Path("/System/Library/Fonts/Supplemental")
pdfmetrics.registerFont(TTFont("Arial", str(FONT_DIR / "Arial.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Bold", str(FONT_DIR / "Arial Bold.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Italic", str(FONT_DIR / "Arial Italic.ttf")))
pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold", italic="Arial-Italic")

INK = HexColor("#111827")
MUTED = HexColor("#64748B")
GREEN = HexColor("#1F7A5A")
GREEN_BG = HexColor("#ECFDF5")
AMBER = HexColor("#D97706")
AMBER_BG = HexColor("#FFFBEB")
RED = HexColor("#DC2626")
RED_BG = HexColor("#FEF2F2")
PURPLE = HexColor("#6D4AFF")
PURPLE_BG = HexColor("#F5F3FF")
PINK = HexColor("#D9467A")
BLUE = HexColor("#2563EB")
GRID = HexColor("#D9E0E7")
LIGHT = HexColor("#F3F6F9")

PAGE_W, PAGE_H = A4
MARGIN_X = 15 * mm
MARGIN_TOP = 16 * mm
MARGIN_BOTTOM = 15 * mm

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleRU", fontName="Arial-Bold", fontSize=25, leading=29, textColor=INK, spaceAfter=6))
styles.add(ParagraphStyle(name="H1RU", fontName="Arial-Bold", fontSize=17.5, leading=21, textColor=INK, spaceAfter=6))
styles.add(ParagraphStyle(name="H2RU", fontName="Arial-Bold", fontSize=11.5, leading=14.5, textColor=GREEN, spaceAfter=4, spaceBefore=6))
styles.add(ParagraphStyle(name="BodyRU", fontName="Arial", fontSize=8.8, leading=12.0, textColor=INK, spaceAfter=4))
styles.add(ParagraphStyle(name="SmallRU", fontName="Arial", fontSize=7.4, leading=9.8, textColor=MUTED, spaceAfter=3))
styles.add(ParagraphStyle(name="CalloutRU", fontName="Arial-Bold", fontSize=10.5, leading=14, textColor=INK, spaceAfter=4))
styles.add(ParagraphStyle(name="TableRU", fontName="Arial", fontSize=7.0, leading=8.8, textColor=INK))
styles.add(ParagraphStyle(name="TableBoldRU", fontName="Arial-Bold", fontSize=7.0, leading=8.8, textColor=INK))
styles.add(ParagraphStyle(name="TableHeadRU", fontName="Arial-Bold", fontSize=7.0, leading=8.6, textColor=colors.white))
styles.add(ParagraphStyle(name="SourceRU", fontName="Arial", fontSize=6.8, leading=8.8, textColor=INK, spaceAfter=3.5))


def P(text: str, style="BodyRU") -> Paragraph:
    return Paragraph(text, styles[style])


def bullet(text: str) -> Paragraph:
    return Paragraph(f"• {text}", styles["BodyRU"])


def tag(text: str, color=GREEN) -> Table:
    t = Table([[P(f'<font color="white"><b>{text}</b></font>', "SmallRU")]], colWidths=[None])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ]))
    return t


class Rule(Flowable):
    def __init__(self, color=GREEN, width=1.2, gap=4):
        super().__init__()
        self.color, self.line_width, self.gap = color, width, gap
        self.height = gap * 2

    def wrap(self, availWidth, availHeight):
        self._availWidth = availWidth
        return availWidth, self.height

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.line_width)
        self.canv.line(0, self.gap, self._availWidth, self.gap)


class HorizontalScoreChart(Flowable):
    def __init__(self, items, title, height=112 * mm):
        super().__init__()
        self.items = items  # list of (label, score, color, verdict_tag)
        self.title = title
        self.height = height

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        return availWidth, self.height

    def draw(self):
        c = self.canv
        c.setFont("Arial-Bold", 10)
        c.setFillColor(INK)
        c.drawString(0, self.height - 11, self.title)

        top = self.height - 22
        bottom = 12
        left = 54 * mm
        right = self.width - 26 * mm
        n = len(self.items)
        row_h = (top - bottom) / n

        # Vertical grid lines at 25, 55, 75, 100
        for val, label in [(0, "0"), (55, "55 (Pivot)"), (75, "75 (Build)"), (100, "100")]:
            x = left + (right - left) * (val / 100.0)
            c.setStrokeColor(GRID if val in (0, 100) else AMBER if val == 55 else GREEN)
            c.setLineWidth(0.5 if val in (0, 100) else 0.9)
            c.line(x, bottom, x, top + 2)
            c.setFont("Arial", 6.2)
            c.setFillColor(MUTED)
            c.drawCentredString(x, bottom - 9, label)

        for i, (name, score, col, vtag) in enumerate(self.items):
            y_center = top - (i + 0.5) * row_h
            bh = min(row_h * 0.62, 7.2 * mm)
            y0 = y_center - bh / 2

            c.setFont("Arial-Bold" if "Dark Fantasy" in name else "Arial", 7.3)
            c.setFillColor(INK)
            c.drawRightString(left - 4, y_center - 2.3, name)

            bw = (right - left) * (score / 100.0)
            c.setFillColor(col)
            c.rect(left, y0, bw, bh, stroke=0, fill=1)

            c.setFont("Arial-Bold", 7.1)
            c.setFillColor(INK)
            c.drawString(left + bw + 4, y_center - 2.3, f"{score}/100  {vtag}")


def make_table(rows, col_widths, highlight_col=None):
    formatted = []
    for r_idx, row in enumerate(rows):
        style = "TableHeadRU" if r_idx == 0 else "TableRU"
        formatted.append([P(str(cell), style) for cell in row])
    t = Table(formatted, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), INK),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.35, GRID),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4.5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4.5),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
    ]
    t.setStyle(TableStyle(style_cmds))
    return t


def callout(title: str, body: str, border=PURPLE, bg=PURPLE_BG):
    t = Table([[P(f"<b>{title}</b><br/>{body}", "BodyRU")]], colWidths=[PAGE_W - 2 * MARGIN_X])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 3.2, border),
        ("BOX", (0, 0), (-1, -1), 0.4, GRID),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def section(title: str, eyebrow: str, color=GREEN):
    return [tag(eyebrow, color), Spacer(1, 3), P(title, "H1RU"), Rule(color, 1.0, 3)]


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Arial", 7.0)
    canvas.setFillColor(MUTED)
    canvas.drawString(MARGIN_X, 9 * mm, "Roblox 10 Game Ideas Evaluation & Top-Potential Audit (2026–2027)")
    canvas.drawRightString(PAGE_W - MARGIN_X, 9 * mm, f"Стр. {doc.page}")
    canvas.restoreState()


IDEAS = [
    {
        "num": "00",
        "deck": "DECK 1 — ОБЁРТКА",
        "name": "Mini-Game Hub (общий формат 5-в-1)",
        "score": 38,
        "verdict": "KILL (НЕ ДЕЛАТЬ ХАБ)",
        "vcolor": RED,
        "vbg": RED_BG,
        "scores": [6, 4, 6, 9, 6, 7],
        "competitors": "Epic Minigames (1.5k–4.5k CCU, миллиарды визитов, 10+ лет контента), Party-хабы.",
        "saturation": "Высокая (зрелый legacy-формат с падающей долей в RFY 2025–2026).",
        "psych": "Кратковременное разнообразие, но нет владения (ownership), нет истории прогресса, слабый D7/D28.",
        "flaws": [
            "Алгоритм RFY после 2025 жёстко наказывает размытое обещание на обложке («5 игр сразу») высоким first-play bounce.",
            "Разработка 5 разных механик в одном проекте в 5 раз дороже и в 5 раз хуже по качеству, чем 1 отполированная игра.",
            "Только Coin + XP + cosmetics не дают причины вернуться через неделю (нет compounding ownership)."
        ],
        "upgrade": "Не запускать хаб. Выбрать 1 сильнейшую механику (например, переименованный Classroom Prank Chaos или standalone horror) и выпустить её отдельной игрой."
    },
    {
        "num": "01",
        "deck": "DECK 1 — MINI-GAME #1",
        "name": "Ice Arena (5 зимних 1-мин челленджей)",
        "score": 34,
        "verdict": "KILL",
        "vcolor": RED,
        "vbg": RED_BG,
        "scores": [7, 4, 4, 7, 5, 7],
        "competitors": "Зимние раунды в Epic Minigames, Snowball Fight клоны, Ski/Ice Obby.",
        "saturation": "Высокая; к тому же жёстко привязано к зимнему сезону.",
        "psych": "Короткий skill/arcade азарт на 5–10 минут, затем быстрое насыщение.",
        "flaws": [
            "Сезонная ловушка: зимняя тематика резко проседает по CTR с марта по октябрь (7–8 месяцев в году).",
            "Внутри одной мини-игры спрятаны ещё 5 разных режимов (Snowball, Ski, Obby, Snowboard, Penguin) — огромный объём физики ради 60-секундных раундов.",
            "Нет долгосрочного якоря удержания (D7/D28) и слабая социальная генеративность."
        ],
        "upgrade": "Не делать отдельной игрой. Использовать только как временный зимний live-event внутри успешной основной игры в декабре."
    },
    {
        "num": "02",
        "deck": "DECK 1 — MINI-GAME #2",
        "name": "Teacher Abuse → Class Prank Chaos",
        "score": 64,
        "pivot_score": 74,
        "verdict": "PIVOT (ЛУЧШАЯ ИЗ DECK 1)",
        "vcolor": AMBER,
        "vbg": AMBER_BG,
        "scores": [13, 12, 10, 15, 10, 4],
        "competitors": "Scary Teacher 3D клоны на Roblox (в основном слабые соло-обби и ролплей; доминирующего полированного мультиплеерного хита НЕТ).",
        "saturation": "Низкая–средняя в качественном мультиплеере (открытое окно!).",
        "psych": "Сильная социальная комедия, совместный хаос (Silent Signal), риск быть пойманным, мгновенные 10-сек клипы для TikTok/Shorts.",
        "flaws": [
            "КРИТИЧЕСКИЙ РИСК МОДЕРАЦИИ: название «Teacher Abuse» гарантированно вызовет санкции/понижение в выдаче Roblox Safety (ассоциация с насилием/травлей в школе).",
            "В текущем виде (1–3 мин без мета-прогрессии) быстро надоест после 3–5 раундов.",
            "Баланс роли Учителя vs Учеников сложен: если учителем играть скучно, игроки будут выходить из раунда."
        ],
        "upgrade": "1) Срочно переименовать в безобидный мультяшный бренд (Class Prank Chaos / Detention Chaos). 2) Сделать standalone-игрой: дерево гаджетов-пранков, комбо-ловушки на 2–3 друзей, субботние ивенты «Приход директора / Строгая замена» и прокачка школьного статуса."
    },
    {
        "num": "03",
        "deck": "DECK 1 — MINI-GAME #3",
        "name": "Build & Break — Tower Rush",
        "score": 52,
        "verdict": "KILL / СЛАБЫЙ",
        "vcolor": RED,
        "vbg": RED_BG,
        "scores": [10, 5, 8, 12, 8, 9],
        "competitors": "Build A Boat For Treasure (7.5k–16k CCU), Doomspire Brickbattle, BedWars, Tower Defense Simulator (9k–17k CCU).",
        "saturation": "Очень высокая в классическом строительстве и разрушении.",
        "psych": "Командная компетентность и физическое разрушение — приятно на 10–15 мин.",
        "flaws": [
            "Конкуренция напрямую с гигантами (Build A Boat и BedWars) без уникального системного твиста.",
            "После раунда постройка исчезает — нет persistent ownership (игрок ничего не сохраняет и не развивает между днями).",
            "Строительство под таймер на мобильных телефонах часто вызывает фрустрацию и высокий bounce."
        ],
        "upgrade": "Только если добавить сохраняемые чертежи крепостей + систему редких блоков/ловушек + серверные осады с общим состоянием (shared server state)."
    },
    {
        "num": "04",
        "deck": "DECK 1 — MINI-GAME #4",
        "name": "Color Switch Panic",
        "score": 29,
        "verdict": "KILL (100% КЛОН)",
        "vcolor": RED,
        "vbg": RED_BG,
        "scores": [8, 1, 3, 5, 3, 9],
        "competitors": "Color Block (1k–2k+ CCU, 2.6+ млрд визитов) и сотни идентичных клонов.",
        "saturation": "Предельная (коммодитизированный жанр 2018–2021).",
        "psych": "Чистая реакция на 2 минуты; ноль владения, ноль социальной истории, ноль D7.",
        "flaws": [
            "Полная копия Color Block — нулевое отличие, алгоритм RFY не даст трафик без уникального удержания.",
            "Нулевая монетизационная глубина (только базовые трейлы/эмоции).",
            "Нет повода звать друзей повторно на следующий день."
        ],
        "upgrade": "Не тратить время. Шансов выйти в топ в 2026–2027 практически нет."
    },
    {
        "num": "05",
        "deck": "DECK 1 — MINI-GAME #5",
        "name": "Don't Look Behind (Co-op Horror)",
        "score": 66,
        "pivot_score": 76,
        "verdict": "PIVOT / ВЛИТЬ В PINK HOUSE",
        "vcolor": AMBER,
        "vbg": AMBER_BG,
        "scores": [13, 8, 10, 15, 12, 8],
        "competitors": "DOORS, 99 Nights in the Forest, Evade, Don't Blink / Weeping Angel хорроры.",
        "saturation": "Средне-высокая, но спрос на co-op survival horror в 2026–2027 остаётся высоким (70% уверенность).",
        "psych": "Сильнейший co-op страх + клиповость («не оборачивайся!»), высокая вирусность с друзьями.",
        "flaws": [
            "В формате 1–2 минутной мини-игры в «тёмной школе/лаборатории» выглядит вторично и слишком коротко.",
            "Чистый horror-побег попадает в content treadmill: когда игрок выучил карту, он уходит (слабый D14–D28)."
        ],
        "upgrade": "НЕ делать отдельной мини-игрой в школе. Перенести механику монстра («смотри / не оборачивайся») прямо в бездну нашего Pink House / Dark Fantasy Keeper — где уже есть уникальная визуальная фантазия и persistent sanctuary!"
    },
    {
        "num": "06",
        "deck": "DECK 2 — ИДЕЯ #1",
        "name": "Lost City (Приключение / Загадки)",
        "score": 41,
        "verdict": "KILL",
        "vcolor": RED,
        "vbg": RED_BG,
        "scores": [8, 7, 5, 7, 5, 9],
        "competitors": "Сюжетные adventure/showcase карты, The Mimic, квест-румы Roblox.",
        "saturation": "Средняя, но структурно слабая категория для RFY.",
        "psych": "Любопытство и исследование (работает 1 раз, затем полностью исчерпывается).",
        "flaws": [
            "Классическая ловушка «контентного конвейера» из нашего Deep Research: прошёл 3 загадки → увидел секретную комнату → удалил игру навсегда.",
            "В матрице 2020–2025 одиночные/сюжетные исследования без системного риска и владения дают минимальный D7–D28.",
            "Нет сильной причины для друзей возвращаться в ту же локацию десятки раз."
        ],
        "upgrade": "Если использовать визуал заброшенного города — превратить его в кооперативный extraction/survival с лутом, монстрами и базой (как Dead Rails / 99 Nights), а не в спокойные пазлы."
    },
    {
        "num": "07",
        "deck": "DECK 2 — ИДЕЯ #2",
        "name": "Restaurant Empire (Кооп-симулятор)",
        "score": 58,
        "verdict": "PIVOT (НИШЕВЫЙ)",
        "vcolor": AMBER,
        "vbg": AMBER_BG,
        "scores": [9, 5, 13, 13, 9, 9],
        "competitors": "Restaurant Tycoon 2 (1k–3.5k CCU), Work at a Pizza Place (2k–5k CCU), My Restaurant!.",
        "saturation": "Очень высокая — занято легендарными evergreen-хитами.",
        "psych": "Хороший compounding ownership (ресторан растёт) + кооперативные роли (повар/кассир/официант).",
        "flaws": [
            "В описанном виде это почти точная копия Restaurant Tycoon 2 / Work at a Pizza Place без свежего крючка.",
            "Обычный ресторан не даёт вирусного 10-секундного клипа для прорыва в RFY 2026."
        ],
        "upgrade": "Нужен яркий системный твист 2026: хаотичный кооп в духе Overcooked с катастрофами, «ночные визиты проклятых/странных гостей», битва ресторанов на одном сервере (shared server state + sabotage/reviews)."
    },
    {
        "num": "08",
        "deck": "DECK 2 — ИДЕЯ #3",
        "name": "Deep Ocean (Подводное исследование)",
        "score": 39,
        "pivot_score": 76,
        "verdict": "KILL КАК ЕСТЬ / PIVOT В EXTRACTION",
        "vcolor": AMBER,
        "vbg": AMBER_BG,
        "scores": [9, 6, 5, 5, 7, 7],
        "competitors": "Abyss (главный подводный хит, «подводный Fisch»), Fisch (подводные зоны), Become a Deep Sea Explorer.",
        "saturation": "Быстро растущая и уже занятая сильным хитом Abyss.",
        "psych": "В текущем PDF автор САМ убрал главный двигатель: «не ловить и не покупать существ, только наблюдать».",
        "flaws": [
            "ФАТАЛЬНАЯ ОШИБКА В КОНЦЕПТЕ: отказ от поимки/коллекции/владения и от опасности (безопасные маршруты) убивает D1–D28 и монетизацию.",
            "Рынок уже доказал через Fisch и Abyss: игроки хотят глубину + риск кислорода/хищников + редких мутировавших существ + свой аквариум/статус.",
            "Подводная физика и видимость на слабых телефонах требуют серьёзной оптимизации."
        ],
        "upgrade": "Полностью развернуть правило №5: добавить риск кислорода, редких глубоководных существ/реликвии, личный аквариум-витрину и кооп-погружения. Но придётся напрямую обходить Abyss."
    },
    {
        "num": "09",
        "deck": "DECK 2 — ИДЕЯ #4",
        "name": "Delivery Rush (Доставка на время)",
        "score": 44,
        "verdict": "KILL",
        "vcolor": RED,
        "vbg": RED_BG,
        "scores": [8, 5, 8, 6, 6, 11],
        "competitors": "Taxi Boss (4k–13k CCU), Work at a Pizza Place (2k–5k CCU), Driving Empire, Delivery Simulator.",
        "saturation": "Высокая в нише городских доставок и транспорта.",
        "psych": "Быстрый аркадный цикл (1–3 мин) и апгрейд транспорта, но игроки играют параллельно (соло), а не друг с другом.",
        "flaws": [
            "Слабая социальная генеративность: игроки почти не создают друг другу ситуации и драму.",
            "Taxi Boss уже держит 4k–13k CCU с глубокой экономикой и автопарком — обойти его простым курьером крайне сложно.",
            "Управление транспортом на мобильных экранах — частый источник отвала в первую минуту."
        ],
        "upgrade": "Только если сделать безумную кооп-доставку с физикой разрушений / кражей посылок на одном сервере (как Steal + Crazy Taxi)."
    },
    {
        "num": "10",
        "deck": "DECK 2 — ИДЕЯ #5",
        "name": "Dream Park (Строительство парка)",
        "score": 48,
        "verdict": "KILL (ДОРОГО + ЗАНЯТО)",
        "vcolor": RED,
        "vbg": RED_BG,
        "scores": [9, 4, 12, 9, 8, 6],
        "competitors": "Theme Park Tycoon 2 (2k–3.5k CCU, 10 лет развития, кастомные американские горки).",
        "saturation": "Очень высокая против монополиста ниши Theme Park Tycoon 2.",
        "psych": "Автономия, творчество и показ парка друзьям (сильный ownership, но долгий вход).",
        "flaws": [
            "Огромная сложность разработки: система сетки, коллизий, ИИ посетителей, сохранение больших баз и удобный мобильный UI для строительства.",
            "Прямое столкновение с 10-летним хитом Theme Park Tycoon 2, у которого уже есть лояльная база и тысячи объектов.",
            "Идея тематических раундов (как Dress to Impress для парков) интересна, но слишком тяжела технически для быстрого MVP."
        ],
        "upgrade": "Если очень хочется строительный хит — делать быстрый 5-минутный социальный «Построй по теме → проголосуй» (формат DTI), но без сложной симуляции ИИ посетителей."
    },
]

SOURCES = [
    ("R01", "Локальный Deep Research: Roblox 2020–2025 (28 стр.)", "output/pdf/Roblox_Trends_2020_2025_Deep_Research_RU.pdf"),
    ("R02", "Локальный Deck 1: Roblox Mini-Game Hub Visual Concept", "research/inputs/roblox_mini_game_hub_visual_concept.pdf"),
    ("R03", "Локальный Deck 2: Roblox 5 Yangi O'yin G'oyalari", "research/inputs/Roblox_5_Yangi_Oyin_Goyalari_Rasmlar_Bilan.pdf"),
    ("W01", "Rolimon's & RoMonitor Stats — Epic Minigames, Color Block, TDS, Build A Boat CCU", "https://www.rolimons.com/games"),
    ("W02", "RoMonitor Stats — Restaurant Tycoon 2 & Theme Park Tycoon 2 live baselines", "https://romonitorstats.com/"),
    ("W03", "Rolimon's — Taxi Boss & Work at a Pizza Place concurrent player tracking", "https://www.rolimons.com/games"),
    ("W04", "Roblox Underwater Trend — Abyss & Fisch underwater expansions (2025–2026)", "https://www.roblox.com/discover"),
    ("W05", "Roblox Creator Hub — Discovery, RFY signals, Retention & Safety Policies", "https://create.roblox.com/docs/discovery"),
]


def build_story():
    story = []

    # Page 1: Cover & Executive Verdict
    story += [
        Spacer(1, 10 * mm),
        tag("GAME IDEA AUDIT • 2026–2027 TOP-POTENTIAL CHECK", PURPLE),
        Spacer(1, 6 * mm),
        P("Аудит 10 идей Roblox-игр", "TitleRU"),
        P("Есть ли шанс выйти в Топ? Проверка конкурентов, психологии, алгоритма RFY и сравнение с Pink House", "H1RU"),
        Spacer(1, 3 * mm),
        Rule(PINK, 1.8),
        Spacer(1, 4 * mm),
        callout(
            "Главный честный вердикт (без прикрас)",
            "<b>Ни одна из 10 идей в текущем виде не выйдет в Топ Roblox 2026–2027.</b> "
            "7 из 10 идей (плюс формат Mini-Game Hub) — это либо уже занятые evergreen-ниши "
            "(Color Block, Epic Minigames, Restaurant Tycoon 2, Theme Park Tycoon 2, Taxi Boss), "
            "либо «контентный конвейер» без удержания D7–D28 (Lost City, пассивный Deep Ocean).<br/><br/>"
            "<b>Реальный шанс на прорыв есть только у 2–3 направлений ПОСЛЕ переделки:</b> "
            "(1) <b>Pink House / Dark Fantasy Keeper (82/100)</b> — уже строящийся уникальный хит с лучшим совпадением с прогнозом 2026–2027; "
            "(2) <b>Class Prank Chaos (74/100 после ребрендинга с «Teacher Abuse»)</b> — самый сильный вирусный TikTok-кандидат из обоих PDF; "
            "(3) <b>Don't Look Behind</b> лучше не делать отдельной школьной мини-игрой, а встроить её механику монстра прямо в бездну Pink House.",
            PURPLE, PURPLE_BG
        ),
        Spacer(1, 6 * mm),
    ]

    chart_items = [
        ("Pink House / Dark Fantasy Keeper*", 82, GREEN, "BUILD (ЛИДЕР)"),
        ("05. Don't Look Behind (standalone)", 66, AMBER, "PIVOT -> PINK HOUSE"),
        ("02. Teacher Abuse -> Prank Chaos", 64, AMBER, "PIVOT (74 ПОСЛЕ ФИКСА)"),
        ("07. Restaurant Empire", 58, AMBER, "PIVOT (НИША)"),
        ("03. Build & Break — Tower Rush", 52, RED, "KILL / СЛАБЫЙ"),
        ("10. Dream Park", 48, RED, "KILL (ДОРОГО)"),
        ("09. Delivery Rush", 44, RED, "KILL"),
        ("06. Lost City", 41, RED, "KILL"),
        ("08. Deep Ocean (как написано)", 39, AMBER, "KILL / PIVOT (76)"),
        ("00. Mini-Game Hub (формат 5-в-1)", 38, RED, "KILL"),
        ("01. Ice Arena", 34, RED, "KILL"),
        ("04. Color Switch Panic", 29, RED, "KILL (КЛОН)"),
    ]
    story += [
        HorizontalScoreChart(chart_items, "Сводный рейтинг шансов на Топ Roblox (0–100 баллов)", height=106 * mm),
        Spacer(1, 2 * mm),
        P("*Pink House / Dark Fantasy Keeper добавлен как эталон (benchmark) из нашего Deep Research 2020–2025. Подробная система оценки и роутер для AI-агентов вынесены в research/IDEA_VALIDATOR_ROUTER.md.", "SmallRU"),
        PageBreak(),
    ]

    # Page 2: Methodology & Master Comparison Table
    story += section("Методика оценки и сводная таблица", "КАК ПРОВЕРЯЛИ", BLUE)
    story += [
        P("Каждая игра оценена по <b>6 критериям (максимум 100 баллов)</b> на базе нашего Deep Research 2020–2025, требований алгоритма RFY (bounce, play days, D7/D28, intentional co-play) и проверки живых конкурентов Roblox:", "BodyRU"),
        make_table([
            ["Критерий", "Макс", "Что проверяет"],
            ["1. Хук 10 сек и клиповость", "15", "Понятна ли фантазия с обложки за 10 сек и рождает ли игра короткие клипы TikTok/YouTube?"],
            ["2. Конкуренты и отличие", "15", "Не занята ли ниша 10-летним монополистом? Есть ли системная новизна, а не просто рескин?"],
            ["3. Лестница удержания D1–D28", "20", "Есть ли compounding ownership, мастерство и причина вернуться через неделю без content treadmill?"],
            ["4. Социальная генеративность", "20", "Создают ли игроки драму/истории друг для друга (драйвер RFY intentional co-play)?"],
            ["5. Совпадение с трендами 2026–27", "15", "Попадание в Cozy+Danger (75%), Co-op Survival (70%), Social Ownership (70%), Live Events (65%)."],
            ["6. Реализуемость, Mobile и TOS", "15", "Скорость MVP (2–4 недели), работа на слабых телефонах и отсутствие рисков модерации Roblox."],
        ], [48 * mm, 14 * mm, 118 * mm]),
        Spacer(1, 5 * mm),
        P("Сводная таблица всех 10 идей + Hub", "H2RU"),
    ]

    summary_rows = [["#", "Игра", "Балл", "После пивота", "Главный конкурент (CCU)", "Вердикт"]]
    for item in IDEAS:
        comp_short = item["competitors"].split(";")[0]
        if len(comp_short) > 78:
            comp_short = comp_short[:75].rsplit(" ", 1)[0] + "…"
        summary_rows.append([
            item["num"],
            item["name"],
            f"<b>{item['score']}</b>",
            f"<b>{item['pivot_score']}</b>" if "pivot_score" in item else "—",
            comp_short,
            item["verdict"],
        ])
    story += [
        make_table(summary_rows, [9 * mm, 44 * mm, 14 * mm, 18 * mm, 63 * mm, 32 * mm]),
        Spacer(1, 4 * mm),
        callout(
            "Пороги решения (для всех будущих идей)",
            "<b>75–100 (BUILD):</b> запускаем 1-недельный прототип с телеметрией.  "
            "<b>55–74 (PIVOT):</b> есть сильное зерно, но сначала обязательна переделка слабых мест.  "
            "<b>0–54 (KILL):</b> не тратить время команды; максимум — забрать 1 удачную механику.",
            GREEN, GREEN_BG
        ),
        PageBreak(),
    ]

    # Pages 3-8: Detailed 2-per-page cards for all 11 entries (00 + 10 games)
    for idx, item in enumerate(IDEAS):
        if idx % 2 == 0 and idx > 0:
            story.append(PageBreak())
        sc = item["scores"]
        score_str = f"Хук {sc[0]}/15 • Конк. {sc[1]}/15 • D1–D28 {sc[2]}/20 • Соц. {sc[3]}/20 • Тренд {sc[4]}/15 • MVP/TOS {sc[5]}/15"
        pivot_txt = f" → <b>{item['pivot_score']}/100 после пивота</b>" if "pivot_score" in item else ""

        story += [
            tag(f"{item['deck']}  •  {item['verdict']}", item["vcolor"]),
            Spacer(1, 2),
            P(f"{item['num']}. {item['name']} — {item['score']}/100{pivot_txt}", "H2RU"),
            P(f"<b>Разбивка баллов:</b> {score_str}", "SmallRU"),
            make_table([
                ["Конкуренты на Roblox", item["competitors"]],
                ["Насыщенность / Психология", f"{item['saturation']} | {item['psych']}"],
                ["Главные риски / Почему не взлетит как есть", "<br/>".join(f"• {f}" for f in item["flaws"])],
                ["Что нужно для Топа / Рекомендация", item["upgrade"]],
            ], [42 * mm, 138 * mm]),
            Spacer(1, 5 * mm),
        ]

    story.append(PageBreak())

    # Final Page: Strategic Plan + Agent Router Explanation + Sources
    story += section("Стратегический вывод и система проверки для агентов", "ЧТО ДЕЛАТЬ ДАЛЬШЕ", PURPLE)
    story += [
        callout(
            "Оптимальный портфель на 2026–2027 (не распыляться!)",
            "<b>1. Главная ставка (80% фокуса): Pink House / Dark Fantasy Keeper (82/100).</b> "
            "У вас уже есть узнаваемая карта, 3D-трава и лестница в бездну. Встройте туда механику монстра из <i>Don't Look Behind</i> "
            "(«смотри / не оборачивайся» в расщелине), добавьте 5–8 минутный цикл спуска за реликвиями/существами и развитие дома.<br/>"
            "<b>2. Запасной вирусный спин-офф (если нужен второй быстрый проект): Class Prank Chaos (74/100).</b> "
            "Обязательно переименовать (убрать «Teacher Abuse»!), выпустить отдельной игрой без хаба, сделать ставку на кооп-пранки и TikTok-клипы.<br/>"
            "<b>3. Всё остальное (Ice Arena, Color Switch Panic, Lost City, Delivery Rush, Dream Park, пассивный Deep Ocean, Mini-Game Hub) — закрыть.</b>",
            GREEN, GREEN_BG
        ),
        Spacer(1, 5 * mm),
        P("Как работает новый Markdown-роутер для всех AI-агентов команды", "H2RU"),
        P("Чтобы ни один агент (твой или друзей) больше не переполнял контекст и не оценивал идеи «на глаз», в репозиторий добавлен лёгкий файл-роутер <b>research/IDEA_VALIDATOR_ROUTER.md</b> (привязанный в <b>AGENTS.md</b>):", "BodyRU"),
        bullet("Агент сначала читает короткий <b>IDEA_VALIDATOR_ROUTER.md</b> (~100 строк), а не загружает сразу 40 страниц PDF."),
        bullet("Роутер содержит 5 жёстких стоп-фильтров (модерация/TOS, ловушка хаба, клон evergreen-хита, контентный конвейер, запрет выдумывать закрытые метрики)."),
        bullet("Роутер указывает агенту точные пути и страницы PDF-базы знаний (<b>Roblox_Trends_2020_2025_Deep_Research_RU.pdf</b> и этот отчёт), когда нужны факты, графики или конкуренты."),
        bullet("Любая новая идея обязана пройти 100-балльную матрицу и получить честный вердикт <b>BUILD / PIVOT / KILL</b> + план 1-недельного MVP-теста."),
        Spacer(1, 5 * mm),
        P("Источники и база знаний", "H2RU"),
    ]

    for sid, name, url in SOURCES:
        if url.startswith("http"):
            story.append(P(f'<b>{sid}</b> — {name}<br/><link href="{url}" color="#2563EB">{url}</link>', "SourceRU"))
        else:
            story.append(P(f"<b>{sid}</b> — {name} (<code>{url}</code>)", "SourceRU"))

    return story


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=MARGIN_X,
        rightMargin=MARGIN_X,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM,
        title="Аудит 10 идей Roblox-игр (2026–2027)",
        author="Antigravity Research for Dark Fantasy Roblox",
        subject="Competitor, psychology, and RFY evaluation of 10 Roblox game concepts",
    )
    frame = Frame(MARGIN_X, MARGIN_BOTTOM, PAGE_W - 2 * MARGIN_X, PAGE_H - MARGIN_TOP - MARGIN_BOTTOM, id="main")
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=on_page)])
    doc.build(build_story())
    print("Built:", OUT)


if __name__ == "__main__":
    main()
