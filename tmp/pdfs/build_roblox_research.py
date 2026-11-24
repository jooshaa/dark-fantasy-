from __future__ import annotations

import math
import os
from dataclasses import dataclass
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path("/Users/asal/Documents/roblox dev")
OUT = ROOT / "output/pdf/Roblox_Trends_2020_2025_Deep_Research_RU.pdf"

FONT_DIR = Path("/System/Library/Fonts/Supplemental")
pdfmetrics.registerFont(TTFont("Arial", str(FONT_DIR / "Arial.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Bold", str(FONT_DIR / "Arial Bold.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Italic", str(FONT_DIR / "Arial Italic.ttf")))
pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold", italic="Arial-Italic")


INK = HexColor("#111827")
MUTED = HexColor("#64748B")
PAPER = HexColor("#F7F8F4")
GREEN = HexColor("#1F7A5A")
GREEN2 = HexColor("#65A30D")
PINK = HexColor("#D9467A")
PURPLE = HexColor("#6D4AFF")
BLUE = HexColor("#2563EB")
CYAN = HexColor("#0891B2")
ORANGE = HexColor("#EA7C2B")
RED = HexColor("#DC2626")
GOLD = HexColor("#D4A017")
GRID = HexColor("#D9E0E7")
LIGHT = HexColor("#ECF2EF")

PAGE_W, PAGE_H = A4
MARGIN_X = 16 * mm
MARGIN_TOP = 17 * mm
MARGIN_BOTTOM = 15 * mm


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="TitleRU", fontName="Arial-Bold", fontSize=28, leading=31,
    textColor=INK, spaceAfter=8, alignment=TA_LEFT,
))
styles.add(ParagraphStyle(
    name="H1RU", fontName="Arial-Bold", fontSize=20, leading=23,
    textColor=INK, spaceAfter=8, spaceBefore=0,
))
styles.add(ParagraphStyle(
    name="H2RU", fontName="Arial-Bold", fontSize=12.5, leading=15,
    textColor=GREEN, spaceAfter=5, spaceBefore=8,
))
styles.add(ParagraphStyle(
    name="BodyRU", fontName="Arial", fontSize=9.1, leading=12.4,
    textColor=INK, spaceAfter=5,
))
styles.add(ParagraphStyle(
    name="SmallRU", fontName="Arial", fontSize=7.4, leading=9.8,
    textColor=MUTED, spaceAfter=3,
))
styles.add(ParagraphStyle(
    name="TinyRU", fontName="Arial", fontSize=6.2, leading=7.8,
    textColor=MUTED,
))
styles.add(ParagraphStyle(
    name="CalloutRU", fontName="Arial-Bold", fontSize=11.5, leading=15,
    textColor=INK, spaceAfter=5,
))
styles.add(ParagraphStyle(
    name="TableRU", fontName="Arial", fontSize=6.7, leading=8.2,
    textColor=INK,
))
styles.add(ParagraphStyle(
    name="TableHeadRU", fontName="Arial-Bold", fontSize=6.6, leading=8,
    textColor=colors.white,
))
styles.add(ParagraphStyle(
    name="SourceRU", fontName="Arial", fontSize=6.6, leading=8.6,
    textColor=INK, spaceAfter=4,
))


def P(text: str, style="BodyRU") -> Paragraph:
    return Paragraph(text, styles[style])


def bullet(text: str) -> Paragraph:
    return Paragraph(f"• {text}", styles["BodyRU"])


def tag(text: str, color=GREEN) -> Table:
    t = Table([[P(text, "SmallRU")]], colWidths=[None])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
        ("BOX", (0, 0), (-1, -1), 0, color),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


class Rule(Flowable):
    def __init__(self, color=GREEN, width=1.2, gap=5):
        super().__init__()
        self.color, self.line_width, self.gap = color, width, gap
        self.height = gap * 2

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.line_width)
        self.canv.line(0, self.gap, self._availWidth, self.gap)

    def wrap(self, availWidth, availHeight):
        self._availWidth = availWidth
        return availWidth, self.height


class BarChart(Flowable):
    def __init__(self, labels, values, colors_, title, suffix="", height=95*mm, max_value=None):
        super().__init__()
        self.labels = labels
        self.values = values
        self.colors = colors_
        self.title = title
        self.suffix = suffix
        self.height = height
        self.max_value = max_value or max(values) * 1.08

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        return availWidth, self.height

    def draw(self):
        c = self.canv
        c.setFont("Arial-Bold", 10)
        c.setFillColor(INK)
        c.drawString(0, self.height-12, self.title)
        top = self.height - 28
        bottom = 18
        left = 34
        right = self.width - 6
        n = len(self.values)
        gap = 6
        bw = (right-left-gap*(n-1))/n
        c.setStrokeColor(GRID)
        c.setLineWidth(.5)
        for i in range(5):
            y = bottom + (top-bottom)*i/4
            c.line(left, y, right, y)
            v = self.max_value*i/4
            c.setFont("Arial", 5.8)
            c.setFillColor(MUTED)
            c.drawRightString(left-4, y-2, f"{v:.0f}")
        for i, (lab, val, col) in enumerate(zip(self.labels, self.values, self.colors)):
            x = left + i*(bw+gap)
            h = (top-bottom)*val/self.max_value
            c.setFillColor(col)
            c.roundRect(x, bottom, bw, h, 2, stroke=0, fill=1)
            c.setFillColor(INK)
            c.setFont("Arial-Bold", 6.3)
            c.drawCentredString(x+bw/2, bottom+h+4, f"{val:g}{self.suffix}")
            c.setFont("Arial", 6.5)
            c.drawCentredString(x+bw/2, 6, str(lab))


class LineChart(Flowable):
    def __init__(self, labels, values, title, color=GREEN, height=80*mm, y_suffix=""):
        super().__init__()
        self.labels, self.values, self.title = labels, values, title
        self.color, self.height, self.y_suffix = color, height, y_suffix

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        return availWidth, self.height

    def draw(self):
        c = self.canv
        c.setFillColor(INK)
        c.setFont("Arial-Bold", 10)
        c.drawString(0, self.height-12, self.title)
        left, right, bottom, top = 34, self.width-8, 18, self.height-28
        vmin, vmax = 0, max(self.values)*1.08
        for i in range(5):
            y = bottom+(top-bottom)*i/4
            c.setStrokeColor(GRID)
            c.setLineWidth(.5)
            c.line(left, y, right, y)
            c.setFillColor(MUTED)
            c.setFont("Arial", 5.8)
            c.drawRightString(left-4, y-2, f"{vmax*i/4:.1f}{self.y_suffix}")
        pts=[]
        n=len(self.values)
        for i,v in enumerate(self.values):
            x=left+(right-left)*i/max(1,n-1)
            y=bottom+(top-bottom)*(v-vmin)/(vmax-vmin)
            pts.append((x,y))
        c.setStrokeColor(self.color)
        c.setLineWidth(2)
        p=c.beginPath(); p.moveTo(*pts[0])
        for pt in pts[1:]: p.lineTo(*pt)
        c.drawPath(p)
        for i,(x,y) in enumerate(pts):
            c.setFillColor(self.color); c.circle(x,y,2.4,stroke=0,fill=1)
            if i%6==0 or i==n-1:
                c.setFillColor(MUTED); c.setFont("Arial",5.2)
                c.drawCentredString(x,6,self.labels[i])
        c.setFillColor(self.color); c.setFont("Arial-Bold",6.2)
        c.drawString(pts[-1][0]-18, min(top-8,pts[-1][1]+7), f"{self.values[-1]:.1f}{self.y_suffix}")


