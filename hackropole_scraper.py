#!/usr/bin/env python3
"""
hackropole_scraper.py — DLNLab V2

Scrape hackropole.fr et génère le catalogue DLNLab complet.

Structure générée :
  <output-dir>/
    catalog/{category}/{name}.yml
    boxes/{name}/docker-compose.yml     (runtime docker/netcat)
    challenges/{category}/{name}/       (fichiers statiques)

Usage :
  python hackropole_scraper.py [OPTIONS]

Options :
  --output-dir DIR    Racine du projet DLNLab (défaut: .)
  --category CAT      Filtrer : web, crypto, pwn, reverse, forensics, misc, hardware
  --difficulty DIFF   Filtrer : easy, medium, hard
  --limit N           Limiter à N challenges (test)
  --dry-run           Affiche sans télécharger ni écrire
  --delay FLOAT       Pause entre requêtes en secondes (défaut: 0.5)

Dépendances :
  pip install pyyaml beautifulsoup4
"""

import argparse
import re
import time
import urllib.request
import urllib.error
from pathlib import Path

import yaml
from bs4 import BeautifulSoup

BASE_URL = "https://hackropole.fr"
CHALLENGES_LIST_URL = f"{BASE_URL}/fr/challenges/"

CATEGORY_MAP = {
    "web":       "web",
    "crypto":    "crypto",
    "pwn":       "pwn",
    "reverse":   "reverse",
    "forensics": "forensics",
    "misc":      "misc",
    "hardware":  "hardware",
    "algo":      "misc",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (DLNLab-Scraper/2.0; +https://dlnsys.ovh)",
}


# ── Réseau ────────────────────────────────────────────────────────────────────

def fetch(url: str, retries: int = 3, delay: float = 1.0) -> str | None:
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=20) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if attempt < retries - 1:
                time.sleep(delay * (attempt + 1))
            else:
                return None
        except Exception:
            if attempt < retries - 1:
                time.sleep(delay * (attempt + 1))
            else:
                return None
    return None


def download_binary(url: str, dest: Path, retries: int = 3) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as resp:
                dest.write_bytes(resp.read())
            return True
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return False
            if attempt < retries - 1:
                time.sleep(1)
        except Exception:
            if attempt < retries - 1:
                time.sleep(1)
    return False


# ── Parsing liste des challenges ──────────────────────────────────────────────

