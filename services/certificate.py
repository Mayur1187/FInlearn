"""
FinLiteracy – Certificate PDF Generator
Generates a professional completion certificate using ReportLab.
"""

import io
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER


# Landscape A4 dimensions
PAGE_W, PAGE_H = landscape(A4)

# Colour palette (matching FinLiteracy brand)
NAVY    = colors.HexColor('#06111f')
TEAL    = colors.HexColor('#0cbaba')
GREEN   = colors.HexColor('#00c875')
GOLD    = colors.HexColor('#f5c842')
LIGHT   = colors.HexColor('#f0f5ff')
WHITE   = colors.white
MUTED   = colors.HexColor('#4a6785')


def _draw_background(c: canvas.Canvas):
    """Fills the page with the brand background."""
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=True, stroke=False)

    # Decorative corner arcs
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.2)
    c.setFillColor(colors.transparent)
    for cx, cy in [(0, 0), (PAGE_W, 0), (0, PAGE_H), (PAGE_W, PAGE_H)]:
        c.arc(cx - 80, cy - 80, cx + 80, cy + 80, startAng=0, extent=90)

    # Subtle horizontal rules
    c.setStrokeColor(TEAL)
    c.setLineWidth(0.5)
    c.setDash(4, 6)
    for y_pos in [PAGE_H * 0.18, PAGE_H * 0.82]:
        c.line(2 * cm, y_pos, PAGE_W - 2 * cm, y_pos)
    c.setDash()  # reset dash


def _draw_border(c: canvas.Canvas):
    """Draws a decorative double border."""
    pad = 1.1 * cm
    c.setStrokeColor(GOLD)
    c.setLineWidth(2.5)
    c.rect(pad, pad, PAGE_W - 2 * pad, PAGE_H - 2 * pad, fill=False)

    pad2 = pad + 0.35 * cm
    c.setLineWidth(0.8)
    c.setStrokeColor(TEAL)
    c.rect(pad2, pad2, PAGE_W - 2 * pad2, PAGE_H - 2 * pad2, fill=False)


def _center_text(c: canvas.Canvas, text: str, y: float,
                 font: str = 'Helvetica', size: int = 12,
                 color: colors.Color = WHITE):
    c.setFont(font, size)
    c.setFillColor(color)
    c.drawCentredString(PAGE_W / 2, y, text)