class MatrixChart(Flowable):
    def __init__(self, points, title, height=95*mm):
        super().__init__(); self.points=points; self.title=title; self.height=height

    def wrap(self, availWidth, availHeight): self.width=availWidth; return availWidth,self.height

    def draw(self):
        c=self.canv; c.setFont("Arial-Bold",10); c.setFillColor(INK); c.drawString(0,self.height-12,self.title)
        l,b,r,t=48,27,self.width-12,self.height-30
        c.setFillColor(HexColor("#EEF7F2")); c.rect((l+r)/2,b,(r-l)/2,t-b,stroke=0,fill=1)
        c.setStrokeColor(GRID); c.setLineWidth(.8); c.rect(l,b,r-l,t-b,stroke=1,fill=0)
        c.line((l+r)/2,b,(l+r)/2,t); c.line(l,(b+t)/2,r,(b+t)/2)
        c.setFont("Arial",6.5); c.setFillColor(MUTED)
        c.drawString(l,b-13,"слабый сигнал"); c.drawRightString(r,b-13,"сильный сигнал")
        c.saveState(); c.translate(12,b); c.rotate(90); c.drawString(0,0,"короткий цикл  →  долгий цикл"); c.restoreState()
        for label,xv,yv,col in self.points:
            x=l+(r-l)*xv; y=b+(t-b)*yv
            c.setFillColor(col); c.circle(x,y,4,stroke=0,fill=1)
            c.setFillColor(INK); c.setFont("Arial",6.5); c.drawString(x+6,y-2,label)


class ResearchDoc(BaseDocTemplate):
    pass


def on_page(canvas, doc):
    if doc.page == 1:
        return
    canvas.saveState()
    canvas.setStrokeColor(GRID)
    canvas.setLineWidth(.5)
    canvas.line(MARGIN_X, 12*mm, PAGE_W-MARGIN_X, 12*mm)
    canvas.setFont("Arial", 6.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(MARGIN_X, 7.2*mm, "Roblox 2020–2025 • тренды, психология, прогноз")
    canvas.drawRightString(PAGE_W-MARGIN_X, 7.2*mm, str(doc.page))
    canvas.restoreState()


def section(title, kicker=None):
    out=[]
    if kicker: out += [tag(kicker), Spacer(1, 4)]
    out += [P(title,"H1RU"), Rule(), Spacer(1,3)]
    return out


def callout(title, body, color=GREEN):
    data=[[P(title,"CalloutRU")],[P(body,"BodyRU")]]
    t=Table(data,colWidths=[PAGE_W-2*MARGIN_X],hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),HexColor("#EEF7F2") if color==GREEN else HexColor("#F4F0FF")),
        ("BOX",(0,0),(-1,-1),1,color),
        ("LEFTPADDING",(0,0),(-1,-1),10),
        ("RIGHTPADDING",(0,0),(-1,-1),10),
        ("TOPPADDING",(0,0),(-1,-1),7),
        ("BOTTOMPADDING",(0,0),(-1,-1),7),
    ]))
    return t


def make_table(rows, widths, header=True, font_size=6.7, row_bg=True):
    formatted=[]
    for ri,row in enumerate(rows):
        st="TableHeadRU" if header and ri==0 else "TableRU"
        formatted.append([P(str(x),st) for x in row])
    t=Table(formatted,colWidths=widths,repeatRows=1 if header else 0,hAlign="LEFT")
    commands=[
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("GRID",(0,0),(-1,-1),.35,GRID),
        ("LEFTPADDING",(0,0),(-1,-1),4),
        ("RIGHTPADDING",(0,0),(-1,-1),4),
        ("TOPPADDING",(0,0),(-1,-1),4),
        ("BOTTOMPADDING",(0,0),(-1,-1),4),
    ]
    if header:
        commands += [("BACKGROUND",(0,0),(-1,0),INK),("TEXTCOLOR",(0,0),(-1,0),colors.white)]
    if row_bg:
        for r in range(1 if header else 0,len(rows)):
            if r%2==0: commands.append(("BACKGROUND",(0,r),(-1,r),HexColor("#F1F5F3")))
    t.setStyle(TableStyle(commands))
    return t


MONTHS = ["Янв","Фев","Мар","Апр","Май","Июн","Июл","Авг","Сен","Окт","Ноя","Дек"]


