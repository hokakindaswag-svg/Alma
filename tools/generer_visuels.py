# -*- coding: utf-8 -*-
"""Génère les visuels placeholders de Studio Alma (SVG).
Chaque fichier est remplaçable tel quel par une vraie photo (mêmes noms, mêmes ratios)."""
import os

OUT = "assets/img"
os.makedirs(OUT, exist_ok=True)

CREME = "#EDE4D8"; CREME2 = "#E4D8C8"; IVOIRE = "#F6F0E8"
CHOCO = "#3A2A20"; TAUPE = "#A08C7A"; CAFE = "#C3AE99"; BORDEAUX = "#5E2130"
CUIRS = {
    "jeanne":   ("#6B4A34", "#573B29"),
    "romy":     ("#8A6B4F", "#6F553E"),
    "louise":   ("#4A3527", "#3A2A20"),
    "victoire": (BORDEAUX, "#471824"),
    "margot":   ("#A98B6C", "#8C7156"),
}

def head(w, h):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" role="img">')

GRAIN = ('<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" '
         'numOctaves="2" result="n"/><feColorMatrix type="saturate" values="0"/>'
         '<feComponentTransfer><feFuncA type="linear" slope="0.05"/></feComponentTransfer>'
         '<feComposite operator="in" in2="SourceGraphic"/></filter>')

def grain_layer(w, h):
    return f'<rect width="{w}" height="{h}" filter="url(#grain)" fill="{CHOCO}" opacity="0.5"/>'

# ---------------------------------------------------------------- sacs
def sac_path(modele, cx, cy, c1, c2):
    """Silhouette propre à chaque modèle, centrée en (cx, cy)."""
    g = []
    if modele == "jeanne":      # sac trapèze à rabat, bandoulière
        g.append(f'<path d="M{cx-150} {cy-90} L{cx+150} {cy-90} L{cx+120} {cy+120} L{cx-120} {cy+120} Z" fill="{c1}"/>')
        g.append(f'<path d="M{cx-150} {cy-90} L{cx+150} {cy-90} L{cx+138} {cy-5} L{cx-138} {cy-5} Z" fill="{c2}"/>')
        g.append(f'<rect x="{cx-16}" y="{cy-22}" width="32" height="34" rx="6" fill="{CAFE}" opacity="0.85"/>')
        g.append(f'<path d="M{cx-120} {cy-92} C {cx-96} {cy-260}, {cx+96} {cy-260}, {cx+120} {cy-92}" '
                 f'fill="none" stroke="{c2}" stroke-width="13" stroke-linecap="round"/>')
    elif modele == "romy":      # baguette, anse courte
        g.append(f'<rect x="{cx-165}" y="{cy-52}" width="330" height="150" rx="34" fill="{c1}"/>')
        g.append(f'<rect x="{cx-165}" y="{cy-52}" width="330" height="30" rx="15" fill="{c2}"/>')
        g.append(f'<path d="M{cx-110} {cy-54} C {cx-100} {cy-140}, {cx+100} {cy-140}, {cx+110} {cy-54}" '
                 f'fill="none" stroke="{c2}" stroke-width="16" stroke-linecap="round"/>')
        g.append(f'<circle cx="{cx+108}" cy="{cy+26}" r="11" fill="{CAFE}" opacity="0.8"/>')
    elif modele == "louise":    # cabas, deux anses
        g.append(f'<path d="M{cx-140} {cy-70} L{cx+140} {cy-70} L{cx+126} {cy+140} L{cx-126} {cy+140} Z" fill="{c1}"/>')
        g.append(f'<rect x="{cx-140}" y="{cy-70}" width="280" height="14" fill="{c2}"/>')
        for dx in (-70, 70):
            g.append(f'<path d="M{cx+dx-42} {cy-72} C {cx+dx-38} {cy-176}, {cx+dx+38} {cy-176}, {cx+dx+42} {cy-72}" '
                     f'fill="none" stroke="{c2}" stroke-width="13" stroke-linecap="round"/>')
    elif modele == "victoire":  # croissant / hobo
        g.append(f'<path d="M{cx-160} {cy-54} C {cx-120} {cy+130}, {cx+120} {cy+130}, {cx+160} {cy-54} '
                 f'C {cx+90} {cy-18}, {cx-90} {cy-18}, {cx-160} {cy-54} Z" fill="{c1}"/>')
        g.append(f'<path d="M{cx-160} {cy-54} C {cx-90} {cy-18}, {cx+90} {cy-18}, {cx+160} {cy-54} '
                 f'C {cx+120} {cy-70}, {cx-120} {cy-70}, {cx-160} {cy-54} Z" fill="{c2}"/>')
        g.append(f'<path d="M{cx-128} {cy-62} C {cx-70} {cy-170}, {cx+70} {cy-170}, {cx+128} {cy-62}" '
                 f'fill="none" stroke="{c2}" stroke-width="12" stroke-linecap="round"/>')
    else:                        # margot : petit carré, longue bandoulière
        g.append(f'<rect x="{cx-100}" y="{cy-40}" width="200" height="168" rx="12" fill="{c1}"/>')
        g.append(f'<path d="M{cx-100} {cy-40} L{cx+100} {cy-40} L{cx+100} {cy+22} L{cx-100} {cy+22} Z" fill="{c2}"/>')
        g.append(f'<rect x="{cx-13}" y="{cy+6}" width="26" height="30" rx="5" fill="{CAFE}" opacity="0.85"/>')
        g.append(f'<path d="M{cx-92} {cy-42} L{cx-58} {cy-250} M{cx+92} {cy-42} L{cx+58} {cy-250}" '
                 f'fill="none" stroke="{c2}" stroke-width="9" stroke-linecap="round"/>')
    return "".join(g)

