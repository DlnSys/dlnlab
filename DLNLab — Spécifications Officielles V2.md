# DLNLab — Spécifications Officielles V2

## 1. Présentation

DLNLab est un orchestrateur local de challenges de cybersécurité permettant de s'entraîner au CTF et au pentest dans un environnement entièrement local.

### Objectifs

- Indexer des challenges provenant de sources externes (Hackropole, PicoCTF, pwn.college, CTFd…)
- Lancer des environnements selon le type de challenge (fichier local, Docker, netcat)
- Valider les flags soumis
- Suivre la progression
- Reprendre un challenge non terminé
- Proposer des hints progressifs
- Déverrouiller des write-ups après validation

### Inspiré de

- HackTheBox
- Hackropole
- PicoCTF
- Root-Me
- PortSwigger Labs

Fonctionne entièrement en local.

---

## 2. Principe fondamental

> Un challenge = un scénario indépendant avec un flag attendu

Chaque challenge est issu d'une source externe (téléchargé manuellement) et intégré dans le catalogue DLNLab. DLNLab ne crée pas de contenu — il orchestre, valide et suit la progression.

---

## 3. Sources de challenges supportées

### V1 — Catalogue manuel

Les challenges sont téléchargés manuellement par l'utilisateur et indexés dans le catalogue YAML.

Sources recommandées :

| Source                       | URL           | Types                                 |
|------------------------------|---------------|---------------------------------------|
| Hackropole                   | hackropole.fr | reverse, crypto, forensics, web, misc |
| PicoCTF                      | picoctf.org   | multi                                 |
| pwn.college                  | pwn.college   | pwn, système                          |
| CTFd self-hosted             | —             | multi                                 |
| Toute source avec flag natif | —             | multi                                 |

---

## 4. Catégories de challenges

| Catégorie         | Description                                      |
|-------------------|--------------------------------------------------|
| `web`               | Exploitation web, injection, logique applicative |
| `sqli`              | SQL Injection                                    |
| `xss`               | Cross-Site Scripting                             |
| `idor`              | Insecure Direct Object Reference                 |
| `lfi` / `rfi`         | Local/Remote File Inclusion                      |
| `upload`            | File upload abuse                                |
| `auth-bypass`       | Contournement d'authentification                 |
| `jwt`               | JSON Web Token exploitation                      |
| `xxe`               | XML External Entity                              |
| `ssti`              | Server-Side Template Injection                   |
| `command-injection` | Injection de commandes                           |
| `api`               | Exploitation d'API                               |
| `reverse`           | Reverse engineering                              |
| `crypto`            | Cryptographie                                    |
| `forensics`         | Analyse forensique                               |
| `stegano`           | Stéganographie                                   |
| `pwn`               | Exploitation binaire                             |
| `misc`              | Divers                                           |

---

## 5. Niveaux de difficulté

### Easy

- Vulnérabilité visible ou peu cachée
- Exploitation directe
- Peu d'étapes

### Medium

- Reconnaissance nécessaire
- Endpoints ou vecteurs cachés
- Exploitation en plusieurs étapes

### Hard

- Vulnérabilité logique ou complexe
- Chaîne d'exploitation avancée
- Peu d'indices visibles

---

## 6. Types de runtime

DLNLab supporte 3 types de runtime selon le challenge :

### `file`

Challenge statique sous forme de fichier local (binaire, image, pcap, archive…).
Aucun service à lancer — l'utilisateur travaille directement sur le fichier.

```yaml
runtime: file
file: challenge.zip
```

### `docker`

Environnement vulnérable lancé via Docker Compose.
Utilisé pour les challenges web, API, pwn avec service réseau.

```yaml
runtime: docker
compose: docker-compose.yml
port: 8080
```

### `netcat`

Binaire exposé via socket TCP (socat/netcat dans un conteneur Docker).
Utilisé pour les challenges pwn interactifs.

```yaml
runtime: netcat
compose: docker-compose.yml
host: 127.0.0.1
port: 4444
```

