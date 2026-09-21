/* Liens de paiement Studio Alma.
   -----------------------------------------------------------------------
   Renseignez ici le lien de paiement de chaque modèle : lien de paiement
   Stripe, bouton PayPal, checkout Shopify… Tout lien https fonctionne.

   • "defaut"  : lien utilisé pour tous les modèles qui n'ont pas de lien
                 propre (pratique si votre page de paiement gère le choix).
   • "liens"   : un lien par modèle, prioritaire sur le lien par défaut.

   Tant qu'aucun lien n'est renseigné pour un modèle, les boutons
   « Acheter maintenant » et « Passer commande » restent inactifs. */

window.ALMA_PAIEMENT = {
  defaut: "",
  liens: {
    jeanne: "",
    romy: "",
    louise: "",
    victoire: "",
    margot: "",
    clemence: "",
    elise: "",
    camille: "",
    adele: "",
    chloe: "",
    madeleine: ""
  }
};
