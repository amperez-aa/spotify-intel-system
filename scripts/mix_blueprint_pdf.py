import os, json, textwrap

def sanitize(text):
    if not isinstance(text, str):
        text = str(text)
    replacements = {
        '\u2014': '-', '\u2013': '-', '\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"',
        '\u2026': '...'
    }
    for k,v in replacements.items():
        text = text.replace(k, v)
    # Replace remaining non-latin1 characters with '?'
    return ''.join([c if ord(c) < 256 else '?' for c in text])

try:
    from fpdf import FPDF
    have_fpdf = True
except Exception:
    have_fpdf = False

timeline = []
if os.path.exists('output/ai_mix_timeline.json'):
    with open('output/ai_mix_timeline.json','r',encoding='utf-8') as f:
        timeline = json.load(f)

out_path = 'output/mix_blueprint.pdf'
if have_fpdf:
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    font_path = 'fonts/DejaVuSans.ttf'
    try:
        if os.path.exists(font_path):
            pdf.add_font('DejaVu', '', font_path, uni=True)
            pdf.set_font('DejaVu', size=12)
        else:
            pdf.set_font('Arial', size=12)
    except Exception:
        pdf.set_font('Arial', size=12)
    pdf.cell(0, 10, 'Mix Blueprint — Generated', ln=True)
    pdf.ln(4)
    pdf.cell(0, 6, f'Total tracks: {len(timeline)}', ln=True)
    pdf.ln(2)
    for i, t in enumerate(timeline[:200]):
        line = f"{i+1}. {t.get('name')} — {', '.join(t.get('artists',[]))} | start_time: {t.get('start_time_s')}s | offset: {t.get('start_offset_s')}s"
        pdf.multi_cell(0, 6, sanitize(line))
    os.makedirs('output', exist_ok=True)
    pdf.output(out_path)
    print('Saved', out_path)
else:
    os.makedirs('output', exist_ok=True)
    with open('output/mix_blueprint.txt','w',encoding='utf-8') as f:
        f.write('Mix Blueprint (plain text fallback)\\n')
        f.write('Total tracks: ' + str(len(timeline)) + '\\n\\n')
        for i, t in enumerate(timeline[:200]):
            line = f"{i+1}. {t.get('name')} - {', '.join(t.get('artists',[]))} | start_time: {t.get('start_time_s')}s | offset: {t.get('start_offset_s')}s"
            f.write(sanitize(line) + '\\n')
    print('FPDF not installed; wrote output/mix_blueprint.txt instead')