---

## 7. Architecture du projet

```
dlnlab/
│
├── catalog/
│   ├── web/
│   │   └── hackropole_babel_web.yml
│   ├── reverse/
│   ├── crypto/
│   ├── forensics/
│   ├── pwn/
│   └── misc/
│
├── challenges/
│   ├── web/
│   ├── reverse/
│   ├── crypto/
│   ├── forensics/
│   ├── pwn/
│   └── misc/
│
├── boxes/
│   └── hackropole_babel_web/
│       └── docker-compose.yml
│
├── writeups/
│   └── hackropole_babel_web.md
│
├── state/
│   ├── progress.json
│   └── current.json
│
├── scripts/
│   ├── __init__.py
│   ├── config.py
│   ├── catalog.py
│   ├── state.py
│   ├── menu.py
│   ├── start.py
│   ├── runtime.py
│   ├── submit.py
│   ├── hints.py
│   ├── stop.py
│   ├── resume.py
│   └── progress.py
│
├── config.yml
├── ROADMAP.md
├── requirements.txt
├── README.md
└── dlnlab
```

---

## 8. Format du catalogue YAML

Chaque challenge est décrit par un fichier YAML indépendant.

```yaml
name: hackropole_babel_web
source: hackropole
url: https://hackropole.fr/fr/challenges/web/fcsc2020-web-babel-web/
theme: web
category: web
difficulty: easy
description: >
  An audit of a website under construction is requested to find a flag.
  The target is accessible via http://localhost:8000/.
runtime: docker
compose: docker-compose.yml
port: 8000

flag:
  format: FCSC{...}
  value: a061095c06bc5a7f89fcdf5762f9f3c253dfe4952e9fd296f0e5921bd8f668c0  # SHA256 du flag

hints:
  - "Inspecte les différentes pages et ressources du site."
  - "Cherche des fichiers ou endpoints non listés."

writeup: writeups/hackropole_babel_web.md

enabled: true
```

### Champs obligatoires

| Champ       | Description                     |
|-------------|---------------------------------|
| `name`        | Identifiant unique du challenge |
| `source`      | Origine du challenge            |
| `theme`       | Thème principal                 |
| `category`    | Catégorie de vulnérabilité      |
| `difficulty`  | easy / medium / hard            |
| `description` | Brief affiché au lancement      |
| `runtime`     | file / docker / netcat          |
| `flag.format` | Format du flag (ex: FCSC{…})    |
| `flag.value`  | Hash SHA256 du flag attendu     |

### Champs optionnels

| Champ   | Description                               |
|---------|-------------------------------------------|
| `url`     | URL source du challenge                   |
| `hints`   | Liste de 1 à 3 hints                      |
| `writeup` | Chemin vers le fichier write-up           |
| `enabled` | true / false (exclure du catalogue actif) |

---

## 9. Stockage des flags

Les flags ne sont **jamais stockés en clair** dans le catalogue.

```
flag brut → SHA256 → stocké dans flag.value
```

À la soumission, DLNLab hash le flag soumis et compare avec la valeur stockée.

---

## 10. État et progression

### `state/progress.json`

```json
{
  "completed": [
    "hackropole_babel_web"
  ],
  "unfinished": [],
  "hints_used": {}
}
```

### `state/current.json`

```json
{
  "name": "hackropole_babel_web",
  "runtime": "docker",
  "started_at": "2026-03-14T14:32:00",
  "container_id": "abc123"
}
```

---

## 11. Interface CLI

### Commande principale

```
dlnlab
```

Menu principal :

```
╔══════════════════════════════╗
║         D L N L A B          ║
╚══════════════════════════════╝

  1 - Start new challenge
  2 - Resume unfinished challenge
  3 - Show progress
  4 - Exit

> _
```

### Commandes disponibles

