# -*- coding: utf-8 -*-
"""Génère les pages HTML de Studio Alma à partir d'un gabarit commun.
   python3 tools/build.py  —  à relancer après modification d'un gabarit."""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRIX = "19,99 €"

# --- catalogue : lu depuis assets/js/produits.js pour n'avoir qu'une source ---
def catalogue():
    src = open(os.path.join(ROOT, "assets/js/produits.js"), encoding="utf-8").read()
    bloc = src.split("window.ALMA_PRODUITS =", 1)[1].rsplit("];", 1)[0] + "]"
    bloc = re.sub(r"(\w+):", r'"\1":', bloc)          # clés -> JSON
    bloc = re.sub(r",(\s*[\]}])", r"\1", bloc)
    return json.loads(bloc)

PRODUITS = catalogue()

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500&'
         'family=Jost:wght@300;400;500&display=swap" rel="stylesheet">')

def header(base, actif):
    def lien(href, texte, cle):
        cur = ' aria-current="page"' if cle == actif else ""
        return f'<a href="{base}{href}"{cur}>{texte}</a>'
    return f"""  <p class="bandeau">Livraison offerte sur toutes les commandes<span class="bandeau__suite"> · Retours sous 30 jours</span></p>
  <header class="header">
    <div class="wrap header__inner">
      <button class="burger" type="button" data-ouvrir-menu aria-label="Ouvrir le menu">
        <span></span><span></span><span></span>
      </button>
      <nav class="nav" aria-label="Navigation principale">
        {lien('sacs.html#nouveautes', 'Nouveautés', 'nouveautes')}
        {lien('sacs.html', 'Les sacs', 'sacs')}
        {lien('a-propos.html', 'À propos', 'apropos')}
      </nav>
      <a class="logo" href="{base}index.html">Studio Alma</a>
      <div class="outils">
        <a href="{base}sacs.html" aria-label="Recherche"><span class="outils__texte">Recherche</span>
          <svg class="outils__icone" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M16.5 16.5 21 21"/></svg></a>
        <a href="{base}compte.html" aria-label="Compte"><span class="outils__texte">Compte</span>
          <svg class="outils__icone" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true"><circle cx="12" cy="8.5" r="4"/><path d="M4.5 20.5c1.6-4 4.3-6 7.5-6s5.9 2 7.5 6"/></svg></a>
        <a href="{base}panier.html" aria-label="Panier"><span class="outils__texte">Panier&nbsp;</span>
          <svg class="outils__icone" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true"><path d="M4 7.5h16l-1.2 12.5H5.2L4 7.5Z"/><path d="M8.6 10V6.6a3.4 3.4 0 0 1 6.8 0V10"/></svg>
          <span data-compteur class="compteur-panier">(0)</span></a>
      </div>
    </div>
  </header>

  <div class="menu-mobile" id="menu-mobile">
    <div class="wrap menu-mobile__haut" style="padding:0">
      <span class="logo">Studio Alma</span>
      <button class="fermer" type="button" data-fermer-menu>Fermer</button>
    </div>
    <nav class="menu-mobile__liens" aria-label="Navigation mobile">
      <a href="{base}sacs.html#nouveautes">Nouveautés</a>
      <a href="{base}sacs.html">Les sacs</a>
      <a href="{base}a-propos.html">À propos</a>
      <a href="{base}panier.html">Panier</a>
    </nav>
    <div class="menu-mobile__bas">
      <span>Tous les sacs · {PRIX} · Livraison offerte</span>
      <span>Instagram · TikTok</span>
    </div>
  </div>"""

def footer(base):
    return f"""  <footer class="footer">
    <div class="wrap">
      <div class="footer__grille">
        <div>
          <p class="footer__logo">Studio Alma</p>
          <p class="footer__mot">Cinq city bags féminins, pensés pour la ville et faciles à porter, du matin au soir.</p>
        </div>
        <div>
          <h3>Boutique</h3>
          <ul>
            <li><a href="{base}sacs.html">Boutique</a></li>
            <li><a href="{base}a-propos.html">À propos</a></li>
            <li><a href="{base}livraison.html">Livraison &amp; retours</a></li>
            <li><a href="{base}faq.html">FAQ</a></li>
            <li><a href="{base}contact.html">Contact</a></li>
          </ul>
        </div>
        <div>
          <h3>Nous suivre</h3>
          <ul>
            <li><a href="https://instagram.com" rel="noopener">Instagram</a></li>
            <li><a href="https://tiktok.com" rel="noopener">TikTok</a></li>
          </ul>
        </div>
      </div>
      <div class="footer__bas">
        <span>© 2026 Studio Alma</span>
        <span>Tous les sacs · {PRIX}</span>
      </div>
    </div>
  </footer>"""