def generate_certificate(
    username: str,
    level_title: str,
    level_slug: str,
    quiz_score: int,
    completion_date: datetime = None,
) -> bytes:
    """
    Generates a PDF certificate and returns it as bytes.

    Parameters
    ----------
    username        : display name on the certificate
    level_title     : e.g. "Budgeting Basics"
    level_slug      : used to build certificate ID
    quiz_score      : 0-100 percentage score
    completion_date : defaults to today if not provided
    """
    if completion_date is None:
        completion_date = datetime.utcnow()

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=landscape(A4))
    c.setTitle(f'FinLiteracy Certificate – {level_title}')

    _draw_background(c)
    _draw_border(c)

    mid_x = PAGE_W / 2
    top    = PAGE_H

    # ── Brand header ────────────────────────────────────────────────
    c.setFillColor(GREEN)
    c.setFont('Helvetica-Bold', 13)
    c.drawCentredString(mid_x, top - 2.6 * cm, '₹  F I N L I T E R A C Y')

    c.setFillColor(TEAL)
    c.setFont('Helvetica', 9)
    c.drawCentredString(mid_x, top - 3.2 * cm, 'Financial Literacy for Young India')

    # ── Divider line ─────────────────────────────────────────────────
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(4 * cm, top - 3.7 * cm, PAGE_W - 4 * cm, top - 3.7 * cm)

    # ── Main title ───────────────────────────────────────────────────
    c.setFillColor(GOLD)
    c.setFont('Helvetica-Bold', 32)
    c.drawCentredString(mid_x, top - 5.6 * cm, 'Certificate of Completion')

    # ── Sub-title text ───────────────────────────────────────────────
    c.setFillColor(WHITE)
    c.setFont('Helvetica', 13)
    c.drawCentredString(mid_x, top - 6.8 * cm, 'This is to certify that')

    # ── Name ─────────────────────────────────────────────────────────
    c.setFillColor(GREEN)
    c.setFont('Helvetica-Bold', 36)
    c.drawCentredString(mid_x, top - 8.5 * cm, username)

    # Name underline
    name_w = c.stringWidth(username, 'Helvetica-Bold', 36)
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.5)
    c.line(mid_x - name_w / 2 - 8, top - 8.8 * cm,
           mid_x + name_w / 2 + 8, top - 8.8 * cm)

    # ── Achievement text ──────────────────────────────────────────────
    c.setFillColor(WHITE)
    c.setFont('Helvetica', 13)
    c.drawCentredString(mid_x, top - 10.0 * cm,
                        'has successfully completed the FinLiteracy learning module:')

    # ── Level badge ───────────────────────────────────────────────────
    badge_y = top - 12.2 * cm
    badge_h = 1.6 * cm
    badge_w = 14 * cm
    badge_x = mid_x - badge_w / 2

    c.setFillColor(colors.HexColor('#0d2240'))
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.5)
    c.roundRect(badge_x, badge_y, badge_w, badge_h, 0.4 * cm,
                fill=True, stroke=True)

    c.setFillColor(GOLD)
    c.setFont('Helvetica-Bold', 20)
    c.drawCentredString(mid_x, badge_y + 0.4 * cm, level_title)

    # ── Score badge ───────────────────────────────────────────────────
    c.setFillColor(WHITE)
    c.setFont('Helvetica', 12)
    c.drawCentredString(mid_x, top - 13.6 * cm,
                        f'with a quiz score of  {quiz_score}%')

    # Score bar (small visual)
    bar_x = mid_x - 5 * cm
    bar_y = top - 14.5 * cm
    bar_w = 10 * cm
    bar_h = 0.5 * cm
    c.setFillColor(colors.HexColor('#0d2240'))
    c.setStrokeColor(TEAL)
    c.roundRect(bar_x, bar_y, bar_w, bar_h, 0.15 * cm, fill=True, stroke=True)
    fill_w = bar_w * (quiz_score / 100)
    c.setFillColor(GREEN)
    c.roundRect(bar_x, bar_y, fill_w, bar_h, 0.15 * cm, fill=True, stroke=False)

    # ── Divider ───────────────────────────────────────────────────────
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    c.line(4 * cm, top - 15.4 * cm, PAGE_W - 4 * cm, top - 15.4 * cm)

    # ── Footer row ────────────────────────────────────────────────────
    footer_y = top - 16.5 * cm
    date_str  = completion_date.strftime('%d %B %Y')
    cert_id   = f'FL-{level_slug.upper()[:3]}-{completion_date.strftime("%Y%m%d")}-{abs(hash(username)) % 9999:04d}'

    c.setFillColor(MUTED)
    c.setFont('Helvetica', 9)
    c.drawString(3 * cm, footer_y, f'Certificate ID: {cert_id}')
    c.drawCentredString(mid_x, footer_y, f'Issued on: {date_str}')
    c.drawRightString(PAGE_W - 3 * cm, footer_y, 'finliteracy.app')

    # ── Signature line ────────────────────────────────────────────────
    sig_y = footer_y - 1.1 * cm
    c.setStrokeColor(MUTED)
    c.setLineWidth(0.7)
    c.line(mid_x - 3.5 * cm, sig_y, mid_x + 3.5 * cm, sig_y)
    c.setFillColor(MUTED)
    c.setFont('Helvetica', 8)
    c.drawCentredString(mid_x, sig_y - 0.4 * cm, 'FinLiteracy Platform — Authorised Signature')

    # ── Seal circle ───────────────────────────────────────────────────
    seal_x = PAGE_W - 5.5 * cm
    seal_y = footer_y - 0.5 * cm
    c.setFillColor(colors.HexColor('#0d2240'))
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.circle(seal_x, seal_y, 1.3 * cm, fill=True, stroke=True)
    c.setFillColor(GOLD)
    c.setFont('Helvetica-Bold', 8)
    c.drawCentredString(seal_x, seal_y + 0.2 * cm, 'CERTIFIED')
    c.setFont('Helvetica', 6)
    c.drawCentredString(seal_x, seal_y - 0.3 * cm, 'FINLITERACY')

    c.save()
    return buf.getvalue()