| Commande                  | Description                                        |
|---------------------------|----------------------------------------------------|
| `dlnlab`                  | Ouvre le menu principal                            |
| `dlnlab submit <flag>`    | Soumet un flag                                     |
| `dlnlab hint`             | Affiche le prochain hint                           |
| `dlnlab stop`             | Arrête le challenge en cours                       |
| `dlnlab resume`           | Reprend un challenge non terminé                   |
| `dlnlab progress`         | Affiche la progression globale                     |
| `dlnlab list`             | Liste tous les challenges avec leur statut *(V2)*  |
| `dlnlab info <nom>`       | Affiche les détails d'un challenge *(V2)*          |
| `dlnlab add`              | Ajoute un challenge de façon interactive *(V2)*    |
| `dlnlab history`          | Historique des challenges complétés *(V2)*         |

---

## 12. Démarrage d'un challenge

### Sélection

```
Category:
  1 - Web
  2 - Reverse
  3 - Crypto
  4 - Forensics
  5 - Pwn
  6 - Misc
  7 - Random

Difficulty:
  1 - Easy
  2 - Medium
  3 - Hard
  4 - Random
```

### Algorithme de sélection

1. Filtrer par catégorie
2. Filtrer par difficulté
3. Exclure les challenges terminés
4. Exclure le challenge en cours si existant
5. Confirmation si un challenge est déjà en cours
6. Choisir aléatoirement parmi les restants

### Affichage au lancement

```
╔══════════════════════════════════════════╗
║           CHALLENGE STARTED              ║
╚══════════════════════════════════════════╝

Name       : hackropole_babel_web
Category   : web / web
Difficulty : Easy
Source     : Hackropole

Brief :
  An audit of a website under construction is requested to find a flag.

Target     : http://127.0.0.1:8000
Flag format: FCSC{...}

Commands:
  dlnlab submit <flag>   → submit a flag
  dlnlab hint            → get a hint
  dlnlab stop            → stop the challenge
```

---

## 13. Soumission d'un flag

```
dlnlab submit FCSC{...}
```

### Si correct

```
✓ Correct flag! Challenge completed.
  Time: 12m 34s

Write-up unlocked → writeups/hackropole_babel_web.md
Open write-up? [y/N]
```

### Si incorrect

```
✗ Wrong flag. Keep trying.
```

---

## 14. Hints progressifs

```
dlnlab hint
```

Les hints sont débloqués un par un dans l'ordre.

```
Hint 1/3 : Inspecte les différentes pages et ressources du site.

Unlock next hint? [y/N]
```

Les hints utilisés sont enregistrés dans `progress.json`.

---

## 15. Write-ups

Chaque challenge peut avoir un fichier `writeup.md` associé.

- **Verrouillé** tant que le flag n'est pas validé
- **Déverrouillé** automatiquement après `dlnlab submit` validé
- **Manuel** : rédigé par l'utilisateur après avoir fait le challenge
- Si le fichier est vide : message "No write-up available for this challenge yet."

### Structure recommandée d'un write-up

```markdown
# Write-up : hackropole_babel_web

## Contexte
...

## Reconnaissance
...

## Exploitation
...

## Flag
FCSC{...}

## Ce que j'ai appris
...
```

---

## 16. Arrêt d'un challenge

```
dlnlab stop
```

```
Stop current challenge: hackropole_babel_web

  1 - Mark as completed
  2 - Keep as unfinished
  3 - Cancel

> _
```

- Option 1 → déplacé dans `completed`, conteneur arrêté
- Option 2 → déplacé dans `unfinished`, conteneur arrêté
- Option 3 → annulation, challenge toujours actif

---

## 17. Reprise d'un challenge

```
dlnlab resume
```

```
Unfinished challenges:

  1 - hackropole_babel_web  [web / easy]   hints used: 1/2

> _
```

---

## 18. Progression

```
dlnlab progress
```