timeline = {
2020: [
    ("Adopt Me!","0,50B","MeepCity 0,20B","pet-care / trade","питомцы + обмен"),
    ("Adopt Me!","0,47B","Piggy 0,31B","pet + chapter horror","Piggy резко входит"),
    ("Adopt Me!","0,77B","Piggy 0,45B","social collection","локдаунный рост"),
    ("Adopt Me!","1,20B","Piggy 0,84B","social collection","массовый co-play"),
    ("Piggy","1,30B","Adopt Me! 1,30B","episodic horror","главы + YouTube"),
    ("Adopt Me!","1,20B","Piggy 1,00B","pet economy","обмен и редкость"),
    ("Adopt Me!","1,40B","Piggy 1,00B","pet economy","летний пик"),
    ("Adopt Me!","1,50B","Tower 1,10B","collection + mastery","Brookhaven появляется"),
    ("Adopt Me!","1,30B","Tower 1,00B","collection + obby","Brookhaven растёт"),
    ("Adopt Me!","1,50B","Tower 0,89B","event economy","сезонный апдейт"),
    ("Adopt Me!","1,30B","Tower 0,75B","social sandbox","Brookhaven #3"),
    ("Adopt Me!","1,40B","Tower 0,74B","social collection","holiday spend"),
],
2021: [
    ("Adopt Me!","1,00B","Tower 0,81B","pet economy","инерция 2020"),
    ("Adopt Me!","1,00B","Brookhaven 0,76B","pet ↔ roleplay","смена лидера близко"),
    ("Brookhaven","1,00B","Adopt Me! 0,99B","identity roleplay","свободная игра"),
    ("Brookhaven","1,00B","Adopt Me! 1,00B","identity roleplay","почти паритет"),
    ("Brookhaven","1,00B","Adopt Me! 0,72B","roleplay","социальная сцена"),
    ("Brookhaven","1,00B","Tower 0,67B","roleplay","лето"),
    ("Brookhaven","1,10B","Tower 0,66B","roleplay + PvP","BedWars входит"),
    ("Brookhaven","1,10B","Adopt Me! 0,74B","roleplay","BedWars растёт"),
    ("Brookhaven","1,00B","Adopt Me! 0,52B","roleplay + progression","Blox/PSX растут"),
    ("Brookhaven","0,87B","Adopt Me! 0,41B","roleplay","пост-летний спад"),
    ("Brookhaven","0,86B","Pet Sim X 0,57B","roleplay + collector","Squid Game shock"),
    ("Brookhaven","1,00B","Pet Sim X 0,64B","roleplay + collector","праздники"),
],
2022: [
    ("Brookhaven","1,20B","Pet Sim X 0,65B","roleplay","evergreen"),
    ("Brookhaven","0,96B","Pet Sim X 0,58B","roleplay","стабильность"),
    ("Brookhaven","0,84B","Pet Sim X 0,54B","roleplay","стабильность"),
    ("Brookhaven","0,86B","Blox Fruits 0,48B","roleplay ↔ RPG","RPG ускоряется"),
    ("Brookhaven","0,80B","Blox Fruits 0,55B","roleplay + RPG","power grind"),
    ("Brookhaven","0,92B","Blox Fruits 0,59B","roleplay + RPG","лето"),
    ("Brookhaven","1,10B","Blox Fruits 0,58B","roleplay + RPG","летний пик"),
    ("Brookhaven","1,10B","Blox Fruits 0,63B","roleplay + horror","Rainbow/DOORS входят"),
    ("Blox Fruits","0,88B","Brookhaven 0,80B","RPG + chase horror","DOORS/Evade"),
    ("Blox Fruits","1,10B","Brookhaven 0,85B","power RPG","horror держится"),
    ("Blox Fruits","1,00B","Brookhaven 0,76B","power RPG","evergreen"),
    ("Blox Fruits","1,20B","Brookhaven 0,99B","power RPG","holiday update"),
],
2023: [
    ("Blox Fruits","1,30B","Brookhaven 1,20B","power RPG","два evergreen"),
    ("Brookhaven","1,30B","Blox Fruits 1,20B","roleplay + horror","DOORS 0,60B"),
    ("Brookhaven","1,30B","Blox Fruits 1,20B","roleplay + RPG","PSX/DOORS"),
    ("Brookhaven","1,30B","Blox Fruits 1,20B","roleplay + RPG","PSX 0,59B"),
    ("Blox Fruits","1,10B","Brookhaven 1,10B","RPG ↔ roleplay","паритет"),
    ("Brookhaven","1,20B","Blox Fruits 1,00B","roleplay + horror","Rainbow spike"),
    ("Brookhaven","1,50B","Blox Fruits 1,10B","roleplay","Strongest входит"),
    ("Brookhaven","1,70B","Blox Fruits 1,00B","roleplay + battleground","TTD входит"),
    ("Brookhaven","1,20B","Blox Fruits 0,98B","skill PvP","Blade Ball 0,37B"),
    ("Blox Fruits","1,30B","Brookhaven 1,10B","RPG + skill PvP","Blade Ball 0,92B"),
    ("Blox Fruits","1,70B","Brookhaven 1,10B","RPG + TD","TTD 0,42B"),
    ("Blox Fruits","1,90B","Brookhaven 1,30B","RPG + collector","PS99 входит"),
],
2024: [
    ("Blox Fruits","1,80B","Brookhaven 1,70B","RPG + battleground","TTD/Blade Ball"),
    ("Blox Fruits","1,50B","Brookhaven 1,30B","RPG + battleground","Strongest 0,53B"),
    ("Brookhaven","1,40B","Blox Fruits 1,40B","roleplay + event","The Hunt"),
    ("Brookhaven","1,30B","Blox Fruits 1,20B","roadtrip survival","Dusty Trip/DTI"),
    ("Brookhaven","1,30B","Blox Fruits 1,30B","roleplay + fashion","DTI 0,25B"),
    ("Brookhaven","1,40B","Blox Fruits 1,30B","anime TD + fashion","Anime Defenders"),
    ("Brookhaven","1,80B","Blox Fruits 1,50B","social + fashion","DTI 0,48B"),
    ("Brookhaven","1,60B","Blox Fruits 1,50B","fashion + shooter","DTI/RIVALS"),
    ("Brookhaven","1,20B","Blox Fruits 1,20B","fashion + anime TD","DTI #3"),
    ("Blox Fruits","1,30B","Brookhaven 1,10B","RPG + fashion","DTI 0,84B"),
    ("Blox Fruits","1,10B","Brookhaven 1,00B","cozy fishing","Fisch входит"),
    ("Blox Fruits","2,20B","Brookhaven 1,30B","RPG + fishing","Fisch 0,69B"),
],
2025: [
    ("Blox Fruits","2,00B","Brookhaven 1,60B","RPG + shooter","RIVALS 0,80B"),
    ("Brookhaven","1,30B","Blox Fruits 1,20B","roleplay + shooter","Fisch/Dandy"),
    ("Brookhaven","1,50B","Blox Fruits 1,10B","expedition survival","Dead Rails 0,80B"),
    ("Brookhaven","1,50B","Dead Rails 1,40B","survival run","почти смена лидера"),
    ("Grow a Garden","3,50B","Dead Rails 1,60B","cozy incremental","новый масштаб"),
    ("Grow a Garden","8,30B","Steal a Brainrot 1,70B","idle/social economy","RFY acceleration"),
    ("Grow a Garden","9,10B","Steal a Brainrot 6,50B","cozy ↔ theft","admin events"),
    ("Steal a Brainrot","10,10B","Grow a Garden 7,50B","social theft/status","platform peak"),
    ("Steal a Brainrot","9,50B","99 Nights 4,70B","theft + survival","25M+ CCU"),
    ("Steal a Brainrot","8,90B","99 Nights 4,50B","theft + mutation","Plants v Brainrots"),
    ("Steal a Brainrot","7,70B","99 Nights 3,60B","theft + fishing","Fish It 0,93B"),
    ("Steal a Brainrot","7,10B","99 Nights 2,70B","theft + survival","The Forge входит"),
]}


leader_values = []
leader_labels = []
for y in range(2020, 2026):
    for i,row in enumerate(timeline[y]):
        leader_labels.append(f"{MONTHS[i]}{str(y)[2:]}")
        leader_values.append(float(row[1].replace("B","").replace(",",".")))


