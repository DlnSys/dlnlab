# 🧪 DLNLab — Roadmap & Suivi

---

# 🚀 Version 1 — MVP

Objectif : version fonctionnelle permettant de lancer des challenges et suivre la progression.

### Structure du projet
- [x] Structure des dossiers du projet
- [x] Fichier de configuration `config.yml`
- [x] Fichiers d'état
  - `progress.json`
  - `current.json`

### Catalogue de challenges
- [x] Catalogue YAML de challenges indexés manuellement

### Runtime des challenges
- [x] Runtime `file`
- [x] Runtime `docker`
- [x] Runtime `netcat`

### Gameplay
- [x] Validation de flag (`SHA256`)
- [x] Hints progressifs
- [x] Write-ups manuels déverrouillables après validation

### Progression utilisateur
- [x] Progression centralisée (`dlnlab progress`)
- [x] Sélection par catégorie et difficulté
- [x] Reprise de challenge (`dlnlab resume`)

### Interface
- [x] CLI Python complète
- [x] Commande `dlnlab` accessible depuis le `PATH`

---

# ⚙️ Version 2 — Améliorations

Objectif : rendre DLNLab plus immersif, fluide et complet.

### Qualité de vie CLI
- [x] Commande `dlnlab list` — afficher tous les challenges avec leur statut
- [x] Commande `dlnlab info <nom>` — afficher les détails d'un challenge sans le lancer
- [x] Couleurs dans le terminal (vert succès, rouge erreur, etc.)
- [x] Confirmation avant d'écraser un challenge en cours
- [x] Menus interactifs avec InquirerPy (flèches clavier) — menu principal, sélection catégorie/difficulté/challenge

### Catalogue
- [ ] Validation du catalogue au démarrage (vérifier que les fichiers référencés existent)

### Sécurité & fiabilité
- [ ] Vérification que le conteneur Docker est accessible avant d'afficher "Challenge started"

### Runtime
- [ ] Port aléatoire pour les runtimes `docker` / `netcat`
- [x] Docker cleanup automatique après validation du flag — `docker rm` le conteneur + `docker rmi` l'image pour libérer l'espace disque
- [ ] Runtime `file` — copier le fichier statique dans `~/dlnlab/workspace/` au lancement et le supprimer à l'arrêt (stop/submit), plutôt que pointer directement vers `challenges/`

### Gameplay
- [x] Timer affiché au moment de la validation du flag
- [x] Commande `dlnlab history` — historique des challenges complétés avec la date

### Distribution
- [ ] Fichier `requirements.txt`
- [ ] Fichier `README.md` avec instructions d'installation

---

# 🧠 Version 3 — Avancé

Objectif : transformer DLNLab en vraie plateforme d'entraînement CTF.

### Runtime avancé
- [ ] Option `docker.cleanup` dans `config.yml` — choisir la stratégie : `none` / `container` / `full` (container + image)
- [ ] Commande `dlnlab docker clean` — cleanup manuel de toutes les images de challenges résolus

### Gameplay avancé
- [ ] Système de scoring
  - points par challenge
  - bonus de rapidité
  - malus pour les hints

- [ ] Multi-flags par challenge

### Analytics
- [ ] Statistiques avancées
  - temps moyen de résolution
  - taux de réussite par catégorie

### Intégrations
- [ ] Intégration **CTFd self-hosted**

---

# 📊 Suivi

Progression actuelle :