```
╔══════════════════════════════════════════╗
║              PROGRESSION                 ║
╚══════════════════════════════════════════╝

Completed   : 4
Unfinished  : 2
Remaining   : 18
Total       : 24

By category:
  web       ████████░░  4/10
  reverse   ██░░░░░░░░  1/8
  crypto    ░░░░░░░░░░  0/4
  forensics ░░░░░░░░░░  0/2
```

---

## 19. Configuration

Fichier `config.yml` à la racine du projet :

```yaml
catalog_dir: catalog/
challenges_dir: challenges/
boxes_dir: boxes/
writeups_dir: writeups/
state_dir: state/

default_difficulty: random
default_category: random
```

---

## 20. Roadmap

### Version 1 — MVP

- Catalogue YAML de challenges indexés manuellement
- 3 runtimes : file, docker, netcat
- Validation de flag (SHA256)
- Hints progressifs
- Write-ups manuels déverrouillables
- Progression centralisée
- Sélection par catégorie et difficulté
- Reprise de challenge
- CLI Python

### Version 2 — Améliorations

- Commande `dlnlab list` avec statut des challenges
- Commande `dlnlab info <nom>`
- Couleurs dans le terminal
- Confirmation avant d'écraser un challenge en cours
- Commande `dlnlab add` interactive
- Validation du catalogue au démarrage
- Vérification de l'accessibilité Docker avant lancement
- Port aléatoire pour les runtimes Docker/netcat
- Briefs immersifs (contexte narratif au lancement)
- Timer affiché à la validation du flag
- Commande `dlnlab history`
- Fichier `requirements.txt`
- Fichier `README.md`

### Version 3 — Avancé

- Système de scoring (points par challenge, bonus rapidité, malus hints)
- Multi-flags par challenge
- Statistiques avancées (temps moyen, taux de réussite par catégorie)
- Intégration CTFd self-hosted

---

## 21. Mode CTF (V4)

### Objectif

Permettre de lancer un CTF complet en une seule commande depuis DLNLab, sans configuration manuelle.

### Rôle des composants

| Composant | Rôle |
|-----------|------|
| **DLNLab** | Sélectionne les challenges, lance les boxes Docker/netcat, gère la logique de génération |
| **CTFd** | Gère les joueurs/équipes, affiche les challenges, valide les flags, scoreboard |

### Commandes

| Commande | Description |
|----------|-------------|
| `dlnlab ctf` | Lance une session CTF complète |
| `dlnlab ctf stop` | Arrête et cleanup tout |

### Génération de session

Au lancement de `dlnlab ctf`, DLNLab pose les questions suivantes :

- Thème : web / reverse / crypto / forensics / pwn / misc / random
- Difficulté : easy / medium / hard / mix / random
- Nombre de challenges
- Répartition (ex : 4 easy, 4 medium, 2 hard)

Puis sélectionne les challenges correspondants dans le catalogue (manuellement ou aléatoirement).

### Randomisation

- **Full random** : thème + difficulté + challenges tous randomisés
- **Semi-random** : thème fixe, difficulté et challenges aléatoires
- **Seed rejouable** : enregistrement d'une seed pour reproduire une session identique

### Réseau

Les challenges doivent être accessibles via l'IP réelle de la machine (pas `127.0.0.1`) pour permettre un usage multi-utilisateurs en LAN ou VPN.

```yaml
# config.yml
host_ip: 192.168.1.10   # IP réelle de la machine
```

### Infrastructure

```
infra/
└── ctfd/
    └── docker-compose.yml   # Instance CTFd
```

- CTFd est lancé automatiquement via `docker compose up`
- Les challenges sélectionnés sont importés dans CTFd via l'API REST (nom, description, flag, points)
- À l'arrêt, CTFd et les boxes sont stoppés et nettoyés

---

## 22. Objectif final

Créer un cyber-range personnel permettant :

- Entraînement continu toutes catégories CTF
- Apprentissage progressif du pentest et de la sécurité offensive
- Suivi de progression détaillé
- Simulation de conditions proches des CTF réels
- Capitalisation des connaissances via les write-ups