sources = [
    ("S01", "Roblox Creator Hub — Discovery", "https://create.roblox.com/docs/discovery"),
    ("S02", "Roblox Creator Hub — Analytics", "https://create.roblox.com/docs/production/analytics"),
    ("S03", "Roblox Creator Hub — Retention", "https://create.roblox.com/docs/production/analytics/retention"),
    ("S04", "Roblox Creator Hub — Monetization (включая ложную срочность и paid random items)", "https://create.roblox.com/docs/production/monetization"),
    ("S05", "Roblox — 2025 Replay: Search and Style", "https://about.roblox.com/newsroom/2025/12/roblox-replay-decoded-search-style"),
    ("S06", "Roblox — Infrastructure Supporting Record-Breaking Experiences", "https://about.roblox.com/newsroom/2025/06/roblox-infrastructure-supporting-record-breaking-games"),
    ("S07", "Roblox 2020 Form S-1/A", "https://d18rn0p25nwr6d.cloudfront.net/CIK-0001315098/a327f07f-86d6-461c-a020-83cb4882d100.pdf"),
    ("S08", "Roblox FY2021 results", "https://ir.roblox.com/news/news-details/2022/Roblox-Reports-Fourth-Quarter-and-Full-Year-2021-Financial-Results/default.aspx"),
    ("S09", "Roblox FY2022 results", "https://ir.roblox.com/news/news-details/2023/Roblox-Reports-Fourth-Quarter-and-Full-Year-2022-Financial-Results/"),
    ("S10", "Roblox FY2023 results", "https://ir.roblox.com/news/news-details/2024/Roblox-Reports-Fourth-Quarter-and-Full-Year-2023-Financial-Results/default.aspx"),
    ("S11", "Roblox FY2024 results", "https://ir.roblox.com/news/news-details/2025/Roblox-Reports-Fourth-Quarter-and-Full-Year-2024-Financial-Results/"),
    ("S12", "Roblox FY2025 annual report", "https://www.sec.gov/Archives/edgar/data/1315098/000110465926044380/rblx-20251231xars.pdf"),
    ("S13", "Roblox Q3 2025 filing", "https://d18rn0p25nwr6d.cloudfront.net/CIK-0001315098/d7ab90e9-e573-497d-82e9-1f6b7af0472b.pdf"),
    ("S14", "Roblox Wiki / Rolimon’s + Wayback — monthly top index", "https://roblox.fandom.com/wiki/Timeline_of_the_top_10_most-visited_games_per_month"),
    ("S15", "Monthly top 2020", "https://roblox.fandom.com/wiki/Timeline_of_the_top_10_most-visited_games_per_month/2020"),
    ("S16", "Monthly top 2021", "https://roblox.fandom.com/wiki/Timeline_of_the_top_10_most-visited_games_per_month/2021"),
    ("S17", "Monthly top 2022", "https://roblox.fandom.com/wiki/Timeline_of_the_top_10_most-visited_games_per_month/2022"),
    ("S18", "Monthly top 2023", "https://roblox.fandom.com/wiki/Timeline_of_the_top_10_most-visited_games_per_month/2023"),
    ("S19", "Monthly top 2024", "https://roblox.fandom.com/wiki/Timeline_of_the_top_10_most-visited_games_per_month/2024"),
    ("S20", "Monthly top 2025", "https://roblox.fandom.com/wiki/Timeline_of_the_top_10_most-visited_games_per_month/2025"),
    ("S21", "Dubit — turnover of Roblox Top 20 after RFY", "https://dubit.io/blog/roblox-top-20-rfy"),
    ("S22", "Newzoo — top Roblox experiences of 2025", "https://new.newzoo.com/articles/top-roblox-experiences-2025"),
    ("S23", "Associated Press — Grow a Garden", "https://apnews.com/article/2f5e4368448d57002d08b1b3d4a289ca"),
    ("S24", "Przybylski, Rigby & Ryan (2010) — Motivational Model of Video Game Engagement", "https://selfdeterminationtheory.org/SDT/documents/2010_PrzybylskiRigbyRyan_ROGP.pdf"),
    ("S25", "Ryan, Rigby & Przybylski (2006) — Motivational Pull of Video Games", "https://www.rochester.edu/warner/lida/wp-content/uploads/2022/11/02bfe513dd59366750000000.pdf"),
    ("S26", "Tomé et al. (CHI PLAY 2020) — Risking Treasure / loss aversion", "https://hci.usask.ca/wp-content/cache/mendeley-file-cache/6eb59aeb-38be-37ad-950c-7c625cb4cce2.pdf"),
]


def timeline_page(year):
    data=[["Месяц","Лидер","Визиты","Главный соперник","Механика","Сигнал"]]
    for m,row in zip(MONTHS,timeline[year]):
        data.append([m,row[0],row[1],row[2],row[3],row[4]])
    widths=[23*mm,31*mm,19*mm,36*mm,37*mm,37*mm]
    return section(f"{year}: помесячная карта", "72 МЕСЯЦА") + [
        P("Визиты — community-реконструкция Rolimon’s + Wayback, округление до миллионов/миллиардов. Это не официальные MAU и не уникальные игроки.","SmallRU"),
        Spacer(1,3), make_table(data,widths), Spacer(1,6),
        P(year_notes[year],"BodyRU"),
    ]


year_notes={
2020:"<b>Паттерн:</b> социальная коллекция (Adopt Me!) удерживает базу, а Piggy показывает, что сериализованный контент способен на несколько месяцев перехватить лидерство. Brookhaven входит позже, но уже демонстрирует силу открытого roleplay.",
2021:"<b>Паттерн:</b> лидерство переходит от коллекции к идентичности и социальному театру. Параллельно созревают три будущих столпа: skill PvP (BedWars), power progression (Blox Fruits) и collector economy (Pet Simulator X).",
2022:"<b>Паттерн:</b> evergreen-игры занимают вершину, но август–октябрь доказывает жизнеспособность короткого кооперативного horror-loop: Rainbow Friends, DOORS и Evade дают новый эмоциональный язык платформы.",
2023:"<b>Паттерн:</b> Brookhaven/Blox Fruits образуют устойчивый дуополий, но во втором полугодии быстро растут реактивные игровые форматы: Blade Ball, Toilet Tower Defense и The Strongest Battlegrounds. Важнее становится ясность одной механики.",
2024:"<b>Паттерн:</b> рынок дробится: fashion/voting (Dress to Impress), battleground, anime tower defense, roadtrip survival, shooter и fishing. Социальное самовыражение становится не менее сильным, чем сила персонажа.",
2025:"<b>Паттерн:</b> после изменения Recommended For You новые игры растут на порядок быстрее. Побеждает не жанр, а социально передаваемая система: выращивание, кража, совместное выживание, live-events и легко объяснимый прогресс.",
}


