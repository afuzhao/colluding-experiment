"""Render paired estimates and intervals as a self-contained SVG figure."""
import html
import json

from behavioral import ROOT


if __name__ == '__main__':
    data = json.loads((ROOT / 'behavioral_analysis/analysis.json').read_text())
    entries = [(model, effect) for model, result in data.items() for effect in result['primary'] if effect['n']]
    width, height = 1150, 140 + 75 * len(entries)
    left, right = 490, 1000
    position = lambda value: left + (value + 600) / 1200 * (right - left)
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
           '<rect width="100%" height="100%" fill="white"/>',
           '<g font-family="Arial, sans-serif" fill="#17212b">',
           '<text x="24" y="32" font-size="22">Matched effects on consumer-surplus loss</text>',
           '<text x="24" y="56" font-size="13">Positive = greater consumer harm; intervals resample paired seeds. Short simulated markets.</text>',
           f'<line x1="{position(0)}" x2="{position(0)}" y1="75" y2="{height-55}" stroke="#9aa4af" stroke-dasharray="4 4"/>']
    for index, (model, effect) in enumerate(entries):
        y = 100 + index * 75
        label = html.escape(effect['label'])
        svg += [f'<text x="24" y="{y}" font-size="14">{label}</text>',
                f'<text x="24" y="{y+20}" font-size="12" fill="#657280">{html.escape(model)} · n={effect["n"]}</text>']
        lo, hi = effect['ci95']
        x = position(effect['mean'])
        svg += [f'<line x1="{position(lo)}" x2="{position(hi)}" y1="{y}" y2="{y}" stroke="#245a88" stroke-width="3"/>',
                f'<circle cx="{x}" cy="{y}" r="5" fill="#245a88"/>',
                f'<text x="1020" y="{y+4}" font-size="13">{effect["mean"]:+.1f}</text>']
    for value in (-600, -300, 0, 300, 600):
        svg.append(f'<text x="{position(value)}" y="{height-30}" font-size="12" text-anchor="middle">{value}</text>')
    svg += [f'<text x="{(left+right)/2}" y="{height-10}" font-size="12" text-anchor="middle">Change in surplus loss (points per round)</text>', '</g></svg>']
    destination = ROOT / 'behavioral_analysis/paired_effects.svg'
    destination.write_text('\n'.join(svg))
    print(destination)
