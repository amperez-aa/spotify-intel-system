from fpdf import FPDF
import json, os, textwrap

pdf = FPDF(orientation='P', unit='mm', format='A4')

def add_title(pdf, t):
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, t, ln=True)

def add_paragraph(pdf, text, size=11):
    pdf.set_font('Arial', '', size)
    for line in textwrap.wrap(text, width=100):
        pdf.cell(0, 6, line, ln=True)

pdf.add_page()
add_title(pdf, 'Mix Blueprint — Generated')
if os.path.exists('output/ai_mix_timeline.json'):
    with open('output/ai_mix_timeline.json') as f:
        timeline = json.load(f)
    add_paragraph(pdf, f'Total tracks: {len(timeline)}')
    pdf.ln(2)
    for i, t in enumerate(timeline[:200]):
        add_paragraph(pdf, f"{i+1}. {t.get('name')} — {', '.join(t.get('artists',[]))} | start_time: {t.get('start_time_s')}s | offset: {t.get('start_offset_s')}s")
else:
    add_paragraph(pdf, 'Timeline missing. Run ai_mix_timeline.py first.')

os.makedirs('output', exist_ok=True)
pdf.output('output/mix_blueprint.pdf')
print('Saved output/mix_blueprint.pdf')