def produit(modele, index):
    w, h = 900, 1125
    c1, c2 = CUIRS[modele]
    fond = IVOIRE if index == 1 else CREME2
    s = [head(w, h), f'<defs>{GRAIN}</defs>', f'<rect width="{w}" height="{h}" fill="{fond}"/>']
    if index == 1:
        # fond studio : socle discret
        s.append(f'<ellipse cx="{w//2}" cy="{int(h*0.775)}" rx="250" ry="24" fill="{CHOCO}" opacity="0.09"/>')
        s.append(f'<g transform="translate({w//2} {int(h*0.52)}) scale(1.34) translate(-{w//2} -{int(h*0.5)})">')
        s.append(sac_path(modele, w//2, int(h*0.5), c1, c2))
        s.append('</g>')
    else:
        # vue détail : gros plan matière, sac décalé
        s.append(f'<circle cx="{int(w*0.72)}" cy="{int(h*0.24)}" r="270" fill="{CHOCO}" opacity="0.05"/>')
        s.append(f'<g transform="translate({int(w*0.5)} {int(h*0.56)}) scale(1.7) translate(-{w//2} -{int(h*0.5)})">')
        s.append(sac_path(modele, w//2, int(h*0.5), c1, c2))
        s.append('</g>')
    s.append(grain_layer(w, h))
    s.append('</svg>')
    open(f"{OUT}/{modele}-{index}.svg", "w").write("".join(s))

for m in CUIRS:
    produit(m, 1); produit(m, 2)

# ---------------------------------------------------------------- éditoriales
def scene(nom, w, h, teinte, variante):
    """Scène éditoriale stylisée : façade parisienne, lumière douce, silhouette au sac."""
    s = [head(w, h), f'<defs>{GRAIN}</defs>', f'<rect width="{w}" height="{h}" fill="{teinte}"/>']
    sol = int(h * 0.865)

    # --- façade : immeuble haussmannien suggéré, fenêtres hautes
    for i in range(9):
        x = int(w * 0.02) + i * int(w * 0.112)
        s.append(f'<rect x="{x}" y="{int(h*0.045)}" width="{int(w*0.062)}" height="{int(h*0.27)}" '
                 f'rx="{int(w*0.031)}" fill="{CHOCO}" opacity="0.055"/>')
        s.append(f'<rect x="{x-4}" y="{int(h*0.315)}" width="{int(w*0.062)+8}" height="3" fill="{CHOCO}" opacity="0.07"/>')
    s.append(f'<rect x="0" y="{int(h*0.36)}" width="{w}" height="2" fill="{CHOCO}" opacity="0.07"/>')
    # store de café
    s.append(f'<path d="M{int(w*0.60)} {int(h*0.40)} L{int(w*0.96)} {int(h*0.40)} '
             f'L{int(w*0.94)} {int(h*0.50)} L{int(w*0.62)} {int(h*0.50)} Z" fill="{BORDEAUX}" opacity="0.30"/>')
    # sol / trottoir
    s.append(f'<rect x="0" y="{sol}" width="{w}" height="{h-sol}" fill="{CHOCO}" opacity="0.08"/>')
    s.append(f'<rect x="0" y="{sol}" width="{w}" height="2" fill="{CHOCO}" opacity="0.10"/>')

    # --- silhouette
    cx = int(w * (0.60 if variante == "hero" else 0.76))
    u = h / 100.0                      # unité de proportion
    tete_y = int(h * 0.255)
    epaule = int(h * 0.345)
    ourlet = int(h * 0.645)            # bas du manteau
    manteau, cheveux, peau = "#5C4638", "#3A2A20", "#C3AE99"

    # jambes + bottes
    for dx in (-int(4.2*u), int(3.2*u)):
        s.append(f'<rect x="{cx+dx-int(1.6*u)}" y="{ourlet-int(2*u)}" width="{int(3.2*u)}" '
                 f'height="{sol-ourlet+int(2*u)}" rx="{int(1.4*u)}" fill="{CAFE}" opacity="0.75"/>')
        s.append(f'<rect x="{cx+dx-int(1.8*u)}" y="{sol-int(9*u)}" width="{int(3.6*u)}" '
                 f'height="{int(9*u)}" rx="{int(1.2*u)}" fill="{CHOCO}"/>')
    # ombre portée
    s.append(f'<ellipse cx="{cx}" cy="{sol+int(0.8*u)}" rx="{int(11*u)}" ry="{int(1.4*u)}" fill="{CHOCO}" opacity="0.12"/>')

    # manteau ouvert, légèrement évasé
    s.append(f'<path d="M{cx-int(7.4*u)} {epaule} '
             f'C {cx-int(8.6*u)} {int(h*0.45)}, {cx-int(9.6*u)} {int(h*0.57)}, {cx-int(10.4*u)} {ourlet} '
             f'L{cx+int(10.4*u)} {ourlet} '
             f'C {cx+int(9.6*u)} {int(h*0.57)}, {cx+int(8.6*u)} {int(h*0.45)}, {cx+int(7.4*u)} {epaule} '
             f'C {cx+int(4*u)} {epaule-int(2.4*u)}, {cx-int(4*u)} {epaule-int(2.4*u)}, {cx-int(7.4*u)} {epaule} Z" fill="{manteau}"/>')
    # revers / ouverture centrale plus sombre
    s.append(f'<path d="M{cx-int(2.6*u)} {epaule-int(1.4*u)} L{cx+int(2.6*u)} {epaule-int(1.4*u)} '
             f'L{cx+int(1.8*u)} {ourlet} L{cx-int(1.8*u)} {ourlet} Z" fill="{CHOCO}" opacity="0.35"/>')
    # ceinture
    s.append(f'<rect x="{cx-int(8.6*u)}" y="{int(h*0.475)}" width="{int(17.2*u)}" height="{int(1.5*u)}" fill="{CHOCO}" opacity="0.45"/>')

    # cou, tête, cheveux
    s.append(f'<rect x="{cx-int(1.5*u)}" y="{tete_y+int(3*u)}" width="{int(3*u)}" height="{int(4*u)}" fill="{peau}"/>')
    s.append(f'<circle cx="{cx}" cy="{tete_y}" r="{int(4.2*u)}" fill="{peau}"/>')
    s.append(f'<path d="M{cx-int(4.6*u)} {tete_y+int(1*u)} '
             f'C {cx-int(5.2*u)} {tete_y-int(6*u)}, {cx+int(5.2*u)} {tete_y-int(6*u)}, {cx+int(4.6*u)} {tete_y+int(1*u)} '
             f'C {cx+int(5.4*u)} {tete_y+int(7*u)}, {cx+int(3.4*u)} {tete_y+int(8*u)}, {cx+int(3.2*u)} {tete_y+int(4*u)} '
             f'L{cx-int(3.2*u)} {tete_y+int(4*u)} '
             f'C {cx-int(3.4*u)} {tete_y+int(8*u)}, {cx-int(5.4*u)} {tete_y+int(7*u)}, {cx-int(4.6*u)} {tete_y+int(1*u)} Z" fill="{cheveux}"/>')

    # bras côté sac
    bras_x = cx + int(7.2*u)
    s.append(f'<path d="M{cx+int(6.4*u)} {epaule+int(0.5*u)} C {bras_x+int(1.6*u)} {int(h*0.44)}, '
             f'{bras_x+int(1.2*u)} {int(h*0.50)}, {bras_x-int(0.2*u)} {int(h*0.545)}" '
             f'fill="none" stroke="{manteau}" stroke-width="{int(3.4*u)}" stroke-linecap="round"/>')

    # --- le sac, porté au creux du bras
    sx, sy = cx + int(10.6*u), int(h*0.575)
    bw, bh = int(7.4*u), int(6.2*u)
    s.append(f'<path d="M{sx-int(5.6*u)} {int(h*0.44)} C {sx-int(3.2*u)} {int(h*0.50)}, '
             f'{sx-int(0.6*u)} {int(h*0.50)}, {sx} {sy-bh}" fill="none" stroke="#471824" '
             f'stroke-width="{max(3,int(0.9*u))}" stroke-linecap="round"/>')
    s.append(f'<path d="M{sx-bw} {sy-bh} L{sx+bw} {sy-bh} L{sx+int(bw*0.84)} {sy+bh} '
             f'L{sx-int(bw*0.84)} {sy+bh} Z" fill="{BORDEAUX}"/>')
    s.append(f'<path d="M{sx-bw} {sy-bh} L{sx+bw} {sy-bh} L{sx+int(bw*0.94)} {sy-int(bh*0.15)} '
             f'L{sx-int(bw*0.94)} {sy-int(bh*0.15)} Z" fill="#471824"/>')

    # lumière rasante
    s.append(f'<circle cx="{int(w*0.86)}" cy="{int(h*0.16)}" r="{int(h*0.20)}" fill="#FBF7F1" opacity="0.26"/>')
    s.append(f'<circle cx="{int(w*0.88)}" cy="{int(h*0.14)}" r="{int(h*0.09)}" fill="#FBF7F1" opacity="0.22"/>')
    s.append(grain_layer(w, h))
    s.append('</svg>')
    open(f"{OUT}/{nom}.svg", "w").write("".join(s))

# Les scènes lifestyle sont désormais de vraies photos (hero.jpg, editorial.jpg).
# La fonction scene() reste disponible pour regénérer un placeholder si besoin :
#   scene("hero", 1800, 1000, CREME2, "hero")
print("SVG générés :", len(os.listdir(OUT)))
