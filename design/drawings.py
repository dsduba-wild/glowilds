#!/usr/bin/env python3
"""Draws the site's neon line-art pictures in the WILD colors.

How It Works: each step's drawing lives in a 1000x500 box, written twice:
  static/images/process-N.svg        wide (2000x714): drawing filling the half opposite the text, for desktop
  static/images/process-N-phone.svg  2:1 (1000x500): drawing alone, shown above the text on phones
Who We Help: one 750x500 card picture per industry, on a dark tile:
  static/work/<industry>-thumb.svg
Run from the repo root: python3 design/drawings.py
"""
import re
from pathlib import Path

G, P, B, U = "#52fe20", "#ff6dd6", "#4e83fe", "#cf56fe"  # WILD: green, pink, blue, purple; keep in step with $wild-* in assets/scss/_bootstrap-variables.scss
FAINT = "#26305e"

def defs(w, h):
    return f"""<defs>
<filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
  <feGaussianBlur stdDeviation="4" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<pattern id="dots" width="25" height="25" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.4" fill="{FAINT}"/></pattern>
<radialGradient id="fade"><stop offset="0.55" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>
<mask id="fadeMask"><rect width="{w}" height="{h}" fill="url(#fade)"/></mask>
</defs>"""

LABEL = 'font-family="Helvetica, Arial, sans-serif" font-size="21" letter-spacing="1.5"'


def label(x, y, text, color, anchor="middle"):
    return f'<text x="{x}" y="{y}" fill="{color}" {LABEL} text-anchor="{anchor}">{text}</text>'


def tool(cx, cy, color, icon, text, ty):
    """A round badge with an icon and a label, like a tool clipped onto the plan."""
    return (f'<circle cx="{cx}" cy="{cy}" r="34" fill="#060818" stroke="{color}" stroke-width="3"/>'
            f'<g transform="translate({cx},{cy})" stroke="{color}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round">{icon}</g>'
            + label(cx, cy + ty, text, color))


MAGNIFIER = '<circle cx="-5" cy="-5" r="11"/><path d="M3 3l11 11"/>'
WRENCH = '<path d="M-12 12l14-14M2-2a9 9 0 1 0 8-12l-6 6-5-5 6-6a9 9 0 0 0-12 8"/>'
STAR = '<path d="M0-15l4.5 9.5 10.5 1.5-7.5 7 2 10.5L0 8.5l-9.5 5 2-10.5-7.5-7 10.5-1.5z"/>'
CHAT = '<path d="M-15-11h30v19h-16l-9 8v-8h-5z"/><path d="M-7-2h0M0-2h0M7-2h0"/>'
GEAR = ('<circle r="7"/><path d="M0-17v6M0 11v6M-17 0h6M11 0h6M-12-12l4 4M8 8l4 4M-12 12l4-4M8-8l4-4"/>')
CHECK = '<path d="M-12 1l8 8 16-17"/>'
PLAY = '<path d="M-7-11l18 11-18 11z"/>'


