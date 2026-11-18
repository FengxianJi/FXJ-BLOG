#!/usr/bin/env python3
"""Render aggregate-only blog figures using stdlib SVG and gnuplot.
Run from any directory: python3 scripts/build_feedback_figures.py
No API, source manuscripts, or review text is used.
"""
import json, subprocess
from html import escape
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/evidencepatch-feedback'
OUT.mkdir(parents=True,exist_ok=True)
d=json.loads((OUT/'aggregate_data.json').read_text())
def chart(name,data,body):
 (OUT/(name+'.dat')).write_text(data)
 for terminal,ext in [('svg size 1150,650 font "Arial,19"','svg'),('pngcairo size 1725,975 font "Arial,27"','png'),('pdfcairo size 11.5in,6.5in font "Arial,17"','pdf')]:
  script=f'''set terminal {terminal}
set output '{name}.{ext}'
set encoding utf8
set border 3 lc rgb '#9aa7b3'
set tics nomirror
set grid xtics lc rgb '#e5eaf0'
set key off
set lmargin 25
set rmargin 7
set bmargin 5
set tmargin 4
set style line 1 lc rgb '#246c9c' lw 3
'''+body
  subprocess.run(['gnuplot'],input=script,text=True,cwd=OUT,check=True)
# Score and concern outcomes have different units and denominators: separate figures.
score=d['score_contrasts']
chart('score_effects','\n'.join(f'"{x[0]}" {x[1]} {x[2]} {x[3]} {len(score)-i}' for i,x in enumerate(score))+'\n', '''set title 'Overall AI recommendation: C5 minus C0 (300 papers)'
set xlabel 'Mean score change on the 1-5 scale; paper-bootstrap 95% CI'
set xrange [-1.08:0.15]
set yrange [0.4:4.6]
set ytics ('M3 primary' 4, 'M3 execution rerun' 3, 'Qwen3 (CPU)' 2, 'Mistral (CPU)' 1)
set arrow from 0,graph 0 to 0,graph 1 nohead lc rgb '#777777' dt 2
plot 'score_effects.dat' using 2:5:3:4 with xerrorbars ls 1 pt 7 ps 1.5, '' using ($2+0.025):($5+0.22):(sprintf('%.3f', $2)) with labels left font ',17' textcolor rgb '#172b3a'
''')
chart('discordance','"Score increased" 10 3\n"Score unchanged" 20 2\n"Score decreased" 25 1\n', '''set title '55 papers with an improved concern-resolution proxy'
set xlabel 'Number of papers (284 papers eligible for paired analysis)'
set xrange [0:30]
set yrange [0.4:3.6]
set ytics ('Score increased' 3, 'Score unchanged' 2, 'Score decreased' 1)
set boxwidth 0.55
set style fill solid 0.85 noborder
plot 'discordance.dat' using ($2/2):3:($2/2):(0.28) with boxxyerror lc rgb '#246c9c', '' using ($2+0.5):3:2 with labels left font ',21'
''')
chart('repeatability','"C0 original" 47.7 2\n"C5 evidence appendix" 43.3 1\n', '''set title 'Same frozen version, different M3 executions'
set xlabel 'Papers with exactly matching three-rating mean scores (%)'
set xrange [0:100]
set yrange [0.4:2.6]
set ytics ('C0 original' 2, 'C5 evidence appendix' 1)
set boxwidth 0.55
set style fill solid 0.85 noborder
plot 'repeatability.dat' using ($2/2):3:($2/2):(0.28) with boxxyerror lc rgb '#567d70', '' using ($2+1):3:(sprintf('%.1f%%',$2)) with labels left font ',21'
''')
# Main conceptual figure: explicit method / evidence boundary, with measured endpoints.
svg=['''<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="980" viewBox="0 0 1440 980" role="img" aria-labelledby="title desc">
<title id="title">EvidencePatch: evidence-grounded revision and the evaluation disconnect</title>
<desc id="desc">A proposed concern-to-evidence planning workflow above separate measured concern-resolution and overall-score outcomes. The primary experiment tests frozen-body appendices, not the full planner or multiround efficacy.</desc>
<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#587285"/></marker></defs>
<rect width="1440" height="980" fill="#ffffff"/>
<style>text{font-family:Arial,Helvetica,sans-serif;fill:#163047}.title{font-size:33px;font-weight:700}.h{font-size:24px;font-weight:700}.body{font-size:20px}.small{font-size:18px;fill:#506577}.num{font-size:38px;font-weight:700}.arrow{fill:none;stroke:#587285;stroke-width:3;marker-end:url(#arrow)}</style>''']
def text(x,y,s,cls='body'):svg.append(f'<text x="{x}" y="{y}" class="{cls}">{escape(s)}</text>')
def box(x,y,w,h,color='#f0f5fa',stroke='#cfdae5'):svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{color}" stroke="{stroke}" stroke-width="2"/>')
def arrow(x1,y1,x2,y2):svg.append(f'<path d="M{x1},{y1} L{x2},{y2}" class="arrow"/>')
text(45,55,'EvidencePatch: a revision is more than a higher score','title')
text(45,91,'Method workflow + observed evaluation outcomes; AI judgments remain proxies','body')
box(35,120,1370,290,'#f7fafc')
text(60,158,'A  |  Evidence-grounded, budget-aware revision workflow','h')
labels=[('Paper + reviews',['Frozen input versions','and traceable sources']),('Diagnose + retrieve',['Checkable concerns','and source evidence']),('Plan actions',['Pointers / clarification','experiment / stop']),('Verify patch',['Check provenance','retain unresolved gaps'])]
for i,(title,ls) in enumerate(labels):
 x=65+i*335;box(x,188,300,135)
 text(x+16,224,title,'h')
 for j,s in enumerate(ls):text(x+16,260+j*29,s)
 if i<3:arrow(x+302,253,x+329,253)
