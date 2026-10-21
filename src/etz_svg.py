def bottle(x, base, h=70, w=14, c='var(--wine-mid)'):
    neck=h*0.32; body=h-neck
    return (f'<path d="M{x-w/2} {base} V{base-body+6} Q{x-w/2} {base-body} {x-w/4} {base-body-4} V{base-h+4} H{x+w/4} V{base-body-4} Q{x+w/2} {base-body} {x+w/2} {base-body+6} V{base} Z" fill="{c}"/>'
            f'<rect x="{x-w/4-1}" y="{base-h}" width="{w/2+2}" height="7" rx="1.5" fill="var(--steel)"/>')
def etz_svg(cls='etz-svg'):
    o=[]; A=o.append
    A(f'<svg class="{cls}" viewBox="0 0 400 660" role="img" aria-label="Схема этажерки: три яруса с бутылками на вращающейся колонне поднимаются из пола">')
    A('<defs><linearGradient id="etzGlow" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="var(--amber)" stop-opacity=".0"/><stop offset="1" stop-color="var(--amber)" stop-opacity=".55"/></linearGradient>'
      '<radialGradient id="etzPool" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="var(--amber)" stop-opacity=".35"/><stop offset="1" stop-color="var(--amber)" stop-opacity="0"/></radialGradient>'
      '<clipPath id="etzAbove"><rect x="0" y="0" width="400" height="520"/></clipPath>'
      '<pattern id="etzFloor" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><path d="M0 0 V10" stroke="var(--line-strong)" stroke-width="1"/></pattern></defs>')
    # pit below floor
    A('<rect x="120" y="522" width="160" height="128" fill="none" stroke="var(--line-strong)" stroke-dasharray="4 5"/>')
    A('<rect x="20" y="520" width="100" height="18" fill="url(#etzFloor)"/><rect x="280" y="520" width="100" height="18" fill="url(#etzFloor)"/>')
    A('<path d="M20 520 H120 M280 520 H380" stroke="var(--bone)" stroke-width="1.2"/>')
    A('<ellipse cx="200" cy="520" rx="120" ry="12" fill="url(#etzPool)"/>')
    # rising unit
    A('<g clip-path="url(#etzAbove)"><g class="etz-rise">')
    top=150; bot=520
    for x in (128,200,272):
        A(f'<rect x="{x-2}" y="{top}" width="4" height="{bot-top}" fill="var(--steel)" opacity=".85"/>')
    levels=[250,365,480]
    for i,y in enumerate(levels):
        A(f'<rect x="124" y="{y-92}" width="152" height="92" fill="url(#etzGlow)"/>')
        xs=[146,168,190,212,234,256] if i<2 else [158,184,210,236]
        for k,x in enumerate(xs):
            A(bottle(x,y-2,h=78 if i<2 else 84,w=15,c='var(--wine-mid)' if k%3 else 'var(--oak-dark)'))
        A(f'<ellipse cx="200" cy="{y}" rx="78" ry="9" fill="var(--slab)" stroke="var(--steel)" stroke-width="1.4"/>')
    A(f'<ellipse cx="200" cy="{top}" rx="96" ry="13" fill="var(--block)" stroke="var(--bone)" stroke-width="1.4"/>')
    A(f'<path d="M104 {top} v8 a96 13 0 0 0 192 0 v-8" fill="var(--block)" stroke="var(--bone)" stroke-width="1.2"/>')
    A('</g></g>')
    # annotations
    A('<g class="etz-ann"><path d="M104 112 H296" stroke="var(--ash)" stroke-width="1" marker-start="url(#arr)" marker-end="url(#arr)"/>'
      '<text x="200" y="100" text-anchor="middle" class="t-n">Ø 250 или 400 мм</text>'
      '<path d="M330 158 V512" stroke="var(--ash)" stroke-width="1" stroke-dasharray="2 4"/>'
      '<text x="340" y="215" class="t-s">ярус 1</text><text x="340" y="330" class="t-s">ярус 2</text><text x="340" y="445" class="t-s">ярус 3</text>'
      '<text x="30" y="512" class="t-s">уровень пола</text><text x="200" y="640" text-anchor="middle" class="t-s">механизм в полу</text></g>')
    A('<defs><marker id="arr" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="var(--ash)"/></marker></defs>')
    A('</svg>')
    return ''.join(o)