def step1():
    """Business check-up: the business laid out on a folded map, a planned route, and tools clipped on."""
    s = []
    # folded map, three panels
    s.append(f'<path d="M290 110 L430 85 L570 110 L710 85 L710 395 L570 420 L430 395 L290 420 Z" fill="none" stroke="{B}" stroke-width="3"/>')
    s.append(f'<path d="M430 85 L430 395 M570 110 L570 420" stroke="{B}" stroke-width="2" stroke-dasharray="6 6" opacity=".7"/>')
    # streets and a river
    for d in ("M300 190 L700 170", "M300 300 L700 285", "M370 108 L380 410", "M640 95 L650 405"):
        s.append(f'<path d="{d}" stroke="{FAINT}" stroke-width="5"/>')
    s.append(f'<path d="M292 360 C380 330 430 380 520 340 S650 300 708 330" fill="none" stroke="{U}" stroke-width="3" opacity=".7"/>')
    # planned route between pins
    s.append(f'<path d="M340 360 C360 260 450 250 470 210 S560 150 600 230 S640 300 660 150" fill="none" stroke="{G}" stroke-width="3.5" stroke-dasharray="10 8"/>')
    for x, y in ((340, 360), (470, 210), (600, 230), (660, 150)):
        s.append(f'<path d="M{x} {y} c-12-16-12-30 0-30 s12 14 0 30z" fill="#060818" stroke="{P}" stroke-width="3"/><circle cx="{x}" cy="{y-20}" r="4" fill="{P}"/>')
    # tools clipped on, with leader lines to the map
    for (cx, cy, color, icon, text, ty, mx, my) in (
        (150, 130, G, MAGNIFIER, "GOOGLE", 58, 290, 160),
        (150, 370, P, WRENCH, "DAILY OPS", 58, 290, 350),
        (850, 130, U, STAR, "REVIEWS", 58, 710, 150),
        (850, 370, B, CHAT, "CALLS", 58, 710, 340),
    ):
        s.append(f'<path d="M{cx + (34 if cx < 500 else -34)} {cy} L{mx} {my}" stroke="{color}" stroke-width="2" stroke-dasharray="4 5"/>')
        s.append(tool(cx, cy, color, icon, text, ty))
    return "".join(s)


def step2():
    """Build: a blueprint of the website, AI helper and automations being put together."""
    s = []
    # browser wireframe
    s.append(f'<rect x="170" y="90" width="420" height="300" rx="14" fill="none" stroke="{B}" stroke-width="3"/>')
    s.append(f'<path d="M170 130 H590" stroke="{B}" stroke-width="3"/>')
    for i, c in enumerate((P, U, G)):
        s.append(f'<circle cx="{195 + i * 22}" cy="110" r="6" fill="none" stroke="{c}" stroke-width="2.5"/>')
    s.append(f'<rect x="200" y="155" width="360" height="70" rx="6" fill="none" stroke="{U}" stroke-width="2.5"/>')
    s.append(f'<path d="M220 180 H420 M220 202 H360" stroke="{U}" stroke-width="3" stroke-linecap="round"/>')
    for i in range(3):
        s.append(f'<rect x="{200 + i * 124}" y="245" width="112" height="110" rx="6" fill="none" stroke="{FAINT}" stroke-width="3"/>')
    s.append(f'<path d="M222 330 H290" stroke="{G}" stroke-width="3" stroke-linecap="round"/><rect x="460" y="320" width="76" height="22" rx="11" fill="none" stroke="{G}" stroke-width="2.5"/>')
    # phone wireframe overlapping
    s.append(f'<rect x="540" y="200" width="120" height="220" rx="18" fill="#060818" stroke="{P}" stroke-width="3"/>')
    s.append(f'<path d="M585 218 H615 M560 250 H640 M560 270 H620 M560 290 H630" stroke="{P}" stroke-width="3" stroke-linecap="round"/>')
    s.append(f'<rect x="560" y="370" width="80" height="26" rx="13" fill="none" stroke="{G}" stroke-width="2.5"/>')
    # blueprint dimension line
    s.append(f'<path d="M170 435 H590 M170 425 V445 M590 425 V445" stroke="{FAINT}" stroke-width="2"/>')
    s.append(label(380, 470, "YOUR WEBSITE", B))
    # AI helper and automation gears, wired in
    s.append(f'<path d="M660 250 C720 250 720 150 770 150 M660 330 C720 330 720 360 770 360" fill="none" stroke="{FAINT}" stroke-width="3"/>')
    s.append(tool(805, 150, P, CHAT, "AI HELPER", 60))
    s.append(f'<g transform="translate(805,360)" fill="none" stroke-width="3">'
             f'<g stroke="{U}"><circle r="28"/><circle r="10"/>'
             + "".join(f'<path d="M0 -28 V-38" transform="rotate({a})"/>' for a in range(0, 360, 45))
             + f'</g><g stroke="{G}" transform="translate(48,-30)"><circle r="16"/><circle r="5"/>'
             + "".join(f'<path d="M0 -16 V-23" transform="rotate({a})"/>' for a in range(0, 360, 60))
             + '</g></g>')
    s.append(label(805, 425, "AUTOMATIONS", U))
    return "".join(s)


