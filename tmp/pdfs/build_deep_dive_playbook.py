from __future__ import annotations

from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
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
OUT = ROOT / "output/pdf/Roblox_10_Ideas_Deep_Dive_Playbook_RU.pdf"

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
BLUE = HexColor("#2563EB")
BLUE_BG = HexColor("#EFF6FF")
PINK = HexColor("#D9467A")
GRID = HexColor("#D9E0E7")
LIGHT = HexColor("#F3F6F9")

PAGE_W, PAGE_H = A4
MARGIN_X = 14 * mm
MARGIN_TOP = 15 * mm
MARGIN_BOTTOM = 14 * mm

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleRU", fontName="Arial-Bold", fontSize=24, leading=28, textColor=INK, spaceAfter=5))
styles.add(ParagraphStyle(name="H1RU", fontName="Arial-Bold", fontSize=16.5, leading=20, textColor=INK, spaceAfter=5))
styles.add(ParagraphStyle(name="H2RU", fontName="Arial-Bold", fontSize=11.0, leading=14, textColor=GREEN, spaceAfter=3, spaceBefore=5))
styles.add(ParagraphStyle(name="BodyRU", fontName="Arial", fontSize=8.5, leading=11.6, textColor=INK, spaceAfter=3.5))
styles.add(ParagraphStyle(name="SmallRU", fontName="Arial", fontSize=7.2, leading=9.5, textColor=MUTED, spaceAfter=2.5))
styles.add(ParagraphStyle(name="TableRU", fontName="Arial", fontSize=7.1, leading=9.1, textColor=INK))
styles.add(ParagraphStyle(name="TableHeadRU", fontName="Arial-Bold", fontSize=7.1, leading=9.0, textColor=colors.white))
styles.add(ParagraphStyle(name="SourceRU", fontName="Arial", fontSize=6.8, leading=8.8, textColor=INK, spaceAfter=3))


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
    def __init__(self, color=GREEN, width=1.1, gap=3.5):
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


def make_table(rows, col_widths, head_bg=INK):
    formatted = []
    for r_idx, row in enumerate(rows):
        st = "TableHeadRU" if r_idx == 0 else "TableRU"
        formatted.append([P(str(cell), st) for cell in row])
    t = Table(formatted, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), head_bg),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.35, GRID),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4.5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4.5),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
    ]))
    return t


def callout(title: str, body: str, border=PURPLE, bg=PURPLE_BG):
    t = Table([[P(f"<b>{title}</b><br/>{body}", "BodyRU")]], colWidths=[PAGE_W - 2 * MARGIN_X])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 3.2, border),
        ("BOX", (0, 0), (-1, -1), 0.4, GRID),
        ("LEFTPADDING", (0, 0), (-1, -1), 7.5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7.5),
        ("TOPPADDING", (0, 0), (-1, -1), 5.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5.5),
    ]))
    return t


