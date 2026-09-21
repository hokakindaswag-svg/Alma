# Studio Alma

Site e-commerce statique d'une marque française de city bags.
Cinq modèles — Jeanne, Romy, Louise, Victoire, Margot — tous à 19,99 €.
Livraison offerte sur toutes les commandes.

## Lancer le site

Aucune dépendance, aucun build nécessaire :

```bash
python3 -m http.server 8000
# puis http://localhost:8000
```

## Structure

```
index.html            accueil (hero, collection, éditorial, prix unique)
sacs.html             catalogue des cinq modèles
produit/<modele>.html page produit (galerie, accordéons, ajout au panier)
panier.html           panier (localStorage)
a-propos.html, livraison.html, faq.html, contact.html, compte.html
assets/css/style.css  feuille de style unique
assets/js/produits.js catalogue (source unique : noms, prix, textes, images)
assets/js/main.js     panier, menu mobile, galerie, accordéons, apparitions
assets/img/           visuels placeholders (SVG)
tools/build.py        régénère les pages HTML depuis le gabarit commun
```

## Visuels

Le hero et la section éditoriale utilisent de vraies photos
(`assets/img/hero.jpg`, `hero-mobile.jpg`, `editorial.jpg`, `editorial-mobile.jpg`).
Les photos produits sont encore des placeholders SVG, pensés pour être
remplacés tels quels.

1. Déposez vos photos dans `assets/img/` (ratio 4/5 pour les produits,
   16/8.5 pour le hero, 16/7.5 pour les bandeaux éditoriaux).
2. Mettez à jour le tableau `images` du modèle concerné dans
   `assets/js/produits.js` (ex. `["assets/img/jeanne-1.jpg", "assets/img/jeanne-2.jpg"]`).
3. Relancez `python3 tools/build.py` pour régénérer les pages.

Direction photo : Paris, cafés, rues pavées, métro, appartements, lumière
naturelle. Palette crème, chocolat, taupe, noir doux, bordeaux.

## Modifier le contenu

- Textes produits, dimensions, matières : `assets/js/produits.js`
- Structure des pages, header, footer : `tools/build.py`, puis relancer le script
- Couleurs et typographie : variables `:root` dans `assets/css/style.css`