def step3():
    """Launch & learn: the system goes live, and a short walkthrough shows how it works."""
    s = []
    # laptop
    s.append(f'<rect x="240" y="170" width="330" height="210" rx="12" fill="none" stroke="{B}" stroke-width="3"/>')
    s.append(f'<path d="M200 400 H610 L585 380 H225 Z" fill="none" stroke="{B}" stroke-width="3" stroke-linejoin="round"/>')
    # rocket leaving the screen
    s.append(f'<path d="M395 330 C400 285 418 240 438 208" fill="none" stroke="{P}" stroke-width="3" stroke-dasharray="3 9" stroke-linecap="round"/>')
    s.append(f'<g transform="translate(480,150) rotate(40) scale(1.25)" fill="none" stroke-width="2.6" stroke-linejoin="round">'
             f'<path d="M0-70 C24-46 24 0 14 30 H-14 C-24 0 -24-46 0-70Z" stroke="{U}"/>'
             f'<circle cy="-22" r="9" stroke="{B}"/>'
             f'<path d="M-14 8 L-32 34 L-12 30 M14 8 L32 34 L12 30" stroke="{U}"/>'
             f'<path d="M-8 34 Q0 70 8 34" stroke="{P}"/><path d="M-3 36 Q0 52 3 36" stroke="{G}"/></g>')
    s.append(label(405, 365, "LIVE", G))
    # walkthrough card: three checked steps
    s.append(f'<rect x="680" y="120" width="210" height="250" rx="14" fill="none" stroke="{G}" stroke-width="3"/>')
    s.append(label(785, 155, "HOW IT WORKS", G))
    for i in range(3):
        y = 195 + i * 55
        s.append(f'<g transform="translate(712,{y}) scale(.75)" stroke="{G}" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round">{CHECK}</g>')
        s.append(f'<path d="M740 {y} H{860 - i * 25}" stroke="{FAINT}" stroke-width="5" stroke-linecap="round"/>')
    # quick call bubble
    s.append(f'<path d="M610 240 C640 240 650 230 680 230" fill="none" stroke="{FAINT}" stroke-width="3"/>')
    s.append(tool(130, 260, P, PLAY, "QUICK CALL", 60))
    s.append(f'<path d="M164 260 H240" stroke="{P}" stroke-width="2" stroke-dasharray="4 5"/>')
    return "".join(s)


def step4():
    """Grow: calls, reviews and bookings rising over time, kept on track."""
    s = []
    # axes
    s.append(f'<path d="M200 90 V410 H820" fill="none" stroke="{FAINT}" stroke-width="3"/>')
    # rising bars in the four colors
    for i, (c, h) in enumerate(((G, 70), (P, 120), (B, 180), (U, 250))):
        x = 245 + i * 145
        s.append(f'<rect x="{x}" y="{410 - h}" width="70" height="{h}" rx="6" fill="none" stroke="{c}" stroke-width="3"/>')
    # trend arrow
    s.append(f'<path d="M230 330 C380 300 480 240 560 200 S700 120 790 95" fill="none" stroke="{G}" stroke-width="3.5"/>')
    s.append(f'<path d="M766 88 L792 94 L778 117" fill="none" stroke="{G}" stroke-width="3.5" stroke-linejoin="round" stroke-linecap="round"/>')
    # stars over the tallest bar, a sprout at the base
    for dx in (-30, 0, 30):
        s.append(f'<g transform="translate({715 + dx},{125 + abs(dx) // 3}) scale(.7)" stroke="{P}" stroke-width="3" fill="none" stroke-linejoin="round">{STAR}</g>')
    s.append(f'<path d="M180 410 V370 M180 385 C160 380 155 365 160 355 C175 360 180 372 180 385 M180 375 C195 365 205 350 200 340 C188 345 180 358 180 375" fill="none" stroke="{G}" stroke-width="3" stroke-linecap="round"/>')
    for x, t, c in ((280, "CALLS", G), (425, "REVIEWS", P), (570, "BOOKINGS", B), (715, "TIME BACK", U)):
        s.append(label(x, 440, t, c))
    return "".join(s)