def parse_challenge_list(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    results = []
    for row in soup.select("table tr"):
        cells = row.find_all("td")
        if len(cells) < 5:
            continue
        link = cells[1].find("a")
        if not link:
            continue
        title = link.get_text(strip=True)
        href = link.get("href", "")
        m = re.search(r"/challenges/(?:[^/]+/)?([^/]+)/?$", href)
        if not m:
            continue
        challenge_id = m.group(1)
        full_href = href if href.startswith("http") else BASE_URL + href
        fcsc_link = cells[3].find("a")
        fcsc = fcsc_link.get_text(strip=True) if fcsc_link else ""
        tags = [a.get_text(strip=True).lower() for a in cells[4].find_all("a")]
        results.append({
            "id":       challenge_id,
            "title":    title,
            "fcsc":     fcsc,
            "tags":     tags,
            "page_url": full_href.rstrip("/") + "/",
        })
    return results


# ── Parsing page individuelle ─────────────────────────────────────────────────

def count_stars(soup) -> int:
    """Compte les éléments SVG #star-fill pour déterminer la difficulté."""
    count = 0
    for use in soup.find_all("use"):
        href = use.get("href", "") or use.get("xlink:href", "")
        if "#star-fill" in href:
            count += 1
    return count


def stars_to_difficulty(n: int) -> str:
    if n <= 1:
        return "easy"
    elif n == 2:
        return "medium"
    else:
        return "hard"


def parse_challenge_page(html: str) -> dict:
    """
    Extrait depuis la page HTML d'un challenge :
      - description   : paragraphes du div .col-md-8.markdown
      - difficulty    : comptage #star-fill SVG
      - flag_hash     : attribut data-flags-hash sur l'input
      - files         : section "Fichiers" (français)
      - compose_url   : lien <a href="...docker-compose.public.yml">
      - runtime       : docker / netcat / file
      - port          : port exposé
    """
    info = {
        "description": "",
        "difficulty":  "easy",
        "flag_hash":   "",
        "files":       [],
        "compose_url": None,
        "runtime":     "file",
        "port":        None,
    }

    soup = BeautifulSoup(html, "html.parser")
    full_text = soup.get_text(" ")

    # Difficulté via comptage #star-fill
    n_stars = count_stars(soup)
    info["difficulty"] = stars_to_difficulty(n_stars)

    # Description : tous les <p> du div .col-md-8.markdown
    desc_div = soup.find("div", class_=lambda c: c and "col-md-8" in c and "markdown" in c)
    if desc_div:
        paragraphs = [p.get_text(" ", strip=True) for p in desc_div.find_all("p")]
        info["description"] = "\n".join(p for p in paragraphs if p)

    # Flag hash via attribut data-flags-hash
    flag_input = soup.find(attrs={"data-flags-hash": True})
    if flag_input:
        info["flag_hash"] = flag_input.get("data-flags-hash", "")

    # docker-compose URL via lien <a href="...docker-compose.public.yml">
    compose_link = soup.find("a", href=re.compile(r"docker-compose\.public\.yml"))
    if compose_link:
        href = compose_link.get("href", "")
        info["compose_url"] = href if href.startswith("http") else BASE_URL + href

    # Fichiers statiques : section "Fichiers" (français)
    files_tag = next(
        (tag for tag in soup.find_all(["h2", "h3"])
         if re.search(r"fichiers?", tag.get_text(), re.I)),
        None
    )
    if files_tag:
        ul = files_tag.find_next("ul")
        if ul:
            for a in ul.find_all("a"):
                href = a.get("href", "")
                if not href or "docker-compose" in href:
                    continue
                url = href if href.startswith("http") else BASE_URL + href
                filename = a.get_text(strip=True) or url.split("/")[-1]
                info["files"].append((filename, url))

    # Port exposé
    m_port = re.search(r"http://localhost:(\d{2,5})", full_text)
    if m_port:
        info["port"] = int(m_port.group(1))
    else:
        m_nc = re.search(r"nc localhost (\d{2,5})", full_text)
        if m_nc:
            info["port"] = int(m_nc.group(1))

    # Runtime : priorité au compose, sinon file
    if info["compose_url"]:
        if "nc localhost" in full_text or "netcat" in full_text.lower():
            info["runtime"] = "netcat"
        else:
            info["runtime"] = "docker"
    elif info["files"]:
        info["runtime"] = "file"

    return info


# ── Helpers ───────────────────────────────────────────────────────────────────

def get_category(tags: list[str]) -> str:
    for tag in tags:
        if tag in CATEGORY_MAP:
            return CATEGORY_MAP[tag]
    return "misc"


def make_name(challenge_id: str) -> str:
    """fcsc2020-web-babel-web → babel_web"""
    name = re.sub(r"fcsc\d{4}-[a-z]+-", "", challenge_id)
    if name == challenge_id:
        name = re.sub(r"fcsc\d{4}-", "", challenge_id)
    return name.replace("-", "_")


def get_service_name(compose_path: Path) -> str | None:
    """Lit le docker-compose.yml et retourne le premier nom de service."""
    try:
        with open(compose_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        services = data.get("services", {})
        if services:
            return next(iter(services))
    except Exception:
        pass
    return None


def build_yaml(chall: dict, page: dict, name: str, category: str, service: str | None) -> dict:
    theme = next((t for t in chall["tags"] if t), category)

    data = {
        "name":        name,
        "source":      "hackropole",
        "url":         chall["page_url"],
        "theme":       theme,
        "category":    category,
        "difficulty":  page["difficulty"],
        "description": page["description"] or f"Challenge {chall['title']} — {chall['fcsc']}",
        "runtime":     page["runtime"],
    }

    if page["compose_url"]:
        data["compose"] = "docker-compose.yml"
        if service:
            data["service"] = service
        if page["port"]:
            data["port"] = page["port"]
        if page["runtime"] == "netcat":
            data["host"] = "127.0.0.1"

    # Fichiers statiques — indépendant du runtime (runtime mixte supporté)
    if page["files"]:
        filenames = [fn for fn, _ in page["files"]]
        data["file"] = filenames[0] if len(filenames) == 1 else filenames

    data["flag"] = {
        "format": "FCSC{...}",
        "value":  page["flag_hash"] or "TODO",
    }
    if not page["flag_hash"]:
        data["needs_review"] = True

    data["writeup"] = f"writeups/{name}.md"
    data["enabled"] = True

    return data


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Hackropole → DLNLab V2 scraper")
    parser.add_argument("--output-dir",  default=".")
    parser.add_argument("--category",    default=None, help="web, crypto, pwn, reverse, forensics, misc")
    parser.add_argument("--exclude",     default=None, help="Catégorie à exclure : web, crypto, pwn, reverse, forensics, misc")
    parser.add_argument("--difficulty",  default=None, help="easy, medium, hard")
    parser.add_argument("--limit",       type=int,   default=None)
    parser.add_argument("--dry-run",     action="store_true")
    parser.add_argument("--delay",       type=float, default=0.5)
    args = parser.parse_args()

    root = Path(args.output_dir)

    # ── 1. Liste ──────────────────────────────────────────────────────────────
    print("[*] Récupération de la liste des challenges...")
    html = fetch(CHALLENGES_LIST_URL)
    if not html:
        print("[!] Impossible de récupérer la liste.")
        return 1

    challenges = parse_challenge_list(html)
    print(f"[+] {len(challenges)} challenges trouvés")

    # ── 2. Filtre catégorie (sur les tags de la liste) ─────────────────────
    if args.category:
        cat = args.category.lower()
        challenges = [c for c in challenges if cat in c["tags"]]
        print(f"[*] Filtre '{cat}' → {len(challenges)} challenges")

    if args.exclude:
        excl = args.exclude.lower()
        challenges = [c for c in challenges if excl not in c["tags"]]
        print(f"[*] Exclusion '{excl}' → {len(challenges)} challenges")

    if args.limit:
        challenges = challenges[: args.limit]
        print(f"[*] Limité à {args.limit} challenges")

    # ── 3. Traitement ─────────────────────────────────────────────────────────
    stats = {"docker": 0, "netcat": 0, "file": 0, "skip": 0, "error": 0}

    for i, chall in enumerate(challenges, 1):
        name     = make_name(chall["id"])
        category = get_category(chall["tags"])

        print(f"\n[{i:3}/{len(challenges)}] {chall['title']}  →  {name}")
        print(f"  cat={category}")

        catalog_dir    = root / "catalog" / category
        boxes_dir      = root / "boxes" / name
        challenges_dir = root / "challenges" / category / name

        if args.dry_run:
            print(f"  [dry-run] catalog/{category}/{name}.yml")
            stats["skip"] += 1
            continue

        # Skip si déjà traité
        yaml_path = catalog_dir / f"{name}.yml"
        if yaml_path.exists():
            print(f"  déjà présent, skip")
            stats["skip"] += 1
            time.sleep(args.delay)
            continue

        # Fetch page individuelle
        page_html = fetch(chall["page_url"], delay=args.delay)
        if not page_html:
            print(f"  [!] Page inaccessible, skip")
            stats["error"] += 1
            time.sleep(args.delay)
            continue

        page = parse_challenge_page(page_html)

        # Filtre difficulté (après parsing de la page via les étoiles)
        if args.difficulty and page["difficulty"] != args.difficulty.lower():
            print(f"  skip (difficulté={page['difficulty']})")
            stats["skip"] += 1
            time.sleep(args.delay)
            continue

        flag_ok = "✓" if page["flag_hash"] else "✗"
        print(f"  runtime={page['runtime']}  difficulty={page['difficulty']}  "
              f"port={page['port']}  files={len(page['files'])}  flag={flag_ok}")

        # ── Téléchargements ───────────────────────────────────────────────────
        service = None

        # Docker-compose (docker ou netcat)
        if page["compose_url"]:
            boxes_dir.mkdir(parents=True, exist_ok=True)
            dest = boxes_dir / "docker-compose.yml"
            if not dest.exists():
                ok = download_binary(page["compose_url"], dest)
                print(f"  boxes/{name}/docker-compose.yml → {'✓' if ok else '✗'}")
            else:
                print(f"  docker-compose déjà présent")
            service = get_service_name(boxes_dir / "docker-compose.yml")

        # Fichiers statiques — indépendant du compose (runtime mixte)
        if page["files"]:
            for filename, url in page["files"]:
                dest = challenges_dir / filename
                if not dest.exists():
                    ok = download_binary(url, dest)
                    print(f"  challenges/{category}/{name}/{filename} → {'✓' if ok else '✗'}")
                else:
                    print(f"  {filename} déjà présent")

        # ── Écriture YAML ─────────────────────────────────────────────────────
        catalog_dir.mkdir(parents=True, exist_ok=True)
        yaml_data = build_yaml(chall, page, name, category, service)

        with open(yaml_path, "w", encoding="utf-8") as f:
            yaml.dump(
                yaml_data, f,
                allow_unicode=True,
                default_flow_style=False,
                sort_keys=False,
                width=120,
            )
        print(f"  catalog/{category}/{name}.yml ✓")
        stats[page["runtime"]] += 1

        time.sleep(args.delay)

    # ── Résumé ────────────────────────────────────────────────────────────────
    total = stats["docker"] + stats["netcat"] + stats["file"]
    print("\n" + "=" * 50)
    print(f"  Total traités  : {total}")
    print(f"  Docker         : {stats['docker']}")
    print(f"  Netcat         : {stats['netcat']}")
    print(f"  File           : {stats['file']}")
    print(f"  Erreurs        : {stats['error']}")
    print(f"  Skippés        : {stats['skip']}")
    print(f"  Output         : {root.resolve()}")
    print("=" * 50)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
