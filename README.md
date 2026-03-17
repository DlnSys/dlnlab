# DLNLab

Orchestrateur local de challenges de cybersécurité — entraînement CTF et pentest en environnement entièrement local.

Inspiré de HackTheBox, Hackropole, PicoCTF et Root-Me. Fonctionne entièrement hors ligne une fois les challenges téléchargés.

Supporte 3 types de runtime : fichiers statiques, environnements Docker, et services netcat. La progression, les hints et les write-ups sont centralisés dans une CLI simple et interactive.

---

## Merci Hackropole

Un immense merci à l'[ANSSI](https://www.ssi.gouv.fr) et à toute l'équipe derrière [Hackropole](https://hackropole.fr) pour la qualité exceptionnelle des challenges proposés et leur mise à disposition sous licence ouverte. Ce projet n'aurait pas été possible sans leur travail remarquable.

Les métadonnées des challenges Hackropole incluses dans ce dépôt sont publiées sous [Licence ouverte / Etalab 2.0](https://www.etalab.gouv.fr/licence-ouverte-open-licence) — © ANSSI.

---

## Installation

```bash
bash <(wget -qO- https://raw.githubusercontent.com/DlnSys/dlnlab/main/install.sh)
```

Le script vérifie et installe automatiquement les prérequis suivants :

| Prérequis | Rôle |
|-----------|------|
| Python 3.10+ | Moteur CLI |
| pip | Gestionnaire de paquets Python |
| Docker + Docker Compose | Lancement des environnements vulnérables |
| Git | Clonage du dépôt |

Redémarre ensuite ton terminal ou tape `source ~/.zshrc`.

### Peupler le catalogue (à faire une seule fois)

Une fois installé, télécharge les challenges Hackropole :

```bash
cd /opt/dlnlab

# Tous les challenges
python hackropole_scraper.py

# Par catégorie
python hackropole_scraper.py --category web

# Exclure une catégorie
python hackropole_scraper.py --exclude forensics

# Tester sans télécharger
python hackropole_scraper.py --dry-run --limit 5
```

Catégories disponibles : `web` `reverse` `crypto` `pwn` `misc` `hardware` `forensics`

> ⚠️ **Espace disque** : la catégorie `forensics` seule peut dépasser **40 Go+** (images disque, captures réseau, fichiers binaires lourds). Le catalogue complet nécessite plusieurs dizaines de Go libres. Il est fortement recommandé de commencer sans forensics :
> ```bash
> python hackropole_scraper.py --exclude forensics
> ```
> Et de l'ajouter séparément uniquement si tu as l'espace nécessaire.

---

## Utilisation

```bash
# Menu principal
dlnlab

# Soumettre un flag
dlnlab submit FCSC{...}

# Obtenir un hint
dlnlab hint

# Arrêter le challenge en cours
dlnlab stop

# Reprendre un challenge non terminé
dlnlab resume

# Afficher la progression
dlnlab progress

# Lister tous les challenges avec leur statut
dlnlab list

# Détails d'un challenge
dlnlab info <nom>

# Historique des challenges complétés
dlnlab history
```

---

## Runtimes supportés

| Runtime  | Description                                              |
|----------|----------------------------------------------------------|
| `file`   | Fichier statique copié dans `~/dlnlab/workspace/`        |
| `docker` | Environnement web/API lancé via Docker Compose           |
| `netcat` | Binaire exposé via socket TCP (pwn interactif)           |

---

## Ajouter ses propres challenges

DLNLab accepte n'importe quelle source de challenges disposant d'un flag. Voici comment intégrer un challenge manuellement.

### 1. Créer le fichier catalogue YAML

Dans `catalog/{category}/{nom}.yml` :

```yaml
name: mon_challenge
source: perso
url: https://...
theme: web
category: web
difficulty: easy
description: >
  Description du challenge.
runtime: docker        # file / docker / netcat

compose: docker-compose.yml
service: app
port: 8080

flag:
  format: FLAG{...}
  value: <SHA256 du flag>   # echo -n "FLAG{...}" | sha256sum

hints:
  - "Premier indice."
  - "Deuxième indice."

writeup: writeups/mon_challenge.md
enabled: true
```

### 2. Selon le runtime

**`file`** — placer le fichier dans :
```
challenges/{category}/{nom}/{fichier}
```

**`docker` / `netcat`** — placer le `docker-compose.yml` dans :
```
boxes/{nom}/docker-compose.yml
```

### 3. Générer le hash du flag

```bash
echo -n "FLAG{mon_flag}" | sha256sum
```

Coller le hash dans `flag.value` du YAML.

---

## Contribuer

DLNLab est ouvert aux contributions, notamment pour enrichir le catalogue de challenges.

Tu peux contribuer en :
- Ajoutant des challenges compatibles (voir section ci-dessus)
- Signalant des bugs via les Issues GitHub
- Proposant des améliorations via Pull Request

> Les boxes et fichiers de challenges ne sont pas inclus dans le dépôt pour des raisons de droits. Seules les métadonnées YAML sont partagées.

---

## Configuration

Fichier `config.yml` à la racine :

```yaml
workspace_dir: ~/dlnlab/workspace   # Dossier de travail pour les challenges file
host_ip: auto                        # IP affichée (auto = détection automatique)
```

---

## Structure du projet

```
dlnlab/
├── catalog/          # Métadonnées YAML des challenges (Etalab 2.0)
├── challenges/       # Fichiers statiques des challenges (gitignored)
├── boxes/            # Docker Compose des challenges (gitignored)
├── writeups/         # Write-ups personnels (gitignored)
├── state/            # Progression et état courant
├── scripts/          # Code source CLI
├── main.py           # Point d'entrée Python
├── dlnlab            # Wrapper bash
├── install.sh        # Script d'installation
├── config.yml        # Configuration
└── requirements.txt  # Dépendances Python
```

---

## Contact

Une question, un bug, une idée ? Envoie un mail à : [contact@example.com](mailto:contact@example.com)

---

## Licence

Code source : [MIT](https://opensource.org/licenses/MIT) — utilisation, modification et redistribution libres, à condition de conserver la mention de copyright.

Contenus Hackropole : [Licence ouverte / Etalab 2.0](https://www.etalab.gouv.fr/licence-ouverte-open-licence) — © ANSSI