def svg(width, height, inner, fade=(1000, 500)):
    """fade: size of the drawing box the dot grid fades within."""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">'
            f'{defs(*fade)}{inner}</svg>\n')


def drawing(body):
    """The 1000x500 drawing: faded dot grid behind neon line art."""
    return f'<rect width="1000" height="500" fill="url(#dots)" mask="url(#fadeMask)"/><g filter="url(#glow)">{body}</g>'


MOON = '<path d="M8-16a18 18 0 1 0 10 28A15 15 0 0 1 8-16z"/>'
BELL = '<path d="M-13 8V-2a13 13 0 0 1 26 0V8l4 5h-34z"/><path d="M-4 17a4 4 0 0 0 8 0"/>'


def calendar(x, y, w, h, color, mark=CHECK):
    """A calendar page with a grid and a mark on the booked day."""
    cells = "".join(f'<path d="M{x + 12} {y + 40 + r * (h - 52) / 3:.0f} H{x + w - 12}" stroke="{FAINT}" stroke-width="2"/>' for r in range(1, 3))
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#060818" stroke="{color}" stroke-width="3"/>'
            f'<path d="M{x} {y + 30} H{x + w} M{x + 25} {y - 8} V{y + 12} M{x + w - 25} {y - 8} V{y + 12}" stroke="{color}" stroke-width="3" stroke-linecap="round"/>'
            + cells +
            f'<g transform="translate({x + w / 2},{y + 30 + (h - 30) / 2})" stroke="{G}" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round">{mark}</g>')