def build_story():
    story=[]
    # 1 Cover
    story += [Spacer(1,18*mm), tag("DEEP RESEARCH • DATA FREEZE: 2025-12-31", PURPLE), Spacer(1,10*mm),
              P("Roblox 2020–2025", "TitleRU"),
              P("Какие игры становились актуальными, почему игроки возвращались и что можно прогнозировать дальше", "H1RU"),
              Spacer(1,4*mm), Rule(PINK,2), Spacer(1,5*mm),
              P("Помесячная лента • недельный ритм • психология мотивации • влияние рекомендаций • прогноз 2026–2027 • выводы для нового проекта", "CalloutRU"),
              Spacer(1,18*mm),
              callout("Главный вывод", "С 2020 по 2024 вершину удерживали крупные evergreen-игры. В 2025 рост сместился к новым, чрезвычайно простым для объяснения системам, где действия игроков создают контент друг для друга: совместное выращивание, кража, статус, выживание и live-events. Копировать тему недостаточно — нужно воспроизвести социальный двигатель и удержание.", PURPLE),
              Spacer(1,16*mm),
              P("Подготовлено для проекта Pink House / Dark Fantasy Roblox", "H2RU"),
              P("Дата исследования: 24 ноября 2026. Все прогнозы построены с намеренной отсечкой данных на 31 декабря 2025, чтобы не подмешивать события 2026 года задним числом.", "SmallRU"),
              PageBreak()]

    # 2 Executive
    story += section("Резюме для принятия решения", "СНАЧАЛА СУТЬ")
    story += [callout("Не искать «следующий жанр»", "История показывает ротацию оболочек: pets → roleplay → RPG/horror → fashion → cozy/steal/survival. Стабильны не оболочки, а потребности: принадлежность, компетентность, автономия, статус, коллекция и повод вернуться с друзьями."), Spacer(1,7)]
    rows=[["Наблюдение","Что это значит"],
          ["2020: пандемийный скачок и Adopt Me/Piggy","Простая социальная система + сериализованные обновления масштабируются быстрее сложного контента."],
          ["2021–2024: Brookhaven/Blox Fruits — многолетние лидеры","Evergreen строится на свободе роли или длинной прогрессии; контент игроков заменяет часть production cost."],
          ["2022–2024: DOORS, Blade Ball, DTI, Fisch","Новый хит сначала выигрывает ясностью одной фантазии, затем удерживается мета-прогрессом и социальным ритуалом."],
          ["2025: Grow / Steal / 99 Nights","Сильнейшая формула — low-friction loop + shared server state + статус/риск + события по выходным."],
          ["Алгоритм RFY","После марта 2025 новые игры получили больше шансов, но масштаб сохраняется только при низком bounce и сильных D1–D28 сигналах."],
          ["Прогноз","Наиболее перспективны гибриды: cozy + риск, co-op survival + persistent sanctuary, social ownership + opt-in conflict."]]
    story += [make_table(rows,[54*mm,128*mm]),Spacer(1,7),P("<b>Рекомендация:</b> для dark-fantasy проекта не превращать красивую карту в пустую прогулку. Поверх Pink House нужен повторяемый социальный цикл: безопасное убежище → короткая экспедиция в бездну → добыча/существо/реликвия → улучшение дома → совместное событие → новый риск.","BodyRU"),PageBreak()]

    # 3 methodology
    story += section("Методика, качество данных и честные ограничения", "КАК ЧИТАТЬ")
    quality=[["Уровень","Источники","Для чего использован","Надёжность"],
             ["A — официальный","Roblox filings, Creator Hub, Newsroom","DAU, часы, алгоритм, сезонность, рекорды","высокая"],
             ["B — индустриальный","Newzoo/RoMonitor, Dubit, AP","концентрация, кейсы, внешняя проверка","средне-высокая"],
             ["C — community archive","Rolimon’s + Wayback через Roblox Wiki","помесячные визиты топ-игр","средняя"],
             ["D — вывод","категоризация и прогноз автора","объяснение паттернов, сценарии","вероятностная"]]
    story += [make_table(quality,[28*mm,54*mm,72*mm,28*mm]),Spacer(1,8),
              P("<b>Что означает «месяц»:</b> количество запусков/визитов игры за календарный месяц, а не уникальные игроки. Один игрок создаёт много визитов. Поэтому метрика хорошо показывает импульс, но не размер уникальной аудитории.","BodyRU"),
              P("<b>Что означает «неделя»:</b> полной открытой таблицы top games за все 313 недель 2020–2025 нет. Google Trends в ходе исследования вернул HTTP 429, а Roblox публично подтверждает только общий недельный ритм и отдельные рекорды. Недельный раздел — смесь официальной сезонности, событийных точек и явно помеченной модели, а не выдуманная временная серия.","BodyRU"),
              P("<b>Закрытые данные:</b> Creator Analytics конкретных игр, внутренние retention/monetization cohorts и коммерческие базы без доступа не использовались. Закрытые числа не реконструировались по слухам.","BodyRU"),
              callout("Критическое правило", "Корреляция не равна причине. Например, brainrot-тема совпала с ростом 2025 года, но одновременно изменились RFY-дистрибуция, общий размер платформы и live-event практика. Поэтому прогноз опирается на механизмы, а не на название мема.", PURPLE),PageBreak()]

    # 4 platform scale
    story += section("Платформа выросла в четыре раза", "МАСШТАБ")
    story += [BarChart([2020,2021,2022,2023,2024,2025],[32.6,45.5,56.0,68.4,82.9,127.0],[GREEN,GREEN,GREEN,GREEN,GREEN,PINK],"Средние DAU Roblox, млн",suffix=""),Spacer(1,4),
              BarChart([2020,2021,2022,2023,2024,2025],[30.6,41.4,49.3,60.0,73.5,123.9],[BLUE,BLUE,BLUE,BLUE,BLUE,PURPLE],"Часы вовлечения за год, млрд",suffix="",height=70*mm),
              P("Источники S07–S12. 2020 был ускорен локдаунами; 2025 — уже другой тип роста: новые игры, мобильная глобализация, рекомендации и социальная дистрибуция. Рост платформы усиливает рекорды, поэтому абсолютные визиты разных лет нельзя сравнивать без контекста.","SmallRU"),PageBreak()]

    # 5 eras chart
    story += section("72 месяца: скорость лидера", "МАКРО-КРИВАЯ")
    story += [LineChart(leader_labels,leader_values,"Месячные визиты игры №1, млрд",PINK,88*mm,"B"),Spacer(1,5),
              P("До 2024 лидер обычно находился около 0,8–2,2 млрд визитов в месяц. В мае–августе 2025 верхняя граница взлетела до 3,5–10,1 млрд. Это структурный разрыв, а не обычная сезонность.","BodyRU"),
              make_table([["Эра","Доминирующая формула","Тип удержания"],
                          ["2020","pet economy + episodic horror","коллекция / новая глава"],
                          ["2021","identity roleplay","друзья создают сюжет"],
                          ["2022","roleplay/RPG + co-op horror","долгая сила / эмоциональный run"],
                          ["2023","evergreen + one-mechanic PvP","мастерство / состязание"],
                          ["2024","fashion, battleground, anime TD, fishing","самовыражение / social vote"],
                          ["2025","cozy incremental, theft, survival, live-events","shared state / статус / риск"]],[31*mm,78*mm,73*mm]),PageBreak()]

    # 6 taxonomy
    story += section("Категории: не жанры, а психологические двигатели", "ТАКСОНОМИЯ")
    tax=[["Категория","Примеры","Обещание игроку","Петля","Риск"],
         ["Identity sandbox","Brookhaven, Berry Ave","«Я могу быть кем угодно»","роль → реакция друзей","пустота без компании"],
         ["Collect / care / trade","Adopt Me, Pet Sim","«Моё редкое существо»","получить → растить → обменять","pay-to-win / scam"],
         ["Power RPG","Blox Fruits","«Я стану сильнее»","бой → loot → skill unlock","grind fatigue"],
         ["Skill PvP","BedWars, Blade Ball, RIVALS","«Я лучше»","матч → mastery → rank","skill gap"],
         ["Co-op horror","Piggy, DOORS, Rainbow","«Переживём это вместе»","run → shock → knowledge","контент дорог"],
         ["Fashion / vote","Dress to Impress","«Меня увидят»","создать → показать → голос","toxicity / copying"],
         ["Cozy production","Grow, Fisch","«Мир растёт от моего ухода»","собрать → улучшить → автоматизировать","idle fatigue"],
         ["Social theft/status","Steal a Brainrot","«Рискну чужим/своим»","добыть → показать → защитить","loss rage"],
         ["Survival expedition","Dead Rails, 99 Nights","«Ещё один run»","готовиться → идти → вернуться","run too long"],
         ["Meme/IP response","Squid, brainrot clones","«Я внутри тренда»","узнать → поделиться","быстрый распад"]]
    story += [make_table(tax,[31*mm,35*mm,47*mm,42*mm,27*mm]),Spacer(1,6),
              P("Самые живучие игры обычно совмещают минимум два двигателя: Brookhaven = identity + relatedness; Blox Fruits = competence + collection; Grow = ownership + compounding; Steal = ownership + loss aversion + social status.","BodyRU"),PageBreak()]

    # 7-12 timelines
    for y in range(2020,2026):
        story += timeline_page(y) + [PageBreak()]

    # 13 transition map
    story += section("Как менялся интерес: от контента к системам", "ПАТТЕРН")
    story += [MatrixChart([
        ("Piggy: chapters",.25,.42,RED),("Brookhaven: roleplay",.58,.88,BLUE),
        ("Blox Fruits: progression",.65,.82,PURPLE),("DOORS: runs",.42,.62,RED),
        ("DTI: creation/vote",.72,.72,PINK),("Grow: compounding",.82,.78,GREEN2),
        ("Steal: social conflict",.92,.68,ORANGE),("meme clone",.55,.18,MUTED),
    ],"Сила сигнала × долговечность петли"),Spacer(1,5),
              P("<b>2020:</b> контент и коллекция. <b>2021–2023:</b> миры, где игроки сами создают истории, и длинная сила. <b>2024:</b> самовыражение и короткая демонстрация навыка. <b>2025:</b> shared-state системы, в которых каждый сервер сам производит драму, дефицит и клипы.","BodyRU"),
              callout("Проверяемая гипотеза", "Чем больше значимых событий создаются взаимодействием игроков, а не заранее сделанными катсценами, тем дешевле масштабировать контент и тем выше шанс на повторяемость. Но без честных правил такая система превращается в токсичность."),PageBreak()]

    # 14 weekly
    story += section("Недельный цикл: что действительно подтверждено", "НЕДЕЛИ")
    weekly=[["День","Наблюдение","Практический смысл","Статус"],
            ["Пн","обычно ниже выходных; анализ предыдущего пика","разбор ошибок/серверных метрик","официальная сезонность + inference"],
            ["Вт–Ср","будни ниже; удобно наращивать ожидание","тизер, creator seeding, A/B packaging","inference"],
            ["Чт","Roblox проверяет capacity для крупных updates","финальная QA/announcement","официально S06"],
            ["Пт","Roblox добавляет cloud capacity к weekend peak","релиз до пика, а не во время него","официально S06"],
            ["Сб","обычный недельный максимум рекомендаций","главный event / co-play moment","официально S01"],
            ["Вс","остаточный трафик и social catch-up","hotfix, мягкий второй повод","inference"]]
    story += [make_table(weekly,[20*mm,54*mm,76*mm,32*mm]),Spacer(1,7),
              callout("Событийные недельные точки 2025", "Dead Rails превысил 1 млн CCU в марте; Grow a Garden достиг 21,6 млн; в августе платформа фиксировала 45 млн одновременно в субботу; Steal a Brainrot превысил 25 млн в сентябре. Эти точки подтверждают силу update-weekend, но не заменяют полную недельную таблицу."),
              P("Для собственной игры нужен event calendar с cohort-измерением, а не вера в «магический день»: сравнивать PTR, bounce <60/61–180 sec, playtime, D1, D2–7, D8–28 и intentional co-play по источнику трафика.","BodyRU"),PageBreak()]

    # 15 monthly seasonality
    story += section("Месячная и годовая сезонность", "СЕЗОНЫ")
    season=[["Период","Наблюдаемый эффект","Что делать"],
            ["Июн–Авг","Roblox официально отмечает повышенную вовлечённость; летние рекорды повторяются в таблицах","крупный launch/update, социальные события, масштабирование инфраструктуры"],
            ["Сен–Ноя","после лета engagement обычно ниже; Halloween даёт тематический всплеск horror","не путать seasonal dip с поломкой игры; готовить horror/event packaging"],
            ["Дек","bookings исторически сильнее из-за праздников; обновления evergreen-игр часто заметны","giftable cosmetics, fair bundles, возвращение старых игроков"],
            ["Ян–Фев","инерция праздников быстро нормализуется","retention pass, новые cohorts, не завышать baseline"],
            ["Март–Май","окно для новых форматов до летнего пика; в 2025 Dead Rails/Grow начали перелом","launch readiness + быстрые итерации"]]
    story += [make_table(season,[30*mm,87*mm,65*mm]),Spacer(1,8),
              P("<b>Четырёхнедельная модель live-ops (inference):</b> W1 — новый объект/механика; W2 — социальная вариация; W3 — редкий риск/событие; W4 — bridge к следующему циклу. Если каждую неделю добавлять только новый item, novelty выгорает; если менять отношения между игроками, контент дольше самовоспроизводится.","BodyRU"),
              P("<b>Необходимый тест:</b> держать контрольную группу. Иначе update spike, школьный календарь и изменение алгоритма смешиваются в одну цифру.","BodyRU"),PageBreak()]

    # 16 psychology
    story += section("Почему игрок возвращается: модель потребностей", "ПСИХОЛОГИЯ")
    psych=[["Потребность","Игровое выражение","Сильные категории","Метрика"],
           ["Компетентность","становлюсь лучше, понимаю систему","RPG, PvP, obby, survival","progress, win rate, D7"],
           ["Автономия","выбираю роль, путь, стиль","roleplay, fashion, building","breadth, creation rate"],
           ["Связанность","друзья замечают и помогают","roleplay, co-op, trade","intentional co-play"],
           ["Владение/статус","это моё и это редкое","pets, garden, collectibles","showcase/trade"],
           ["Риск потери","хочу защитить накопленное","steal, extraction","return urgency, rage quit"],
           ["Новизна/любопытство","что будет дальше?","horror, events, meme","episode completion"],
           ["Ритуал/спокойствие","маленький знакомый прогресс","cozy, fishing, idle","play days, session cadence"]]
    story += [make_table(psych,[31*mm,58*mm,55*mm,38*mm]),Spacer(1,7),
              P("Исследования SDT связывают удовольствие и будущую игру с удовлетворением компетентности, автономии и связанности (S24–S25). CHI PLAY показал, что loss aversion сохраняется даже для виртуальных ресурсов (S26). Это объясняет силу stealing, но не оправдывает намеренное причинение вреда ребёнку.","BodyRU"),
              callout("Этическая граница", "Использовать риск как добровольную драму, а не как наказание за отсутствие. Никакой ложной срочности, скрытых odds, кражи paid items или pay-to-recover. Лучшее удержание создаёт желание вернуться, а не страх потерять."),PageBreak()]

    # 17 loop architecture
    story += section("Архитектура хита: пять вложенных петель", "ДИЗАЙН")
    loops=[["Горизонт","Вопрос игрока","Пример","Ошибка"],
           ["0–10 сек","Что это и зачем нажать?","дом + бездна + существо видно сразу","длинная заставка"],
           ["10–90 сек","Могу ли я что-то получить/сделать?","первая находка, выбор, мини-риск","tutorial без награды"],
           ["3–15 мин","Хочу ли ещё один цикл?","экспедиция / выращивание / матч","слишком длинный run"],
           ["1–7 дней","Есть ли незавершённая цель?","коллекция, дом, skill tree","только daily reward"],
           ["2–4 недели","Есть ли социальное событие?","server event, новый маршрут","контент без систем"],
           ["месяцы","Могу ли я показать историю?","редкие формы, sanctuary, статус","power reset без смысла"]]
    story += [make_table(loops,[26*mm,61*mm,56*mm,39*mm]),Spacer(1,7),
              P("RFY усиливает именно эту лестницу: play-through и first-play bounce проверяют вход; playtime/play days — короткий и средний цикл; D2–7/D8–28 — долговечность; intentional co-play — социальную петлю; spend days — устойчивость экономики.","BodyRU"),
              P("Следствие: красивый мир без понятного действия может дать хороший thumbnail CTR, но высокий first-play bounce. Система без визуальной фантазии может удержать узкую аудиторию, но плохо конвертировать показы. Нужны оба слоя.","BodyRU"),PageBreak()]

    # 18 case studies
    story += section("Четыре переломных кейса", "КЕЙСЫ")
    cases=[["Кейс","Почему взлетел","Почему держался/снизился","Урок"],
           ["Adopt Me / 2020","care + trade + редкость + друзья","живая экономика и обновления","ownership сильнее одиночного контента"],
           ["DOORS / 2022","понятный co-op horror run, клипы, знание опасностей","повтор через mastery; контентные затраты","страх работает, если игрок учится"],
           ["Dress to Impress / 2024","создание → демонстрация → голосование; каждая сессия новая","UGC-like variety, identity/status","игроки сами производят контент"],
           ["Grow / Steal / 2025","простая loop, shared server state, коллекция/риск, creator events","Grow быстрее снизился; Steal держал #1 6 месяцев","social system + live moment важнее темы"]]
    story += [make_table(cases,[36*mm,55*mm,55*mm,36*mm]),Spacer(1,8),
              P("Dubit сообщает: доля mature-игр в Top-20 visits упала с 84% до RFY до 18% спустя шесть месяцев; brand-new выросли до 60,7% к июню. При этом абсолютный трафик mature-игр не исчез — рынок расширился, а новый рост забрали свежие хиты (S21).", "BodyRU"),
              P("Newzoo отдельно отмечает ускорение и концентрацию 2025: Q2 впервые дал игру с >10 млн peak CCU; в Q3 таких было уже три (S22).", "BodyRU"),PageBreak()]

    # 19 forecast method
    story += section("Как прогнозировать без гадания", "МЕТОД")
    story += [P("Прогноз ниже не называет будущий хит по имени. Он ранжирует игровые системы по четырём наблюдаемым факторам:","BodyRU"),
              bullet("<b>Передаваемость:</b> можно ли объяснить игру одной фразой и показать 10-секундным клипом?"),
              bullet("<b>Социальная генеративность:</b> создают ли игроки новые ситуации друг для друга?"),
              bullet("<b>Долговечность:</b> есть ли D8–D28 причина вернуться без бесконечного production content?"),
              bullet("<b>Алгоритмический fit:</b> низкий bounce, play days, co-play, honest spend days?"),
              Spacer(1,5),
              MatrixChart([
                  ("cozy + risk",.84,.80,GREEN),("co-op survival",.75,.78,RED),
                  ("identity + creation",.72,.82,PINK),("skill PvP",.64,.72,BLUE),
                  ("pure meme clone",.78,.18,ORANGE),("solo cinematic",.32,.55,PURPLE),
                  ("idle-only",.58,.35,GOLD),("social ownership",.88,.74,CYAN),
              ],"Вероятность широкого сигнала × долговечность"),PageBreak()]

    # 20 forecast
    story += section("Прогноз 2026–2027 (по данным только до 2025)", "СЦЕНАРИИ")
    forecast=[["Сценарий","Уверенность","Почему","Ранний индикатор"],
              ["Cozy + danger","75%","Grow доказал compounding; Steal — риск владения","игрок возвращается защищать/развивать, но не rage-quits"],
              ["Co-op survival episodes","70%","Dead Rails/99 Nights соединяют run и социальную историю","друзья запускают повторные runs"],
              ["Social ownership","70%","pets/garden/brainrots — разные формы одного владения","showcase, trade, gifting без pay-to-win"],
              ["Identity + playable creation","60%","Brookhaven/DTI долговечны, игроки создают контент","высокий co-play и share rate"],
              ["Creator-led live events","65%","admin events стали культурным событием","Saturday peaks без обвала D1"],
              ["Sports/anime skill PvP","55%","RIVALS/Blue Lock/Strongest сохраняют спрос","skill mastery и spectating"],
              ["Чистый meme clone","25% на долгий срок","высокий старт, слабая уникальность","визиты есть, D8–D28 падает"]]
    story += [make_table(forecast,[43*mm,25*mm,76*mm,38*mm]),Spacer(1,7),
              P("Проценты — оценка уверенности в направлении, а не вероятность коммерческого успеха конкретной игры. Даже правильный тренд провалится при плохом onboarding, слабом performance, нечестной экономике или отсутствии update cadence.","SmallRU"),PageBreak()]

    # 21 concept recommendation
    story += section("Что строить поверх Pink House", "РЕКОМЕНДАЦИЯ")
    story += [callout("Рабочее направление: Dark Fantasy Keeper", "Игрок живёт в красивом розовом доме над бездной, спускается в короткие опасные экспедиции, спасает/связывает существ и реликвии, развивает личное убежище и переживает совместные ночные события. Визуальная карта остаётся ядром фантазии, но получает повторяемую систему."),Spacer(1,7)]
    concept=[["Слой","Реализация","Потребность","Проверка"],
             ["Promise","дом, лестница и бездна видны в первые секунды","любопытство","PTR/bounce"],
             ["60-sec reward","первая живая реликвия у края","компетентность/владение","tutorial complete"],
             ["Run 5–8 min","спуск → выбор риска → возврат","mastery/autonomy","session replay"],
             ["Sanctuary","существо меняет сад/интерьер","identity/ownership","D1/D7"],
             ["Co-play","один держит свет, другой несёт реликвию","relatedness","intentional co-play"],
             ["Opt-in conflict","охота за cursed shard, не кража paid pet","risk/status","rage quit guardrail"],
             ["Live event","ветер/тьма меняют маршрут в субботу","ritual/novelty","event cohort"],
             ["Monetization","косметика дома/существ, emotes, fair pass","expression","spend days без paywall"]]
    story += [make_table(concept,[30*mm,70*mm,45*mm,37*mm]),Spacer(1,6),
              P("Это не копия Grow или Steal. Это перенос их системных преимуществ — compounding ownership, social server state и live moments — в оригинальную dark-fantasy фантазию.","BodyRU"),PageBreak()]

    # 22 MVP plan
    story += section("Вертикальный срез: что проверить до большой игры", "MVP")
    mvp=[["Неделя","Что собрать","Критерий решения"],
         ["1","одна экспедиция, одна реликвия, возврат в дом","игрок без текста понимает цель <60 сек"],
         ["2","2-player dependency + death/recovery","co-play заметно повышает replay"],
         ["3","sanctuary upgrade + 6 collectibles","есть D1 reason без daily bribe"],
         ["4","один Saturday event + 2 packaging variants","event cohort лучше baseline, bounce не растёт"],
         ["5","mobile performance + economy guardrails","стабильный frame time на выбранном low-end"],
         ["6","soft launch с instrumented funnel","решение: iterate / pivot / stop"]]
    story += [make_table(mvp,[22*mm,91*mm,69*mm]),Spacer(1,8),
              P("<b>Минимальный telemetry funnel:</b> impression → play → 60 sec → first reward → first run → return home → upgrade → friend join → second run → D1/D7. Отдельно хранить source/thumbnail variant/device.","BodyRU"),
              P("<b>Stop rule:</b> не расширять карту, пока первый run не работает. Качество графики увеличивает доверие и желание исследовать, но не заменяет ясную цель и повтор.","BodyRU"),PageBreak()]

    # 23 metrics
    story += section("Dashboard, который нужен каждую неделю", "ИЗМЕРЕНИЕ")
    metrics=[["Слой","Метрика","Вопрос"],
             ["Packaging","impressions, PTR by thumbnail","обещание понятно?"],
             ["First minute","bounce <60 / 61–180 sec","игрок нашёл действие?"],
             ["Core loop","first reward, run complete, replay","петля доставляет удовольствие?"],
             ["Retention","D1, D7, D30; D2–7/D8–28 play days","есть причина вернуться?"],
             ["Social","intentional co-play, invites, party replay","друзья усиливают игру?"],
             ["Economy","spend days, payer conversion, refunds","монетизация честна и устойчива?"],
             ["Health","rage quit after loss, reports, scams","риск не разрушает доверие?"],
             ["Performance","frame time, memory, crashes by device","игра доступна массовой аудитории?"]]
    story += [make_table(metrics,[31*mm,77*mm,74*mm]),Spacer(1,8),
              P("Roblox подчёркивает: сравнение benchmark — ориентир, а не прямой фактор ранжирования. Главное — улучшать собственные cohorts, особенно новых пользователей из Home Recommendations.","BodyRU"),
              callout("Нельзя оптимизировать только CCU", "CCU — результат одновременности. Он может взлететь от события и рухнуть на следующий день. Для устойчивости нужны play days, long-term retention и co-play; для бизнеса — честные spend days, а не разовая паническая покупка."),PageBreak()]

    # 24 ethics and risk
    story += section("Риски, которые могут уничтожить хороший проект", "GUARDRAILS")
    risks=[["Риск","Как проявляется","Защита"],
           ["Clone trap","копируется тема, но не система","одна оригинальная social mechanic + уникальная fantasy"],
           ["Loss abuse","игрок теряет платное/редкое без согласия","opt-in zones, insurance earned by play, no paid theft"],
           ["False urgency","таймер постоянно сбрасывается","реальные сроки и прозрачные условия"],
           ["Randomized spend","неясные odds/региональные ограничения","PolicyService, disclosed odds, cosmetic alternatives"],
           ["Content treadmill","каждую неделю нужно делать новую карту","системы, где игроки создают вариативность"],
           ["Performance debt","визуал перегружает mobile","LOD, streaming, profile before claim"],
           ["Social toxicity","status превращается в harassment/scam","safe trade, consent, reporting, no public shaming"]]
    story += [make_table(risks,[35*mm,73*mm,74*mm]),Spacer(1,7),
              P("Психология здесь используется для понимания мотивации, а не для эксплуатации детей. Долгосрочный бренд строится на доверии; Roblox прямо не рекомендует leading giveaways, mismatched metadata и ложную срочность (S01, S04).", "BodyRU"),PageBreak()]

    # 25 conclusion
    story += section("Итог: формула следующего шага", "ВЫВОД")
    story += [P("<b>1. Визуальная фантазия:</b> Pink House и бесконечная травяная скала дают сильный, отличимый promise.","BodyRU"),
              P("<b>2. Одна фраза:</b> «Спускайся в бездну, спасай проклятых существ и перестраивай дом — но ночью бездна приходит за ними».","BodyRU"),
              P("<b>3. Один повторяемый run:</b> 5–8 минут, с выбором риска и понятным возвращением.","BodyRU"),
              P("<b>4. Социальная зависимость:</b> co-op должен менять решение, а не просто удваивать урон.","BodyRU"),
              P("<b>5. Persistent ownership:</b> сад, дом и существа сохраняют историю игрока.","BodyRU"),
              P("<b>6. Event cadence:</b> обновления меняют отношения и маршруты, а не только добавляют item.","BodyRU"),
              P("<b>7. Решение по данным:</b> сначала PTR/bounce/core-loop/D1/co-play; только потом масштаб карт и монетизация.","BodyRU"),
              Spacer(1,9),
              callout("Самая сильная ставка", "Не «сделать ещё один Steal a…», а построить красивый dark-fantasy мир, где владение имеет эмоциональный смысл, друзья реально нужны, а каждый сервер рождает новую историю. Это соединяет устойчивые мотивы 2020–2024 с системой роста 2025.", PURPLE),
              Spacer(1,8),
              P("Следующий практический документ: one-page Game Design Thesis + instrumented prototype specification для Pink House.","SmallRU"),PageBreak()]

    # 26-27 sources
    story += section("Источники", "БИБЛИОГРАФИЯ")
    for i,(sid,name,url) in enumerate(sources):
        if i==13:
            story += [PageBreak()] + section("Источники (продолжение)", "БИБЛИОГРАФИЯ")
        story.append(P(f"<b>{sid}</b> — {name}<br/><link href=\"{url}\" color=\"#2563EB\">{url}</link>","SourceRU"))
    story += [Spacer(1,4),P("Локальный фон: Roblox_Research_Reconstructed_RU.pdf. Он использован только как список вопросов/тем; сам файл прямо сообщает, что является реконструкцией без исходных восьми отчётов и не служит доказательством чисел.","SmallRU"),PageBreak()]

    # 28 appendix
    story += section("Приложение: что ещё собрать при доступе к закрытым данным", "DATA ROOM")
    backlog=[["Данные","Зачем","Минимальный формат"],
             ["Creator Analytics 10–20 игр","проверить retention, а не только visits","daily cohorts, source, device"],
             ["RoMonitor/Newzoo full history","полная weekly CCU и event shocks","hourly/daily CCU"],
             ["TikTok/YouTube creator posts","измерить social transmission","posts, views, publish time"],
             ["Update logs","связать механику и изменение метрик","timestamp + patch tags"],
             ["Economy sinks/sources","понять устойчивость владения","currency flow by cohort"],
             ["Player interviews 9–12 / 13–16 / 17+","разделить мотивы по возрасту","10–15 интервью/сегмент"]]
    story += [make_table(backlog,[48*mm,82*mm,52*mm]),Spacer(1,8),
              P("До получения этих данных прогноз следует использовать как портфель гипотез. Его ценность — не в точном угадывании следующего мема, а в сокращении пространства решений и формулировке тестов.","BodyRU"),
              P("Конец отчёта.","H2RU")]
    return story


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc=ResearchDoc(str(OUT),pagesize=A4,
                    leftMargin=MARGIN_X,rightMargin=MARGIN_X,
                    topMargin=MARGIN_TOP,bottomMargin=MARGIN_BOTTOM,
                    title="Roblox 2020–2025: тренды, психология и прогноз",
                    author="Codex research for Pink House project",
                    subject="Deep research on Roblox experience trends, 2020–2025")
    frame=Frame(MARGIN_X,MARGIN_BOTTOM,PAGE_W-2*MARGIN_X,PAGE_H-MARGIN_TOP-MARGIN_BOTTOM,id="normal")
    doc.addPageTemplates([PageTemplate(id="main",frames=[frame],onPage=on_page)])
    doc.build(build_story())
    print(OUT)


if __name__ == "__main__":
    main()
