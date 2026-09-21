/* Studio Alma — interactions du site (panier, navigation, galerie, accordéons). */
(function () {
  "use strict";

  document.body.classList.remove("no-js");

  var CLE = "studio-alma-panier";
  var BASE = document.body.getAttribute("data-base") || "";

  /* ------------------------------------------------------------- utilitaires */
  function euros(n) {
    return n.toFixed(2).replace(".", ",") + " €";
  }

  function produit(id) {
    return (window.ALMA_PRODUITS || []).filter(function (p) { return p.id === id; })[0];
  }

  function lire() {
    try {
      var brut = localStorage.getItem(CLE);
      var data = brut ? JSON.parse(brut) : [];
      return Array.isArray(data) ? data.filter(function (l) { return produit(l.id); }) : [];
    } catch (e) {
      return [];
    }
  }

  function ecrire(lignes) {
    try { localStorage.setItem(CLE, JSON.stringify(lignes)); } catch (e) {}
    majCompteur();
  }

  function lienPaiement(id) {
    var config = window.ALMA_PAIEMENT || {};
    var liens = config.liens || {};
    return (liens[id] || config.defaut || "").trim();
  }

  function total(lignes) {
    return lignes.reduce(function (s, l) { return s + l.qte * (produit(l.id) || {}).prix; }, 0);
  }

  function nbArticles(lignes) {
    return lignes.reduce(function (s, l) { return s + l.qte; }, 0);
  }

  /* --------------------------------------------------------------- compteur */
  function majCompteur() {
    var n = nbArticles(lire());
    [].forEach.call(document.querySelectorAll("[data-compteur]"), function (el) {
      el.textContent = "(" + n + ")";
    });
  }

  /* ------------------------------------------------------------ notification */
  var minuteur;
  function toast(message) {
    var el = document.querySelector(".toast");
    if (!el) {
      el = document.createElement("div");
      el.className = "toast";
      el.setAttribute("role", "status");
      document.body.appendChild(el);
    }
    el.textContent = message;
    requestAnimationFrame(function () { el.classList.add("est-visible"); });
    clearTimeout(minuteur);
    minuteur = setTimeout(function () { el.classList.remove("est-visible"); }, 2600);
  }

  /* ------------------------------------------------------------------ panier */
  /* Un seul sac par panier : ajouter un modèle remplace celui qui s'y trouve. */
  function ajouter(id) {
    var precedent = lire()[0];
    ecrire([{ id: id, qte: 1 }]);
    return precedent && precedent.id !== id ? produit(precedent.id) : null;
  }

  function retirer(id) {
    ecrire(lire().filter(function (l) { return l.id !== id; }));
  }

  document.addEventListener("click", function (e) {
    var btn = e.target.closest("[data-ajouter]");
    if (btn) {
      e.preventDefault();
      var id = btn.getAttribute("data-ajouter");
      var remplace = ajouter(id);
      var p = produit(id);
      toast(remplace
        ? (p ? p.nom : "Article") + " remplace " + remplace.nom + " dans votre panier"
        : (p ? p.nom : "Article") + " ajouté au panier");
    }

    var achat = e.target.closest("[data-acheter]");
    if (achat) {
      e.preventDefault();
      var idAchat = achat.getAttribute("data-acheter");
      var lien = lienPaiement(idAchat);
      if (!lien) { return; }
      ajouter(idAchat);
      window.location.href = lien;
    }
  });

  /* Les boutons d'achat direct restent inactifs tant qu'aucun lien de
     paiement n'est renseigné dans assets/js/paiement.js. */
  function majBoutonsAchat(racine) {
    [].forEach.call((racine || document).querySelectorAll("[data-acheter]"), function (b) {
      var pret = !!lienPaiement(b.getAttribute("data-acheter"));
      b.disabled = !pret;
      b.setAttribute("aria-disabled", String(!pret));
      b.title = pret ? "" : "Paiement bientôt disponible";
    });
  }

  /* ------------------------------------------------------------ menu mobile */
  var menu = document.querySelector(".menu-mobile");
  function basculerMenu(ouvrir) {
    if (!menu) { return; }
    menu.classList.toggle("est-ouvert", ouvrir);
    document.body.style.overflow = ouvrir ? "hidden" : "";
  }
  document.addEventListener("click", function (e) {
    if (e.target.closest("[data-ouvrir-menu]")) { e.preventDefault(); basculerMenu(true); }
    if (e.target.closest("[data-fermer-menu]")) { e.preventDefault(); basculerMenu(false); }
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { basculerMenu(false); }
  });

  /* ------------------------------------------------------------- accordéons */
  [].forEach.call(document.querySelectorAll(".accordeon"), function (acc) {
    var tete = acc.querySelector(".accordeon__tete");
    var corps = acc.querySelector(".accordeon__corps");
    if (!tete || !corps) { return; }
    tete.addEventListener("click", function () {
      var ouvert = acc.getAttribute("data-ouvert") === "true";
      acc.setAttribute("data-ouvert", ouvert ? "false" : "true");
      tete.setAttribute("aria-expanded", ouvert ? "false" : "true");
      corps.style.maxHeight = ouvert ? "0px" : corps.scrollHeight + "px";
    });
  });

  /* ---------------------------------------------------------------- galerie */
  var vue = document.querySelector("[data-vue]");
  if (vue) {
    [].forEach.call(document.querySelectorAll("[data-miniature]"), function (b) {
      b.addEventListener("click", function () {
        vue.src = b.getAttribute("data-miniature");
        [].forEach.call(document.querySelectorAll("[data-miniature]"), function (o) {
          o.setAttribute("aria-current", String(o === b));
        });
      });
    });
  }

  /* -------------------------------------------------------- apparition douce */
  var cibles = document.querySelectorAll(".apparait");
  if ("IntersectionObserver" in window && cibles.length) {
    var obs = new IntersectionObserver(function (entrees) {
      entrees.forEach(function (entree) {
        if (entree.isIntersecting) {
          entree.target.classList.add("est-visible");
          obs.unobserve(entree.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    [].forEach.call(cibles, function (el) { obs.observe(el); });
  } else {
    [].forEach.call(cibles, function (el) { el.classList.add("est-visible"); });
  }

  /* ------------------------------------------------------------ page panier */
  var zone = document.querySelector("[data-panier]");
  function rendrePanier() {
    if (!zone) { return; }
    var lignes = lire();
    if (!lignes.length) {
      zone.innerHTML =
        '<div class="panier-vide">' +
          '<h1 class="panier-titre">Votre panier est vide</h1>' +
          '<p>Onze modèles vous attendent, tous à 19,99 €.</p>' +
          '<a class="btn" href="' + BASE + 'sacs.html">Voir les sacs</a>' +
        "</div>";
      return;
    }
    var articles = lignes.map(function (l) {
      var p = produit(l.id);
      return (
        '<div class="ligne-panier">' +
          '<a class="ligne-panier__img" href="' + BASE + "produit/" + p.id + '.html">' +
            '<img src="' + BASE + p.images[0] + '" alt="' + p.nom + '" loading="lazy">' +
          "</a>" +
          "<div>" +
            '<a class="ligne-panier__nom" href="' + BASE + "produit/" + p.id + '.html">' + p.nom + "</a>" +
            '<div class="ligne-panier__meta">' + p.type + " · " + euros(p.prix) + "</div>" +
            '<button type="button" class="supprimer" data-supprimer="' + p.id + '">Supprimer</button>' +
          "</div>" +
          "<div>" + euros(p.prix) + "</div>" +
        "</div>"
      );
    }).join("");

    var somme = total(lignes);
    zone.innerHTML =
      '<h1 class="panier-titre">Panier</h1>' +
      '<div class="panier-grille">' +
        "<div>" + articles + "</div>" +
        '<aside class="recap">' +
          "<h2>Récapitulatif</h2>" +
          '<div class="recap__ligne"><span>Sous-total</span><span>' + euros(somme) + "</span></div>" +
          '<div class="recap__ligne"><span>Livraison</span><span>Offerte</span></div>' +
          '<div class="recap__ligne recap__total"><span>Total</span><span>' + euros(somme) + "</span></div>" +
          '<button class="btn btn--bloc" type="button" data-acheter="' + lignes[0].id + '">Passer commande</button>' +
          '<p class="recap__note">Livraison offerte · un sac par commande</p>' +
        "</aside>" +
      "</div>";
    majBoutonsAchat(zone);
  }

  if (zone) {
    zone.addEventListener("click", function (e) {
      var sup = e.target.closest("[data-supprimer]");
      if (sup) { retirer(sup.getAttribute("data-supprimer")); rendrePanier(); }
    });
    rendrePanier();
  }

  majCompteur();
  majBoutonsAchat();
  window.addEventListener("storage", function () { majCompteur(); rendrePanier(); });
})();