def contractors():
    """A missed call on the job becomes a booked job, and the evening stays free."""
    s = []
    # house frame going up, with a ladder
    s.append(f'<path d="M70 250 L215 130 L360 250" fill="none" stroke="{B}" stroke-width="3" stroke-linejoin="round"/>')
    s.append(f'<rect x="100" y="240" width="230" height="190" fill="none" stroke="{B}" stroke-width="3"/>')
    s.append("".join(f'<path d="M{x} 245 V425" stroke="{FAINT}" stroke-width="4"/>' for x in (145, 190, 240, 285)))
    s.append(f'<rect x="135" y="290" width="60" height="50" fill="none" stroke="{U}" stroke-width="2.5"/><rect x="250" y="330" width="50" height="100" fill="none" stroke="{U}" stroke-width="2.5"/>')
    s.append(f'<path d="M350 440 L392 215 M388 440 L428 215" stroke="{P}" stroke-width="3" stroke-linecap="round"/>'
             + "".join(f'<path d="M{354 + i * 7.5} {418 - i * 40} H{392 + i * 7.5}" stroke="{P}" stroke-width="3" stroke-linecap="round"/>' for i in range(5)))
    # ringing phone -> booked calendar
    s.append(f'<rect x="455" y="200" width="80" height="140" rx="14" fill="#060818" stroke="{P}" stroke-width="3"/><path d="M482 216 H508" stroke="{P}" stroke-width="3" stroke-linecap="round"/>')
    s.append(f'<path d="M470 190 a40 40 0 0 1 50 0 M460 176 a55 55 0 0 1 70 0" fill="none" stroke="{P}" stroke-width="2.5" stroke-linecap="round"/>')
    s.append(f'<path d="M548 270 H585" stroke="{G}" stroke-width="3" stroke-dasharray="4 5"/><path d="M578 262 L588 270 L578 278" fill="none" stroke="{G}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
    s.append(calendar(612, 215, 110, 120, G))
    s.append(label(495, 370, "CALL CAUGHT", P) + label(667, 405, "JOB BOOKED", G))
    # evening back
    s.append(f'<g transform="translate(640,95)" stroke="{U}" stroke-width="3" fill="none" stroke-linejoin="round">{MOON}</g>')
    s.append(f'<g transform="translate(590,70) scale(.45)" stroke="{U}" stroke-width="4" fill="none" stroke-linejoin="round">{STAR}</g>')
    s.append(label(640, 150, "EVENINGS BACK", U))
    return "".join(s)


def local_shops():
    """A storefront found on the map, questions answered, sales logged."""
    s = []
    s.append(f'<rect x="80" y="210" width="290" height="220" fill="none" stroke="{B}" stroke-width="3"/>')
    for i, c in enumerate((G, P, B, U, G, P, B)):
        x = 80 + i * 41.4
        s.append(f'<path d="M{x:.0f} 175 H{x + 41.4:.0f} V210 a20.7 20.7 0 0 1 -41.4 0 Z" fill="none" stroke="{c}" stroke-width="2.5" stroke-linejoin="round"/>')
    s.append(f'<path d="M70 175 H380" stroke="{B}" stroke-width="3"/>')
    s.append(f'<rect x="110" y="270" width="120" height="90" fill="none" stroke="{U}" stroke-width="2.5"/><rect x="265" y="270" width="75" height="160" fill="none" stroke="{U}" stroke-width="2.5"/>')
    s.append(f'<rect x="125" y="300" width="40" height="22" rx="4" fill="none" stroke="{G}" stroke-width="2"/>' + label(145, 316, "OPEN", G).replace('font-size="21"', 'font-size="12"'))
    # map pin above with pulse rings
    s.append(f'<path d="M225 128 c-24-30-24-58 0-58 s24 28 0 58z" fill="#060818" stroke="{P}" stroke-width="3"/><circle cx="225" cy="90" r="8" fill="none" stroke="{P}" stroke-width="3"/>')
    s.append(f'<ellipse cx="225" cy="135" rx="40" ry="9" fill="none" stroke="{P}" stroke-width="2" opacity=".6"/>')
    # question and answer bubbles
    s.append(f'<path d="M430 120 h220 v70 h-170 l-25 22 v-22 h-25 z" fill="none" stroke="{B}" stroke-width="3" stroke-linejoin="round"/>' + label(540, 163, "OPEN SUNDAY?", B))
    s.append(f'<path d="M470 225 h230 v70 h-25 v22 l-25 -22 h-180 z" fill="none" stroke="{G}" stroke-width="3" stroke-linejoin="round"/>' + label(585, 268, "YES, 10 TO 4", G))
    # receipt
    s.append(f'<path d="M520 340 h120 v100 l-15 -10 -15 10 -15 -10 -15 10 -15 -10 -15 10 -15 -10 -15 10 z" fill="none" stroke="{U}" stroke-width="3" stroke-linejoin="round"/>'
             + "".join(f'<path d="M538 {365 + i * 20} H{620 - i * 15}" stroke="{U}" stroke-width="3" stroke-linecap="round"/>' for i in range(3)))
    s.append(label(670, 470, "SALES LOGGED", U, "end"))
    return "".join(s)


def professional_care():
    """Trusted online, consultations booked, reminders sent, intake ready."""
    s = []
    s.append(f'<path d="M180 90 L280 125 V230 C280 300 230 345 180 370 C130 345 80 300 80 230 V125 Z" fill="none" stroke="{B}" stroke-width="3" stroke-linejoin="round"/>')
    s.append(f'<g transform="translate(180,230) scale(1.8)" stroke="{G}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round">{CHECK}</g>')
    s.append(label(180, 420, "TRUSTED", B))
    s.append(calendar(340, 150, 150, 150, G))
    s.append(label(415, 345, "BOOKED", G))
    s.append(f'<g transform="translate(415,75)" stroke="{P}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round">{BELL}</g>')
    s.append(f'<path d="M446 52 a30 30 0 0 1 10 22 M384 52 a30 30 0 0 0 -10 22" fill="none" stroke="{P}" stroke-width="2.5" stroke-linecap="round"/>')
    s.append(label(505, 82, "REMINDER SENT", P, "start"))
    # intake clipboard
    s.append(f'<rect x="545" y="170" width="140" height="190" rx="10" fill="none" stroke="{U}" stroke-width="3"/><rect x="585" y="158" width="60" height="24" rx="6" fill="#060818" stroke="{U}" stroke-width="3"/>')
    for i in range(4):
        y = 215 + i * 35
        s.append(f'<rect x="562" y="{y - 10}" width="18" height="18" rx="3" fill="none" stroke="{U}" stroke-width="2"/><path d="M592 {y} H{668 - (i % 2) * 20}" stroke="{FAINT}" stroke-width="5" stroke-linecap="round"/>')
        if i < 3:
            s.append(f'<path d="M565 {y} l5 5 9 -11" fill="none" stroke="{G}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>')
    s.append(label(615, 400, "INTAKE READY", U))
    return "".join(s)


def nonprofits():
    """Volunteers, events and donations coming together around the mission."""
    s = []
    for cx, c, sc in ((235, G, 1), (375, P, 1.2), (515, B, 1)):
        s.append(f'<g transform="translate({cx},300) scale({sc})" fill="none" stroke="{c}" stroke-width="3" stroke-linecap="round">'
                 f'<circle cy="-42" r="26"/><path d="M-50 55 C-50 -10 50 -10 50 55"/></g>')
    s.append(f'<path d="M375 150 C375 135 395 120 410 135 C425 150 400 170 375 188 C350 170 325 150 340 135 C355 120 375 135 375 150Z" fill="none" stroke="{P}" stroke-width="3" stroke-linejoin="round"/>')
    s.append(f'<path d="M150 390 H600" stroke="{FAINT}" stroke-width="3"/>')
    s.append(label(375, 435, "VOLUNTEERS", G))
    s.append(calendar(60, 90, 110, 110, U, STAR))
    s.append(label(115, 235, "EVENTS", U))
    # donation box with a coin
    s.append(f'<rect x="590" y="140" width="110" height="80" rx="8" fill="none" stroke="{B}" stroke-width="3"/><path d="M625 155 H665" stroke="{B}" stroke-width="4" stroke-linecap="round"/>')
    s.append(f'<circle cx="645" cy="105" r="16" fill="none" stroke="{G}" stroke-width="3"/><path d="M645 98 V112" stroke="{G}" stroke-width="3" stroke-linecap="round"/>')
    s.append(label(645, 255, "DONATIONS", B))
    return "".join(s)


def tile(body):
    """A 750x500 card picture: dark tile, faded dot grid, neon line art."""
    return (f'<rect width="750" height="500" fill="#060818"/>'
            f'<rect width="750" height="500" fill="url(#dots)" mask="url(#fadeMask)"/><g filter="url(#glow)">{body}</g>')


WORK = {"contractors": contractors, "local-shops": local_shops, "professional-care": professional_care, "nonprofits": nonprofits}

STEPS = {1: step1, 2: step2, 3: step3, 4: step4}


def picture_side(n):
    """The drawing goes opposite the step's text, so read `align:` from its content file (text is left unless it says right)."""
    m = re.search(r"^align:\s*['\"]?(\w+)", Path(f"content/pages/process/content{n}.md").read_text(), re.M)
    return "left" if m and m.group(1) == "right" else "right"

if __name__ == "__main__":
    out = Path("static/images")
    for n, draw in STEPS.items():
        side = picture_side(n)
        d = drawing(draw())
        (out / f"process-{n}-phone.svg").write_text(svg(1000, 500, d))
        # wide version: the drawing fills one half; the picture is scaled to the section's height on desktop
        x = 0 if side == "left" else 1000
        (out / f"process-{n}.svg").write_text(svg(2000, 714, f'<g transform="translate({x},107)">{d}</g>'))
        print(f"process-{n}.svg, process-{n}-phone.svg (drawing on the {side})")
    for slug, draw in WORK.items():
        (Path("static/work") / f"{slug}-thumb.svg").write_text(svg(750, 500, tile(draw()), fade=(750, 500)))
        print(f"{slug}-thumb.svg")
