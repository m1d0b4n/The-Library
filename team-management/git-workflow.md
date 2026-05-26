# Workflow Git

## Principe général

```
main        → code stable, toujours fonctionnel
feature/*   → nouvelles fonctionnalités
fix/*       → corrections de bugs
test/*      → ajout/modification de tests
```

---

## Étapes pour contribuer

### 1. Récupérer les dernières modifications
```bash
git checkout main
git pull origin main
```

### 2. Créer sa branche
```bash
git checkout -b feature/nom-de-ta-tache
# Exemples :
# git checkout -b feature/securisation-routes
# git checkout -b fix/correction-reservation
# git checkout -b test/tests-bibliotheque
```

### 3. Travailler et committer
```bash
git add .
git commit -m "feat: description courte de ce que tu as fait"
```

> **Conventions de commit :**
> - `feat:` → nouvelle fonctionnalité
> - `fix:` → correction de bug
> - `test:` → ajout de tests
> - `docs:` → documentation
> - `refactor:` → refactoring sans changement de comportement

### 4. Pousser sa branche
```bash
git push origin feature/nom-de-ta-tache
```

### 5. Ouvrir une Pull Request sur GitHub
- Va sur le repo GitHub
- Clique sur **"Compare & pull request"**
- Décris ce que tu as fait
- Assigne un reviewer (un autre membre de l'équipe)
- Lie la PR à l'issue correspondante dans le Project board

### 6. Après validation → merge dans `main`
C'est **Rudy** (Scrum Master) qui valide et merge les PRs.

---

## À ne jamais faire

```bash
git push origin main        # ❌ interdit
git commit -m "fix"         # ❌ message trop vague
git add . && git commit ... # ⚠️  vérifier ce qu'on ajoute avant
```
