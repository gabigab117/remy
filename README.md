# Invent (Réalisé en mars/avril 2023) - Deuxième projet réalisé hors du cadre de ma formation

Projet que j'ai réalisé pour un collègue. Mon tout premier projet complet après ma formation Docstring.
C'est important de se lancer dans un projet à mettre en production.

## Refactoring à faire

A l'époque où j'ai réalisé ce projet, je ne séparais pas encore la logique métier dans des méthodes et fonctions.
Je dois prendre le temps de faire un refactoring sur ce projet.

Mais désormais, je découpe la logique métier dans des méthodes.

Je dois aussi repenser le côté sécurité que je n'appréhendais pas forcément de la bonne manière à l'époque de ce projet.
Evidemment depuis je pense toujours au volet sécurité de mes apps.

## Résumé

### Le but du projet

Le but est de mettre en relation des personnes offrant des idées, et des demandeurs d'idées. On a donc une variante
d'app du style e commerce avec intégration de stripe.
A l'époque (avril 2023) je ne faisais pas encore de tests unitaires.

### En terme d'apprentissage ?

Continuer à manipuler Stripe, les modèles, les querysets.
Mise en place de mon premier moteur de recherche / filtre.
Mise en place d'un tableau de bord utilisateur avec les idées publiées, achetées, vendues et en attente de publication.

stripe listen --forward-to 127.0.0.1:8000/ideas/stripe-webhook/