# -*- coding: utf-8 -*-
"""Normalise les packshots produits au format 4/5 de la grille.

Les photos sources ont des cadrages et des ratios différents. Plutôt que de
recadrer (ce qui couperait les sacs), on centre la photo sur un canevas 4/5 et
on prolonge le fond par réplication des bords : la jointure est invisible sur
un fond uni. Usage : python3 tools/preparer_photos.py <dossier_source>
"""
import sys, os, re
from PIL import Image, ImageDraw, ImageFilter

CIBLE_W, CIBLE_H = 1000, 1250   # 4/5
MARGE = 0.93                    # part de la hauteur/largeur occupée par la photo
FONDU = 26                      # adoucissement des bords de la photo, en pixels

MODELES = ["jeanne", "romy", "louise", "victoire", "margot", "clemence",
           "elise", "camille", "adele", "chloe", "madeleine"]


def couleur_fond(im):
    """Couleur dominante des bords de la photo : son fond de studio."""
    w, h = im.size
    bord = [im.getpixel((x, 0)) for x in range(0, w, 8)]
    bord += [im.getpixel((x, h - 1)) for x in range(0, w, 8)]
    bord += [im.getpixel((0, y)) for y in range(0, h, 8)]
    bord += [im.getpixel((w - 1, y)) for y in range(0, h, 8)]
    bord.sort(key=lambda c: sum(c))
    return bord[len(bord) // 2]


def normaliser(src, dest):
    im = Image.open(src).convert("RGB")
    w, h = im.size
    ech = min(CIBLE_W * MARGE / w, CIBLE_H * MARGE / h)
    im = im.resize((max(1, int(w * ech)), max(1, int(h * ech))), Image.LANCZOS)
    gauche = (CIBLE_W - im.width) // 2
    haut = (CIBLE_H - im.height) // 2
    canevas = Image.new("RGB", (CIBLE_W, CIBLE_H), couleur_fond(im))
    # masque adouci sur les bords : la photo se fond dans le fond uni,
    # sans liseré ni bande, même si son propre fond est légèrement dégradé
    masque = Image.new("L", im.size, 255)
    ImageDraw.Draw(masque).rectangle([0, 0, im.width - 1, im.height - 1], outline=0, width=2)
    masque = masque.filter(ImageFilter.GaussianBlur(FONDU))
    canevas.paste(im, (gauche, haut), masque)
    canevas.save(dest, "JPEG", quality=86, optimize=True, progressive=True)
    return canevas.size


if __name__ == "__main__":
    source = sys.argv[1] if len(sys.argv) > 1 else "photos"
    fichiers = sorted(
        (f for f in os.listdir(source) if f.lower().endswith((".jpg", ".jpeg", ".png"))),
        key=lambda f: int(re.search(r"(\d+)", f).group(1)))
    for modele, fichier in zip(MODELES, fichiers):
        dest = f"assets/img/{modele}-1.jpg"
        print(fichier, "->", dest, normaliser(os.path.join(source, fichier), dest))
