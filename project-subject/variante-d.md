# Variante d'exercice d'entraînement : Modernisation et sécurisation d'une application de gestion de bibliothèque

Ce sujet d'entraînement vous propose de travailler sur la sécurisation et l'évolution d'une application web dédiée à la gestion d'une librairie fictive, baptisée "Librairie ABC". Il s'agit d'un exercice pratique qui vise à préparer les candidats aux problématiques réelles de sécurisation, de revue de code, de tests automatisés et de déploiement sécurisé dans un contexte Agile.

---

## Contexte général

La "Librairie ABC" dispose d'une application web initiale développée il y a quelques années pour permettre la gestion de ses collections et la réservation de livres par ses utilisateurs. Cette version opérationnelle présente cependant un certain nombre de vulnérabilités de sécurité, des problèmes d'optimisation et des difficultés d'adaptation aux évolutions du marché.

Votre équipe, nouvellement constituée, est chargée de reprendre le projet afin d'en améliorer la qualité, la sécurité et la maintenabilité. Vous travaillerez en mode Agile, en veillant à impliquer tous les membres de l'équipe dans l'évolution du projet et la préparation du déploiement de la nouvelle version de l'application.

---

## Objectifs et thèmes abordés

Les principaux axes de cet exercice s'articulent autour des thématiques suivantes :

1. **Organisation d'équipe et gestion de projet en Agile**
   - Définition de la répartition des rôles au sein de l'équipe.
   - Mise en place d'un planning Agile détaillé (sprint planning, rétrospectives, daily stand-up, etc.).
   - Identification des priorités du projet et mise en commun des points forts de chacun.

2. **Revue de code et amélioration de la qualité logicielle**
   - Réaliser une analyse critique du code existant.
   - Identifier les points faibles et proposer des améliorations concrètes (optimisations, refactoring, bonnes pratiques de sécurité).
   - Mettre en place des règles pour la gestion des URL et la sécurisation des routes (exemple : anonymisation des extensions et restriction d'accès aux dossiers sensibles).

3. **Gestion des tests et évaluation de la sécurité**
   - Mise en œuvre d'une série de tests avec des outils automatisés (tel que SonarQube ou d'autres outils d'analyse statique et dynamique).
   - Réalisation de tests de vulnérabilité incluant des scénarios de tests aux limites, des injections ou des simulations d'attaques (pentesting).
   - Analyse des rapports générés, interprétation des résultats et proposition de solutions pour renforcer la sécurité.

4. **Réécriture des spécifications et planification du déploiement**
   - Reformuler les spécifications fonctionnelles et techniques à partir des observations issues de la revue de code et des tests.
   - Élaborer un planning détaillé des corrections et améliorations à apporter avant le déploiement final.
   - Assurer la traçabilité des actions et la communication avec l'ensemble des stakeholders du projet.

---

## Déroulement de l'exercice

Votre équipe devra préparer un rapport de synthèse sous forme de présentation (PDF ou PowerPoint) à présenter oralement devant un jury. Chaque membre de l'équipe devra participer activement lors de la présentation.

Voici un plan suggéré pour votre livrable :

1. **Introduction et présentation de l'équipe**
   - Présentation rapide de la Librairie ABC et du contexte de l'exercice.
   - Organisation de l'équipe (rôles, répartition des tâches, méthode de collaboration Agile).

2. **Évaluation initiale du code et mise en place de bonnes pratiques**
   - Analyse du code existant et identification des principales faiblesses.
   - Propositions concrètes pour la sécurisation de l'application (gestion des URL, restrictions d'accès, etc.).

3. **Mise en place des tests automatiques et analyse des résultats**
   - Présentation des outils et méthodes utilisés pour réaliser les tests (par exemple : configuration et résultats de type SonarQube).
   - Synthèse des vulnérabilités détectées, avec un scoring indiquant le niveau de risque associé à chacune.

4. **Propositions de refactoring et réécriture des spécifications**
   - Reformulation des spécifications fonctionnelles en tenant compte des failles détectées.
   - Présentation des correctifs à apporter et des améliorations techniques et fonctionnelles.

5. **Planification Agile du déploiement final**
   - Élaboration d'un planning avec les sprints et les tâches critiques à réaliser.
   - Stratégie de déploiement sur un environnement de test sécurisé et recommandations pour la mise en production.

---

## Points clés pour la réussite de la mission

- **Communication interne et documentation**  
  Assurez-vous que chaque membre de l'équipe dispose d'une vision claire du projet, des tâches à accomplir et des outils mis en place. La documentation et les échanges réguliers sont essentiels pour minimiser les erreurs et assurer la qualité du déploiement.

- **Utilisation d'outils de suivi et de gestion de projet**  
  Employez des outils collaboratifs (comme Trello, Jira ou autres) pour suivre les tâches, documenter les progrès et centraliser les informations relatives aux tests et aux corrections.

- **Focalisation sur la sécurité**  
  La finalité de cet exercice est de préparer l'application à un déploiement sécurisé. Ne négligez pas l'analyse des vulnérabilités et la mise en place de correctifs. Pesez les risques associés à chaque faille et priorisez vos actions en conséquence.

- **Approche itérative et incrémentale**  
  Travaillez par petites itérations (sprints) pour pouvoir tester, valider et ajuster au fur et à mesure de l'évolution du projet. Cela vous permettra de mieux gérer les imprévus et de garantir une meilleure qualité de code.
