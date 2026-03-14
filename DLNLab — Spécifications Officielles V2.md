# DLNLab — Spécifications Officielles V2

## 1. Présentation

DLNLab est un orchestrateur local de challenges de cybersécurité permettant de s’entraîner au CTF et au pentest dans un environnement entièrement local.

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

Chaque challenge est issu d’une source externe (téléchargé manuellement) et intégré dans le catalogue DLNLab. DLNLab ne crée pas de contenu — il orchestre, valide et suit la progression.

---

## 3. Sources de challenges supportées

### V1 — Catalogue manuel

Les challenges sont téléchargés manuellement par l’utilisateur et indexés dans le catalogue YAML.

Sources recommandées :

| Source                       | URL           | Types                                 |
|------------------------------|---------------|---------------------------------------|
| Hackropole                   | hackropole.fr | reverse, crypto, forensics, web, misc |
| PicoCTF                      | picoctf.org   | multi                                 |
| pwn.college                  | pwn.college   | pwn, système                          |
| CTFd self-hosted             | —             | multi                                 |
| Toute source avec flag natif | —             | multi                                 |

### V2 — Intégration API (roadmap)

Synchronisation automatique du catalogue via les APIs officielles des plateformes.

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
| `auth-bypass`       | Contournement d’authentification                 |
| `jwt`               | JSON Web Token exploitation                      |
| `xxe`               | XML External Entity                              |
| `ssti`              | Server-Side Template Injection                   |
| `command-injection` | Injection de commandes                           |
| `api`               | Exploitation d’API                               |
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
- Peu d’étapes

### Medium

- Reconnaissance nécessaire
- Endpoints ou vecteurs cachés
- Exploitation en plusieurs étapes

### Hard

- Vulnérabilité logique ou complexe
- Chaîne d’exploitation avancée
- Peu d’indices visibles

---

## 6. Types de runtime

DLNLab supporte 3 types de runtime selon le challenge :

### `file`

Challenge statique sous forme de fichier local (binaire, image, pcap, archive…).
Aucun service à lancer — l’utilisateur travaille directement sur le fichier.

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
│   │   ├── picoctf_sqli_easy.yml
│   │   └── hackropole_jwt_medium.yml
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
│   ├── picoctf_webnet0/
│   │   └── docker-compose.yml
│   └── pwncollege_format_string/
│       └── docker-compose.yml
│
├── writeups/
│   ├── picoctf_sqli_easy.md
│   └── hackropole_jwt_medium.md
│
├── state/
│   ├── progress.json
│   └── current.json
│
├── scripts/
│   ├── start.py
│   ├── stop.py
│   ├── submit.py
│   ├── resume.py
│   ├── progress.py
│   └── hints.py
│
├── config.yml
└── dlnlab
```

---

## 8. Format du catalogue YAML

Chaque challenge est décrit par un fichier YAML indépendant.

```yaml
name: picoctf_sqli_easy
source: picoctf
url: https://picoctf.org/challenges
theme: web
category: sqli
difficulty: easy
description: >
  A login form is exposed on an internal service.
  No credentials are provided.
runtime: file
file: challenge/login_form.zip

flag:
  format: picoCTF{...}
  value: picoCTF{th1s_1s_th3_fl4g}   # hashé en SHA256 dans le fichier réel

hints:
  - "Essaie d'insérer un caractère spécial dans le champ username"
  - "Les commentaires SQL peuvent être utiles ici"
  - "Tente une injection de type ' OR 1=1--"

writeup: writeups/picoctf_sqli_easy.md  # vide = non disponible

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
| `flag.format` | Format du flag (ex: picoCTF{…}) |
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
    "picoctf_sqli_easy",
    "hackropole_rsa_easy"
  ],
  "unfinished": [
    "picoctf_webnet0"
  ],
  "hints_used": {
    "picoctf_webnet0": [0, 1]
  }
}
```

### `state/current.json`

```json
{
  "name": "picoctf_webnet0",
  "runtime": "docker",
  "started_at": "2025-03-11T14:32:00",
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

---

## 12. Démarrage d’un challenge

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
5. Choisir aléatoirement parmi les restants

### Affichage au lancement

```
╔══════════════════════════════════════════╗
║           CHALLENGE STARTED              ║
╚══════════════════════════════════════════╝

Name       : picoctf_webnet0
Category   : web / sqli
Difficulty : Easy
Source     : PicoCTF

Brief :
  A login form is exposed on an internal service.
  No credentials are provided.

Target     : http://127.0.0.1:8080
Flag format: picoCTF{...}

Commands:
  dlnlab submit <flag>   → submit a flag
  dlnlab hint            → get a hint
  dlnlab stop            → stop the challenge
```

---

## 13. Soumission d’un flag

```
dlnlab submit picoCTF{th1s_1s_th3_fl4g}
```

### Si correct

```
✓ Correct flag! Challenge completed.

Write-up unlocked → writeups/picoctf_sqli_easy.md
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

Les hints sont débloqués un par un dans l’ordre.

```
Hint 1/3 : Essaie d'insérer un caractère spécial dans le champ username

Unlock next hint? [y/N]
```

Les hints utilisés sont enregistrés dans `progress.json`.

---

## 15. Write-ups

Chaque challenge peut avoir un fichier `writeup.md` associé.

- **Verrouillé** tant que le flag n’est pas validé
- **Déverrouillé** automatiquement après `dlnlab submit` validé
- **Manuel** : rédigé par l’utilisateur après avoir fait le challenge
- Si le fichier est vide : message “No write-up available for this challenge yet.”

### Structure recommandée d’un write-up

```markdown
# Write-up : picoctf_sqli_easy

## Contexte
...

## Reconnaissance
...

## Exploitation
...

## Flag
picoCTF{...}

## Ce que j'ai appris
...
```

---

## 16. Arrêt d’un challenge

```
dlnlab stop
```

```
Stop current challenge: picoctf_webnet0

  1 - Mark as completed
  2 - Keep as unfinished
  3 - Cancel

> _
```

- Option 1 → déplacé dans `completed`, conteneur arrêté
- Option 2 → déplacé dans `unfinished`, conteneur arrêté
- Option 3 → annulation, challenge toujours actif

---

## 17. Reprise d’un challenge

```
dlnlab resume
```

```
Unfinished challenges:

  1 - picoctf_webnet0     [web / easy]   hints used: 2/3
  2 - hackropole_elf_rev  [reverse / medium]   hints used: 0/3

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

### Version 1 — MVP (actuelle spec)

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

- Write-ups générés par IA (Claude API) avec wrapper shell optionnel
- Briefs immersifs (contexte narratif au lancement)
- Port aléatoire pour les runtimes Docker/netcat
- Intégration API Hackropole et PicoCTF (sync automatique du catalogue)
- Mode `dlnlab create` pour assister la création de scénarios custom

### Version 3 — Avancé

- Système de scoring (points par challenge, bonus rapidité, malus hints)
- Multi-flags par challenge
- Statistiques avancées (temps moyen, taux de réussite par catégorie)
- Intégration CTFd self-hosted
- Génération de challenges via IA

---

## 21. Objectif final

Créer un cyber-range personnel permettant :

- Entraînement continu toutes catégories CTF
- Apprentissage progressif du pentest et de la sécurité offensive
- Suivi de progression détaillé
- Simulation de conditions proches des CTF réels
- Capitalisation des connaissances via les write-ups