text(65,360,'Primary-300 intervention: frozen main text + existing-evidence appendix (C5).','body')
text(65,390,'This panel does not validate the full planner or demonstrate monotonic multiround improvement.','small')
arrow(720,412,720,449)
text(45,478,'B  |  Local concern judgments and overall recommendations diverge','h')
box(45,505,650,205,'#eef6f3','#bbd7ca');box(745,505,650,205,'#f1f4fa','#c6d0e5')
text(65,544,'Concern-resolution proxy','h');text(765,544,'Overall recommendation score','h')
text(65,598,'+0.0559','num');text(765,598,'-0.233 / 5','num')
text(65,638,'284 eligible papers / 873 concern pairs')
text(65,672,'95% CI [+0.0402, +0.0730]','body')
text(765,638,'300 papers / 3 M3 ratings per condition')
text(765,672,'95% CI [-0.281, -0.187]','body')
text(65,697,'Same-family M3 labels; weighted 0 / 0.5 / 1 status','small')
text(765,697,'Frozen-body C5 minus C0 contrast','small')
text(45,754,'55 proxy-improved papers: 10 score up / 20 unchanged / 25 down','h')
text(45,790,'Paired-paper association: Spearman rho = 0.069; 95% CI [-0.056, +0.190]','body')
box(45,820,1350,115,'#f8f6ef','#e1d9bc')
text(65,854,'C  |  Iteration also needs a stability check','h')
text(65,887,'On unchanged packets, exact agreement of three-rating means across two M3 runs:','body')
text(65,919,'C0: 47.7%   |   C5: 43.3%   |   Fixed-concern reassessment + fresh review + repeated scoring','body')
text(45,965,'Different endpoints and eligible populations. Proxy audit has quote constraints; expert resolution is not yet established.','small')
svg.append('</svg>')
(OUT/'main_framework.svg').write_text('\n'.join(svg))
print('Generated main_framework.svg and three charts in SVG / PNG / PDF.')