def two_col_boxes(left_title, left_body, right_title, right_body, l_col=GREEN, l_bg=GREEN_BG, r_col=RED, r_bg=RED_BG):
    w = (PAGE_W - 2 * MARGIN_X - 4 * mm) / 2
    t = Table(
        [[P(f"<b>{left_title}</b><br/>{left_body}", "TableRU"), "", P(f"<b>{right_title}</b><br/>{right_body}", "TableRU")]],
        colWidths=[w, 4 * mm, w],
    )
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), l_bg),
        ("LINEBEFORE", (0, 0), (0, 0), 2.8, l_col),
        ("BOX", (0, 0), (0, 0), 0.35, GRID),
        ("BACKGROUND", (2, 0), (2, 0), r_bg),
        ("LINEBEFORE", (2, 0), (2, 0), 2.8, r_col),
        ("BOX", (2, 0), (2, 0), 0.35, GRID),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (0, 0), 6),
        ("RIGHTPADDING", (0, 0), (0, 0), 6),
        ("LEFTPADDING", (2, 0), (2, 0), 6),
        ("RIGHTPADDING", (2, 0), (2, 0), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Arial", 6.8)
    canvas.setFillColor(MUTED)
    canvas.drawString(MARGIN_X, 8.5 * mm, "Roblox 10 Game Ideas — Deep-Dive Playbook (Bull/Bear, Redesign, Monetization & MVP)")
    canvas.drawRightString(PAGE_W - MARGIN_X, 8.5 * mm, f"Стр. {doc.page}")
    canvas.restoreState()


GAMES = [
    {
        "num": "01",
        "name": "Ice Arena (Зимние 60-сек челленджи)",
        "raw_score": 34,
        "upgraded_score": 56,
        "tier": "Tier C → Tier B (сезонный ивент, 300–1k CCU зимой)",
        "tier_col": RED,
        "dev_time": "4–6 недель (5 режимов)",
        "bull": "• Яркая, понятная с первого кадра зимняя эстетика — отлично работает в ноябре–январе.<br/>"
                "• Быстрые 60-сек раунды легко заходят детям на мобильных.<br/>"
                "• Механика Snowball Knockback (вытолкни соперника со льда) сама по себе даёт весёлый хаос с друзьями.",
        "bear": "• Сезонный обвал: с марта по октябрь зимние обложки проигрывают по CTR (аудитория уходит в летние/универсальные темы).<br/>"
                "• 5 разных физик (лыжи, сноуборд, пингвины, снежки, обби) в 5 раз растягивают разработку и баги.<br/>"
                "• Нет мета-прогрессии и владения (D7/D28 падает почти до нуля).",
        "loops": [
            ["0–10 сек", "Одна понятная арена: «Столкни всех с тающего айсберга снежками!» (убрать 4 лишних режима)."],
            ["1–3 мин", "Раунд на тающем/ломающемся льду с супер-снежками и отбрасыванием (как Slap Battles на льду)."],
            ["D1 → D7", "Разблокировка перчаток/пушек-снежкомётов с уникальными эффектами (ледяная стена, лавина, пингвин-торпеда)."],
            ["D28 / Live", "Не делать круглогодичной игрой — запускать сезонные кубки или переименовать в «Elemental Arena» (лёд/лава/песок)."],
        ],
        "monetization": "Скины снежкомётов и эффекты удара (99–249 R$), VIP-эмоции победы, Private Server (50–100 R$) для турниров друзей, 2x Snow Coins (199 R$).",
        "mvp": "Не делать 5 режимов! Сделать 1 арену «Ice Knockback» (тающий лёд + 4 вида снежков) за 10 дней. Если D1 > 12% — расширять биомы (лава, джунгли)."
    },
    {
        "num": "02",
        "name": "Teacher Abuse → Class Prank Chaos",
        "raw_score": 64,
        "upgraded_score": 78,
        "tier": "Tier A (Вирусный прорыв: 2k–15k+ CCU)",
        "tier_col": GREEN,
        "dev_time": "2–3 недели (MVP)",
        "bull": "• ОГРОМНОЕ свободное окно: на Roblox есть слабые клоны Scary Teacher 3D, но НЕТ отполированного мультиплеерного хита про школьные пранки с друзьями.<br/>"
                "• Идеальный TikTok/Shorts-формат: учитель оборачивается, ученики замирают с невинными лицами, срабатывает ловушка — готовый вирусный клип за 10 секунд.<br/>"
                "• Сильнейший RFY-сигнал intentional co-play: пранки в паре (один отвлекает, второй ставит ловушку).",
        "bear": "• КРИТИЧЕСКИЙ СТОП-ФАКТОР: название «Teacher Abuse» нарушает чувствительность Roblox Safety (травля/насилие в школе) — проект может получить теневой бан в поиске.<br/>"
                "• Если роль Учителя скучная (или бот тупой), раунды быстро ломаются.<br/>"
                "• Без мета-прогрессии надоест за 15 минут.",
        "loops": [
            ["0–10 сек", "Переименовать в <b>Class Prank Chaos</b> / <b>Detention Chaos</b>. Сразу в классе: таймер урока, злой смешной учитель у доски."],
            ["1–3 мин", "Шкала хаоса vs шкала подозрений. Комбо-пранки на 2–3 игроков дают x3 очков. Пойманный летит в «угол позора» (друзья могут спасти!)."],
            ["D1 → D7", "Коллекция 30+ мультяшных пранк-гаджетов (бумажный дрон, резиновая мышь, подушка-пердушка, клей), прокачка «Репутации хулигана»."],
            ["D28 / Live", "Субботние ивенты: «Приход Директора-Босса», «Урок химии со взрывами», «Замена учителя-робота»."],
        ],
        "monetization": "Наборы смешных гаджетов (косметика/эффекты, не P2W), кастомные классы/скины парт, звук/анимация пранков, роль «Секретный Учитель» / Private Server для стримеров (100 R$).",
        "mvp": "1 класс + 1 смешной AI/игрок-Учитель + 5 пранк-предметов + механика «замри, когда смотрит» + спасение друга из detention. Тест с друзьями на 5–8 человек."
    },
    {
        "num": "03",
        "name": "Build & Break — Tower Rush",
        "raw_score": 52,
        "upgraded_score": 71,
        "tier": "Tier A–B (1.5k–8k CCU при ставке на физику)",
        "tier_col": AMBER,
        "dev_time": "3–4 недели (MVP)",
        "bull": "• Наше доп-исследование показало: на Roblox НЕТ одного доминирующего хита в жанре «Быстрый PvP Build & Physics Destroy» (Voxel Destruction Physics — просто песочница, Build A Boat — не быстрый PvP).<br/>"
                "• Физическое обрушение башни блоками (как Teardown/Angry Birds в 3D) невероятно зрелищно и клипово.<br/>"
                "• Чёткая командная динамика: 2v2 / 4v4, легко звать друзей.",
        "bear": "• В базовом PDF постройка пропадает после раунда — нет долгосрочного владения (ownership).<br/>"
                "• Строить блоки на телефоне под таймер неудобно, если нет «быстрых шаблонов» (1-tap prefabs).<br/>"
                "• Лаги физики при разрушении сотен деталей на слабых смартфонах.",
        "loops": [
            ["0–10 сек", "Две башни друг напротив друга через пропасть. 45 сек стройки (1-tap модули: стена, балка, щит, пушка) → 90 сек обстрела!"],
            ["1–3 мин", "Разрушай опоры врага, чтобы вся его башня красиво рухнула в пропасть! Кто сбил «Ядро» врага — победил."],
            ["D1 → D7", "Сохраняемые чертежи крепостей (Blueprints), открытие редких материалов (обсидиан, пружинные блоки, TNT-ловушки) и пушек."],
            ["D28 / Live", "Клановые осады по выходным (8v8 мега-замки), рейтинговые лиги инженеров."],
        ],
        "monetization": "Дополнительные слоты чертежей (149 R$), косметические скины блоков и взрывов (неон, средневековье, лава), Private Server для дуэлей, ускорение открытия сундуков.",
        "mvp": "1 арена 2v2, 6 типов блоков (включая 1-tap готовые стены для мобилок), 2 пушки, честная физика обрушения (ограничение до 120 деталей на башню для 60 FPS)."
    },
    {
        "num": "04",
        "name": "Color Switch Panic",
        "raw_score": 29,
        "upgraded_score": 45,
        "tier": "Tier C (<500 CCU, крайне высокий риск)",
        "tier_col": RED,
        "dev_time": "1–2 недели (MVP)",
        "bull": "• Самый быстрый и дешёвый прототип из всех 10 игр (можно собрать за 3–5 дней как тренировку команды).<br/>"
                "• Нулевой порог входа: правила понятны за 3 секунды даже 6-летнему игроку.<br/>"
                "• Жанр доказал массовость (<b>Color Block</b>: 2.6+ млрд визитов, 1k–2k+ стабильных CCU).",
        "bear": "• Предельная насыщенность: сотни идеальных клонов Color Block уже существуют.<br/>"
                "• Алгоритм RFY не даст органику копии без прорыва по D1/D7 и Playtime.<br/>"
                "• Почти нулевая глубина монетизации (игрокам незачем платить в 1-минутной бегалке).",
        "loops": [
            ["0–10 сек", "Единственный шанс отличиться — добавить <b>социальный саботаж</b>: толкай соперников с нужного цвета, ставь фальшивые плитки!"],
            ["1–3 мин", "Многоэтажная падающая арена + случайные модификаторы (лёд, низкая гравитация, лазеры, фейк-команды)."],
            ["D1 → D7", "Перки/способности (рывок, прыжок-батут, щит на 1 ошибку) + таблица серий побед (Win Streak над головой — статус!)."],
            ["D28 / Live", "Турниры на выбывание (Squid-формат: 30 игроков → 1 победитель с короной)."],
        ],
        "monetization": "Эффекты следа (trails), победные танцы, защита Win Streak (1 раз за сессию, аккуратно без P2W), косметические скины аватара.",
        "mvp": "Стоит делать ТОЛЬКО как учебный спринт на 5 дней, чтобы команда набила руку на Rojo/UI/DataStore, но не ждать от него Топа."
    },
    {
        "num": "05",
        "name": "Don't Look Behind (Co-op Horror)",
        "raw_score": 66,
        "upgraded_score": 80,
        "tier": "Tier S–A (5k–30k+ CCU как standalone или в Pink House)",
        "tier_col": GREEN,
        "dev_time": "3–4 недели (MVP)",
        "bull": "• Попадает прямо в тренд 2026–2027 <b>Co-op Survival Horror (70% уверенность)</b> (DOORS, 99 Nights in the Forest).<br/>"
                "• Механика Weeping Angel / «Не оборачивайся / держи в поле зрения» рождает дикий крик, смех и миллионные клипы с друзьями.<br/>"
                "• Высокая ценность голосового чата (Proximity Voice Chat) и командной зависимости («я смотрю на него — ты открывай замок!»).",
        "bear": "• Сеттинг «тёмная школа/лаборатория на 1–2 мин» слишком банален и короток.<br/>"
                "• Риск контентного конвейера: если карта статичная, через 3 забега становится не страшно.<br/>"
                "• Нужен отличный саунд-дизайн и освещение — дешёвая графика в хорроре сразу даёт высокий bounce.",
        "loops": [
            ["0–10 сек", "<b>Лучший ход:</b> встроить этого монстра в бездну <b>Pink House</b>! Либо сделать процедурный 8-минутный кооп-побег (как DOORS)."],
            ["3–8 мин", "Кооп-зависимость: один игрок держит взгляд/фонарь на сущности, пока второй взламывает дверь или несёт реликвию."],
            ["D1 → D7", "Прокачка снаряжения (фонари, зеркала заднего вида, датчики движения), коллекция пережитых сущностей и лор-журнал."],
            ["D28 / Live", "Режимы сложности, новые сущности-мутаторы по субботам (например, «Двойная тьма» или «Слепой охотник»)."],
        ],
        "monetization": "Скины фонариков/экипировки, 1 честное возрождение за забег (35–49 R$, как в DOORS!), частные лобби, эмоции страха, косметика убежища.",
        "mvp": "1 процедурный коридор/расщелина, 1 умный монстр с проверкой поля зрения камеры (dot product + raycast), 1 кооп-замок на 2 игроков. Тест страха на друзьях!"
    },
    {
        "num": "06",
        "name": "Lost City (Тайны заброшенного города)",
        "raw_score": 41,
        "upgraded_score": 68,
        "tier": "Tier C (как пазлы) → Tier A–B (как Co-op Extraction, 1k–5k CCU)",
        "tier_col": AMBER,
        "dev_time": "4–6 недель",
        "bull": "• Очень красивый, притягательный визуал на обложке (заросший заброшенный мегаполис с фонарями — высокий CTR!).<br/>"
                "• Сильная атмосфера тайны и исследования с друзьями.<br/>"
                "• Легко монетизировать атмосферу (скины рюкзаков, фонарей, дронов, питомцев-помощников).",
        "bear": "• В оригинальном PDF — это одноразовый квест («найди 3 загадки и открой комнату»). Прошёл за 20 минут и больше никогда не вернулся.<br/>"
                "• Невозможно каждую неделю руками строить новые кварталы и загадки (content treadmill).<br/>"
                "• Без риска/опасности и экономики игроки быстро скучают.",
        "loops": [
            ["0–10 сек", "Переосмыслить в <b>Co-op Urban Extraction</b>: «Заброшенный город затапливает туман — собери древние артефакты за 6 минут и вернись в лагерь!»"],
            ["4–6 мин", "Риск vs Награда: чем глубже в город, тем дороже реликвии, но выше шанс встретить стражей руин и потерять лут."],
            ["D1 → D7", "Собственный лагерь/база выживших (улучшение верстака, витрина редких находок, крафт крюка-кошки и сканера)."],
            ["D28 / Live", "Динамическая погода и события города (кислотный дождь, ночная охота, временный бункер по выходным)."],
        ],
        "monetization": "Расширение рюкзака (умеренно), скины фонарей/крюков, декор лагеря, Private Server, Season Pass исследователя.",
        "mvp": "1 квартал руин + 1 лагерь + таймер тумана + 10 видов лута разной редкости + 1 патрулирующая угроза. Проверка, хотят ли игроки сделать 2-й и 3-й заход."
    },
    {
        "num": "07",
        "name": "Restaurant Empire (Кооп-ресторан)",
        "raw_score": 58,
        "upgraded_score": 73,
        "tier": "Tier B–A (1k–6k CCU — стабильный прибыльный бизнес)",
        "tier_col": GREEN,
        "dev_time": "4–5 недель",
        "bull": "• Проверенный вечный спрос: <b>Work at a Pizza Place</b> (2k–5k CCU), <b>Restaurant Tycoon 2</b> (1k–3.5k CCU) и новый хит <b>Restaurant Tycoon 3</b> доказывают, что игроки ОБОЖАЮТ готовить с друзьями.<br/>"
                "• Отличная монетизация: игроки охотно покупают VIP-кухни, быструю готовку, декор и редких шефов.<br/>"
                "• Даже 1 000–2 000 CCU в этом жанре приносят $4k–$15k/мес (DevEx).",
        "bear": "• В 2025–2026 вышел <b>Restaurant Tycoon 3</b> (от Ultraw) с огромным бюджетом, оффлайн-доходом и кастомизацией — копировать его в лоб бессмысленно.<br/>"
                "• Обычный спокойный симулятор не даёт вирусных клипов.<br/>"
                "• Много логики синхронизации (очереди, блюда, роли, сохранение расстановки).",
        "loops": [
            ["0–10 сек", "Не клонировать RT3! Сделать <b>Overcooked-хаос + прогрессию</b>: «Удержи безумную кухню с друзьями во время часа пик!»"],
            ["4–6 мин", "Кооп-смены с катастрофами (пожар на плите, нашествие крыс, VIP-критик с таймером, движущиеся столы) — море смеха и клипов."],
            ["D1 → D7", "Между сменами улучшаете свой ресторан, открываете безумные рецепты (магические/монстр-блюда) и нанимаете помощников."],
            ["D28 / Live", "Битвы ресторанов на одном сервере (кто наберёт 5 звёзд быстрее), сезонные фестивали еды по субботам."],
        ],
        "monetization": "Наборы декора и тем ресторана (киберпанк, уютное кафе, замок), VIP-рецепты, 2x Чаевые (249 R$), косметические шапки/фартуки шефа, Private Server.",
        "mvp": "1 компактная кухня на 2–4 друзей, 3 блюда с 3 шагами готовки, 2 случайные катастрофы (пожар + злой критик), 5 апгрейдов кухни. Проверка веселья в коопе!"
    },
    {
        "num": "08",
        "name": "Deep Ocean (Подводный мир)",
        "raw_score": 39,
        "upgraded_score": 76,
        "tier": "Tier A (2k–15k+ CCU ПОСЛЕ добавления ловли и риска)",
        "tier_col": GREEN,
        "dev_time": "3–5 недель",
        "bull": "• Подводный жанр на огромном подъёме в 2025–2026: <b>Abyss</b> («подводный Fisch») и подводные апдейты <b>Fisch</b> доказали гигантский аппетит игроков к дайвингу, глубине и талассофобии.<br/>"
                "• Попадает сразу в два топ-тренда 2026–2027: <b>Cozy + Danger (75%)</b> и <b>Social Ownership (70%)</b>.<br/>"
                "• Потрясающие скриншоты/видео (биолюминесцентные глубины, гигантские существа).",
        "bear": "• В исходном PDF автор сам убил игру пунктом №5: <i>«не ловить и не покупать существ, только безопасно смотреть»</i> — без владения и риска удержание D7 рухнет.<br/>"
                "• Сильный прямой конкурент <b>Abyss</b> (нужно уникальное отличие: например, кооп-подлодка или свой огромный аквариум-музей).<br/>"
                "• Подводное управление на мобильных часто неудобное.",
        "loops": [
            ["0–10 сек", "Ныряй с аквалангом прямо с пирса/лодки! Сразу видно светящуюся рыбу, затонувший сундук и полоску кислорода."],
            ["3–7 мин", "Спуск на глубину → поимка/сканирование редких мутировавших существ или древних реликвий → возврат наверх, пока не кончился кислород и не догнал хищник!"],
            ["D1 → D7", "Личный подводный Аквариум-Музей (где плавают твои редкие существа и приносят доход), апгрейд баллона, ласт, фонаря и батискафа."],
            ["D28 / Live", "Глубоководные ивенты по субботам: «Пробуждение Левиафана», «Кровавый прилив», редкие мутации (сияющие/древние виды)."],
        ],
        "monetization": "Скины батискафов/скафандров, расширение аквариума, декор музея, 2x Удача на редкие мутации (умеренно, с открытыми шансами), VIP-эхолот.",
        "mvp": "1 коралловый риф + 1 тёмная впадина (2 уровня глубины), кислород, 10 существ с 3 редкостями, 1 маленький личный аквариум и 3 апгрейда снаряжения."
    },
    {
        "num": "09",
        "name": "Delivery Rush (Доставка на время)",
        "raw_score": 44,
        "upgraded_score": 65,
        "tier": "Tier B (500–2.5k CCU при добавлении хаоса/коопа)",
        "tier_col": AMBER,
        "dev_time": "2–3 недели (MVP)",
        "bull": "• Быстрый, супер-понятный цикл (взял заказ → домчал → получил деньги → купил крутой мопед/вертолёт).<br/>"
                "• <b>Taxi Boss</b> (4k–13k CCU) доказывает, что аркадная городская логистика + коллекция транспорта отлично монетизируется.<br/>"
                "• Относительно простой прототип для небольшой команды.",
        "bear": "• В базовом PDF игроки катаются в одиночку на таймер — нет взаимодействия между игроками (низкий intentional co-play).<br/>"
                "• Очень тяжело перебить <b>Taxi Boss</b> и <b>Driving Empire</b> обычной ездой.<br/>"
                "• Физика транспорта в Roblox на телефонах требует тонкой настройки (иначе машины переворачиваются и игроки уходят).",
        "loops": [
            ["0–10 сек", "Добавить безумие (Crazy Taxi + паркур): «Доставь хрупкую пиццу/бомбу через пробки, трамплины и крыши за 60 секунд!»"],
            ["1–3 мин", "Хрупкий груз (падает при ударе!), цепочка комбо-чаевых, короткие маршруты через крыши и переулки."],
            ["D1 → D7", "Гараж безумного транспорта (скутер с турбо, джетпак, дрон, спорткар, вертолёт), прокачка своей службы доставки."],
            ["D28 / Live", "Серверные гонки «Золотой заказ» (кто первый на сервере доставит 1 сверхдорогой груз — остальные могут перехватить!)."],
        ],
        "monetization": "Эксклюзивный транспорт (сбалансированный), скины/тюнинг/неон, 2x Чаевые, авто-навигатор с секретными срезами, Private Server.",
        "mvp": "1 компактный живой район, 1 аркадный скутер (простейшее мобильное управление!), 5 точек доставки, физика комбо-чаевых и 1 серверный «Золотой заказ» раз в 5 мин."
    },
    {
        "num": "10",
        "name": "Dream Park (Свой парк аттракционов)",
        "raw_score": 48,
        "upgraded_score": 67,
        "tier": "Tier B (1k–4k CCU, но дорогая разработка)",
        "tier_col": AMBER,
        "dev_time": "6–10 недель (тяжёлый MVP)",
        "bull": "• Жанр строительства парков — вечный хит (<b>Theme Park Tycoon 2</b>: 2k–3.5k CCU стабильно годами) с отличным Playtime и монетизацией.<br/>"
                "• В PDF есть классная идея: <b>тематические творческие раунды</b> (как Dress to Impress, только стройка парка!).<br/>"
                "• Игроки обожают кататься на аттракционах друзей.",
        "bear": "• Прямой бой с 10-летним монополистом <b>Theme Park Tycoon 2</b>, где можно строить любые американские горки.<br/>"
                "• Самая высокая техническая сложность из всех 10 идей: мобильный UI строительства, сетка, коллизии, ИИ толпы, сохранение огромных баз.<br/>"
                "• Риск застрять в разработке на 3–4 месяца без запуска.",
        "loops": [
            ["0–10 сек", "Не копировать сложный TPT2! Сделать <b>быстрый социальный Park-Battle (как DTI)</b> ИЛИ <b>модульный уютный парк за 1 клик</b>."],
            ["4–8 мин", "Если Park-Battle: 5 мин на сборку мини-парка по теме («Космос», «Хоррор», «Сладости») из готовых блоков → все катаются и голосуют!"],
            ["D1 → D7", "Открытие редких аттракционов и тем, а лучший парк сохраняется на твоём личном острове."],
            ["D28 / Live", "Тематические сезоны и голосования за «Парк недели» на главной площади."],
        ],
        "monetization": "Пакеты тем/аттракционов (VIP-горки, салюты, ночная подсветка), расширение участка, слоты сохранения парков, эмоции на аттракционах.",
        "mvp": "Только через модульные блоки (без ручной прокладки рельсов!): 1 участок, 10 готовых аттракционов/декора, катание на них с друзьями и голосование."
    },
]


def build_story():
    story = []

    # Page 1: Cover & Honest Two-Lens Explanation
    story += [
        Spacer(1, 8 * mm),
        tag("DEEP-DIVE PLAYBOOK • 10 ИДЕЙ × ПОЛНЫЙ РАЗБОР + ПЛАН РЕАЛИЗАЦИИ", PURPLE),
        Spacer(1, 5 * mm),
        P("Глубокий разбор 10 идей Roblox-игр", "TitleRU"),
        P("Два взгляда на каждую игру: «Топ-10 Roblox» vs «Прибыльный хит малой команды (500–5 000 CCU)»", "H1RU"),
        Spacer(1, 2.5 * mm),
        Rule(PINK, 1.8),
        Spacer(1, 3.5 * mm),
        callout(
            "Почему первый отчёт показался строгим — и что меняет этот глубокий разбор",
            "В первом отчёте мы оценивали все 10 идей <b>строго в том сыром виде, как они написаны на 1 странице</b>, и мерили их планкой <b>«выйдет ли в Топ-10 Roblox (50k–1M+ CCU)?»</b>. По такой жёсткой планке проваливается 99% любых сырых идей.<br/><br/>"
            "Но на практике в Roblox <b>не обязательно обгонять Steal a Brainrot, чтобы сделать успешный и прибыльный проект</b>. По рыночным ориентирам DevEx (<b>$0.0038 за 1 Robux</b>) при грамотной монетизации:<br/>"
            "• <b>500 CCU</b> ≈ $1 500 – $4 500 / мес gross (отличный старт для 1–2 человек)<br/>"
            "• <b>1 000 CCU</b> ≈ $3 000 – $10 000+ / мес gross (полноценная инди-студия из 2–3 друзей)<br/>"
            "• <b>3 000 CCU</b> ≈ $10 000 – $30 000+ / мес gross (сильный прибыльный бутик-хит)<br/><br/>"
            "Поэтому в этом документе мы даём <b>отдельную полную страницу на КАЖДУЮ из 10 игр</b>: честно разбираем <b>Bull Case</b> (почему МОЖЕТ выстрелить), <b>Bear Case</b> (где риски), <b>план переделки под 2026–2027</b>, <b>монетизацию</b> и <b>2-недельный MVP</b>.",
            BLUE, BLUE_BG
        ),
        Spacer(1, 4.5 * mm),
        P("Сводная таблица: «Как написано» vs «После апгрейда» (для команды 2–4 человека)", "H2RU"),
    ]

    summary = [["#", "Игра", "Сырая", "Апгрейд", "Реалистичный потолок (CCU)", "Срок MVP"]]
    for g in GAMES:
        summary.append([
            g["num"],
            g["name"],
            f"{g['raw_score']}",
            f"<b>{g['upgraded_score']}</b>",
            g["tier"],
            g["dev_time"],
        ])
    summary.append(["TOP", "Pink House / Dark Fantasy Keeper", "82", "<b>85+</b>", "Tier S–A (5k–50k+ CCU, флагман)", "Уже в работе!"])
    story += [
        make_table(summary, [8 * mm, 46 * mm, 13 * mm, 15 * mm, 68 * mm, 32 * mm]),
        Spacer(1, 3 * mm),
        P("Примечание: оценки CCU и дохода — индустриальные ориентиры (DevEx $0.0038/R$, RoTrack/Rolimon's/RoMonitor) и зависят от качества реализации, удержания D1/D7 и монетизации.", "SmallRU"),
        PageBreak(),
    ]

    # Pages 2-11: Dedicated 1-page deep dive for EACH of the 10 games
    for g in GAMES:
        story += [
            tag(f"ИДЕЯ #{g['num']}  •  СЫРАЯ: {g['raw_score']}/100  →  ПОСЛЕ АПГРЕЙДА: {g['upgraded_score']}/100", g["tier_col"]),
            Spacer(1, 2),
            P(f"{g['num']}. {g['name']}", "H1RU"),
            P(f"<b>Реалистичный потолок:</b> {g['tier']}   |   <b>Срок MVP:</b> {g['dev_time']}", "SmallRU"),
            Rule(g["tier_col"], 1.0, 3),
            two_col_boxes(
                "BULL CASE — Почему МОЖЕТ сработать", g["bull"],
                "BEAR CASE — Главные риски и конкуренты", g["bear"],
                GREEN, GREEN_BG, RED, RED_BG
            ),
            Spacer(1, 3.5 * mm),
            P("План переделки под 2026–2027 (как превратить идею в хит)", "H2RU"),
            make_table([["Горизонт", "Что должно происходить в игре (5-петлевая архитектура)"]] + g["loops"], [24 * mm, 158 * mm], head_bg=INK),
            Spacer(1, 3.5 * mm),
            make_table([
                ["Слой", "Конкретный план для команды"],
                ["Честная монетизация", g["monetization"]],
                ["Быстрый MVP-тест", g["mvp"]],
            ], [36 * mm, 146 * mm], head_bg=PURPLE),
            PageBreak(),
        ]

    # Page 12: Mini-Game Hub — When It Works vs When It Fails
    story += [
        tag("СПЕЦРАЗБОР • ФОРМАТ MINI-GAME HUB", PURPLE),
        Spacer(1, 2),
        P("Когда Mini-Game Hub работает, а когда убивает проект", "H1RU"),
        Rule(PURPLE, 1.0, 3),
        callout(
            "Главное правило 2026 года для хабов",
            "<b>Никогда не запускайте Mini-Game Hub на старте с 5 сырыми играми.</b> "
            "Запустите <b>1 самую сильную игру отдельно</b> (с чёткой обложкой и 10-секундным хуком). "
            "Когда она пробьёт 1 000+ CCU и соберёт аудиторию — добавьте в её лобби порталы во 2-ю и 3-ю игру как расширение вселенной!",
            AMBER, AMBER_BG
        ),
        Spacer(1, 4 * mm),
        make_table([
            ["Параметр", "Старт сразу с 5-в-1 Hub (опасно)", "Старт с 1 хита → потом Hub (правильно)"],
            ["Обложка / CTR в RFY", "Размытое обещание («всего понемногу») → низкий клик", "Кристально ясная фантазия → высокий PTR"],
            ["First-Play Bounce (<60с)", "Игрок теряется в лобби и порталах → высокий отвал", "Игрок попадает в экшен за 5–10 секунд"],
            ["Качество и баги", "Команда распыляется на 5 разных механик и UI", "100% сил в полировку 1 петли и мобильный FPS"],
            ["Масштабирование", "Если 4 игры слабые, они тянут вниз 1 сильную", "Сильная игра кормит трафиком новые режимы"],
        ], [36 * mm, 73 * mm, 73 * mm]),
        Spacer(1, 5 * mm),
        P("Три реалистичные стратегии для тебя и друзей на ближайшие 2–3 месяца", "H2RU"),
        make_table([
            ["Стратегия", "Какую игру делать", "Зачем выбирать именно её", "Ожидаемый потолок"],
            ["Путь A: Флагман (Рекомендуем)", "Pink House / Dark Fantasy Keeper + монстр из Don't Look Behind", "Карта и 3D-трава уже готовы! Уникальный визуал, ноль прямых клонов, идеальное попадание в тренд 2026–2027.", "5k – 50k+ CCU (Tier S–A)"],
            ["Путь B: Быстрый вирусный спринт", "Class Prank Chaos (бывш. Teacher Abuse) ИЛИ Build & Break Siege", "Свободная ниша, мгновенные смешные TikTok-клипы, быстрый MVP за 2–3 недели.", "2k – 15k+ CCU (Tier A)"],
            ["Путь C: Уютный кооп-бизнес", "Deep Ocean (с ловлей + аквариумом) ИЛИ Restaurant Chaos (Overcooked)", "Доказанная сильная монетизация (1k–3k CCU уже дают $4k–$20k/мес), но высокая конкуренция с Abyss / RT3.", "1k – 8k CCU (Tier B–A)"],
        ], [30 * mm, 44 * mm, 72 * mm, 36 * mm], head_bg=GREEN),
        Spacer(1, 5 * mm),
        P("Источники доп-исследования (24 ноября 2026)", "H2RU"),
        P("• DevEx $0.0038/R$ и ориентиры дохода 500 / 1 000 / 3 000 CCU: RoTrack, Roblox DevEx FAQ, индустриальные оценки.<br/>"
          "• Конкуренты кухни и разрушений: Restaurant Tycoon 3 (Ultraw), Cooking Chaos / Kitchen Chaos, Voxel Destruction Physics, Build A Boat, TDS.<br/>"
          "• Базовые тренды и психология: <code>output/pdf/Roblox_Trends_2020_2025_Deep_Research_RU.pdf</code> и <code>research/IDEA_VALIDATOR_ROUTER.md</code>.", "SourceRU"),
    ]

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
        title="Глубокий разбор 10 идей Roblox-игр (Playbook 2026–2027)",
        author="Antigravity Research for Dark Fantasy Roblox",
        subject="Deep-dive bull/bear, 5-loop redesign, monetization and MVP playbook for 10 Roblox game ideas",
    )
    frame = Frame(MARGIN_X, MARGIN_BOTTOM, PAGE_W - 2 * MARGIN_X, PAGE_H - MARGIN_TOP - MARGIN_BOTTOM, id="main")
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=on_page)])
    doc.build(build_story())
    print("Built:", OUT)


if __name__ == "__main__":
    main()