def page(nom, titre, description, corps, base="", actif="", scripts=""):
    html = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{titre}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#F6F0E8">
<meta property="og:title" content="{titre}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
{FONTS}
<link rel="stylesheet" href="{base}assets/css/style.css">
</head>
<body class="no-js" data-base="{base}">
{header(base, actif)}

<main id="contenu">
{corps}
</main>

{footer(base)}

<script src="{base}assets/js/produits.js"></script>
<script src="{base}assets/js/main.js"></script>{scripts}
</body>
</html>
"""
    chemin = os.path.join(ROOT, nom)
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    open(chemin, "w", encoding="utf-8").write(html)

# ------------------------------------------------------------------ fragments
def carte(p, base="", eager=False):
    charge = "eager" if eager else "lazy"
    return f"""        <a class="carte apparait" href="{base}produit/{p['id']}.html">
          <div class="carte__media">
            <img src="{base}{p['images'][0]}" alt="{p['nom']} — city bag Studio Alma" loading="{charge}" width="900" height="1125">
            <img src="{base}{p['images'][1]}" alt="" aria-hidden="true" loading="lazy" width="900" height="1125">
          </div>
          <div class="carte__infos">
            <p class="carte__nom">{p['nom']}</p>
            <p class="carte__meta">{p['type']}</p>
            <p class="carte__prix">{PRIX}</p>
          </div>
        </a>"""

def grille(base=""):
    return "\n".join(carte(p, base, eager=(i < 2)) for i, p in enumerate(PRODUITS))

# ---------------------------------------------------------------- index.html
accueil = f"""  <section class="hero">
    <div class="hero__media">
      <picture>
        <source media="(max-width: 759px)" srcset="assets/img/hero-mobile.jpg">
        <img src="assets/img/hero.jpg" alt="Jeune femme dans la rue avec son city bag Studio Alma et un café" width="1200" height="637" fetchpriority="high">
      </picture>
      <div class="hero__voile"></div>
    </div>
    <div class="hero__contenu">
      <h1 class="hero__titre">Les sacs<br>de la ville.</h1>
      <p class="hero__texte">Des city bags féminins pensés pour accompagner vos journées, du matin au soir.</p>
      <a class="btn btn--clair" href="sacs.html">Découvrir les sacs</a>
    </div>
  </section>

  <section class="section" id="collection">
    <div class="wrap">
      <div class="section__tete apparait">
        <p class="eyebrow">Automne 2026</p>
        <h2 class="titre-section">La collection</h2>
        <p class="soustitre">Cinq silhouettes. Une seule obsession : le quotidien.</p>
      </div>
      <div class="grille-produits">
{grille()}
      </div>
      <p style="text-align:center;margin-top:48px"><a class="lien-souligne" href="sacs.html">Voir les cinq modèles</a></p>
    </div>
  </section>

  <section class="editorial">
    <div class="editorial__media">
      <picture>
        <source media="(max-width: 759px)" srcset="assets/img/editorial-mobile.jpg">
        <img src="assets/img/editorial.jpg" alt="City bag Studio Alma posé sur une table de café, avec un café et une viennoiserie" loading="lazy" width="1200" height="562">
      </picture>
    </div>
    <div class="editorial__voile"></div>
    <div class="editorial__contenu apparait">
      <h2 class="editorial__titre">Pensés pour la ville.</h2>
      <p class="editorial__texte">Du café du matin au dernier verre du soir, Studio Alma imagine des sacs faciles à vivre et simples à aimer.</p>
      <a class="btn btn--clair" href="sacs.html">Découvrir la collection</a>
    </div>
  </section>

  <section class="section section--serre prix-unique">
    <div class="wrap apparait">
      <h2>Tous les sacs · {PRIX}</h2>
      <p>Parce que le style ne devrait pas être compliqué.</p>
    </div>
  </section>

  <section class="section">
    <div class="wrap trio apparait">
      <div><h3>Livraison offerte</h3><p>Sur toutes les commandes, sans minimum.</p></div>
      <div><h3>Paiement sécurisé</h3><p>Carte, Apple Pay, PayPal.</p></div>
      <div><h3>Retours faciles</h3><p>30 jours pour changer d'avis.</p></div>
    </div>
  </section>"""

page("index.html", "Studio Alma — City bags féminins pensés pour la ville",
     f"Cinq city bags féminins à {PRIX}, pensés pour la ville et faciles à porter du matin au soir.",
     accueil, actif="accueil")

# ----------------------------------------------------------------- sacs.html
sacs = f"""  <section class="page-tete apparait" id="nouveautes">
    <div class="wrap">
      <p class="eyebrow">La collection · Automne 2026</p>
      <h1 class="titre-section">Les sacs</h1>
      <p class="soustitre">Cinq city bags, cinq personnalités.</p>
    </div>
  </section>

  <section class="section" style="padding-top:0">
    <div class="wrap">
      <div class="grille-produits">
{grille()}
      </div>
    </div>
  </section>

  <section class="section section--serre prix-unique">
    <div class="wrap apparait">
      <h2>Tous les sacs · {PRIX}</h2>
      <p>Parce que le style ne devrait pas être compliqué.</p>
    </div>
  </section>"""

page("sacs.html", "Les sacs — Studio Alma",
     f"Cinq city bags Studio Alma, tous à {PRIX}. Jeanne, Romy, Louise, Victoire, Margot.",
     sacs, actif="sacs")

# -------------------------------------------------------------- pages produit
def page_produit(p):
    autres = [a for a in PRODUITS if a["id"] != p["id"]][:3]
    minis = "\n".join(
        f'            <button type="button" data-miniature="../{img}" aria-current="{str(i == 0).lower()}" aria-label="Vue {i+1}">'
        f'<img src="../{img}" alt="" loading="lazy"></button>'
        for i, img in enumerate(p["images"]))
    accordeons = [
        ("Détails", p["details"]),
        ("Dimensions", p["dimensions"]),
        ("Matières", p["matieres"]),
        ("Livraison &amp; retours", "Expédition sous 24 h, livraison en 2 à 4 jours en France. "
                                    "Retours gratuits sous 30 jours."),
    ]
    blocs = "\n".join(f"""          <div class="accordeon" data-ouvert="false">
            <button class="accordeon__tete" type="button" aria-expanded="false">{t}<span class="accordeon__signe">+</span></button>
            <div class="accordeon__corps"><p>{c}</p></div>
          </div>""" for t, c in accordeons)

    corps = f"""  <div class="wrap fil"><a href="../sacs.html">Les sacs</a> · {p['nom']}</div>

  <div class="wrap produit">
    <div class="galerie apparait">
      <div class="galerie__vue"><img data-vue src="../{p['images'][0]}" alt="{p['nom']} — city bag Studio Alma" width="900" height="1125" fetchpriority="high"></div>
      <div class="galerie__vue"><img src="../{p['images'][1]}" alt="{p['nom']}, vue détail" loading="lazy" width="900" height="1125"></div>
      <div class="galerie__miniatures">
{minis}
      </div>
    </div>

    <div class="panneau apparait">
      <h1 class="panneau__nom">{p['nom']}</h1>
      <p class="panneau__prix">{PRIX}</p>
      <p class="panneau__type">{p['type']}</p>
      <p class="panneau__desc">{p['description']}</p>
      <button class="btn btn--bloc" type="button" data-ajouter="{p['id']}">Ajouter au panier</button>
      <div class="rassurances">
        <span>Livraison offerte</span><span>Paiement sécurisé</span><span>Retours faciles</span>
      </div>
      <div class="accordeons">
{blocs}
      </div>
    </div>
  </div>

  <section class="section" style="padding-top:0">
    <div class="wrap">
      <div class="section__tete apparait"><h2 class="titre-section" style="font-size:clamp(22px,4vw,32px)">Vous aimerez aussi</h2></div>
      <div class="grille-produits">
{chr(10).join(carte(a, '../') for a in autres)}
      </div>
    </div>
  </section>"""

    page(f"produit/{p['id']}.html", f"{p['nom']} — City bag {PRIX} — Studio Alma",
         p["description"], corps, base="../", actif="sacs")

for p in PRODUITS:
    page_produit(p)

# --------------------------------------------------------------- panier.html
page("panier.html", "Panier — Studio Alma", "Votre panier Studio Alma.",
     '  <div class="wrap" style="padding-top:40px" data-panier></div>', actif="panier")

# ------------------------------------------------------------- a-propos.html
apropos = f"""  <section class="page-tete apparait">
    <div class="wrap">
      <p class="eyebrow">Studio Alma</p>
      <h1 class="titre-section">À propos</h1>
      <p class="soustitre">Une jeune marque française de city bags, née à Paris.</p>
    </div>
  </section>

  <div class="editorial">
    <div class="editorial__media" style="aspect-ratio:16/7.5">
      <img src="assets/img/editorial.jpg" alt="City bag Studio Alma sur une table de café" loading="lazy" width="1200" height="562">
    </div>
  </div>

  <section class="section">
    <div class="wrap texte-long apparait">
      <p>Studio Alma est née d'une idée simple : un sac qui suit la journée entière, sans qu'on ait
      à y penser. Le métro le matin, le bureau, un café, un dîner. Rien de plus.</p>
      <h2>Cinq modèles</h2>
      <p>Nous dessinons cinq sacs, pas trente. Jeanne, Romy, Louise, Victoire et Margot :
      cinq formes qui couvrent à peu près tout ce qu'une journée demande.</p>
      <h2>Un seul prix</h2>
      <p>Tous nos sacs coûtent {PRIX}. Pas de promotion permanente, pas de calcul compliqué :
      vous choisissez la forme qui vous ressemble, le prix ne change rien.</p>
      <h2>Facile à porter</h2>
      <p>Des matières légères, des finitions propres, des bandoulières réglables.
      Des sacs faits pour être portés, pas rangés dans une housse.</p>
      <p style="margin-top:34px"><a class="lien-souligne" href="sacs.html">Voir la collection</a></p>
    </div>
  </section>"""
page("a-propos.html", "À propos — Studio Alma",
     "Studio Alma, jeune marque française de city bags pensés pour la ville.", apropos, actif="apropos")

# ------------------------------------------------------- pages informatives
def page_texte(nom, titre, chapo, sections):
    corps = f"""  <section class="page-tete apparait">
    <div class="wrap">
      <h1 class="titre-section">{titre}</h1>
      <p class="soustitre">{chapo}</p>
    </div>
  </section>
  <section class="section" style="padding-top:20px">
    <div class="wrap texte-long apparait">
{"".join(f'      <h2>{t}</h2>{chr(10)}      <p>{c}</p>{chr(10)}' for t, c in sections)}    </div>
  </section>"""
    page(nom, f"{titre} — Studio Alma", chapo, corps)

page_texte("livraison.html", "Livraison &amp; retours",
           "Tout ce qu'il faut savoir, en quelques lignes.",
           [("Expédition", "Toutes les commandes partent sous 24 h ouvrées depuis la France."),
            ("Délais", "2 à 4 jours en France métropolitaine, 3 à 7 jours en Europe."),
            ("Frais", "La livraison est offerte sur toutes les commandes, sans minimum d'achat."),
            ("Retours", "30 jours pour changer d'avis. Retour gratuit, remboursement sous 5 jours après réception.")])

page_texte("faq.html", "FAQ", "Les questions qu'on nous pose le plus souvent.",
           [("Tous les sacs sont-ils au même prix ?", f"Oui. Les cinq modèles sont à {PRIX}, toute l'année."),
            ("Quelles matières utilisez-vous ?", "Un extérieur enduit façon cuir et une doublure en coton recyclé."),
            ("Comment entretenir mon sac ?", "Un chiffon doux légèrement humide suffit. Évitez les produits abrasifs."),
            ("Puis-je échanger un modèle ?", "Oui, sous 30 jours. Écrivez-nous et nous nous occupons du reste.")])

page_texte("contact.html", "Contact", "Une question ? On répond vite.",
           [("Par e-mail", "bonjour@studioalma.fr — réponse sous 24 h ouvrées."),
            ("Sur Instagram", "@studioalma, en message direct."),
            ("Commandes", "Précisez votre numéro de commande, cela nous fait gagner du temps.")])

page_texte("compte.html", "Compte", "Espace client — bientôt disponible.",
           [("Vos commandes", "Le suivi de commande arrive très bientôt. En attendant, écrivez-nous à bonjour@studioalma.fr."),
            ("Vos retours", "Les retours se déclarent par e-mail, en une ligne.")])

print("Pages générées :", sum(len(f) for _, _, f in os.walk(ROOT) if True) and "ok")
