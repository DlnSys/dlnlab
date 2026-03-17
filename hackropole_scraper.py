#!/usr/bin/env python3
"""
hackropole_scraper.py — DLNLab V2

Scrape hackropole.fr et génère le catalogue DLNLab complet.

Structure générée :
  dlnlab/
    catalog/{category}/{name}.yml
    boxes/{name}/docker-compose.yml     (runtime docker/netcat)
    challenges/{category}/{name}/       (runtime file)

Usage :
  python hackropole_scraper.py [OPTIONS]

Options :
  --output-dir DIR    Racine du projet DLNLab (défaut: ./dlnlab)
  --category CAT      Filtrer : web, crypto, pwn, reverse, forensics, misc, hardware
  --difficulty DIFF   Filtrer : intro, star, starstar, starstarstar
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

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

BASE_URL = "https://hackropole.fr"
CHALLENGES_LIST_URL = f"{BASE_URL}/fr/challenges/"

# Difficulté Hackropole → DLNLab
DIFFICULTY_MAP = {
    "intro":       "easy",
    "star":        "medium",
    "starstar":    "hard",
    "starstarstar": "hard",
}

# Tag principal → catégorie dossier DLNLab
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
    if HAS_BS4:
        return _parselist_bs4(html)
    return _parselist_regex(html)


def _parselist_bs4(html: str) -> list[dict]:
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
        diff_raw = cells[2].get_text(strip=True).lower()
        fcsc_link = cells[3].find("a")
        fcsc = fcsc_link.get_text(strip=True) if fcsc_link else ""
        tags = [a.get_text(strip=True).lower() for a in cells[4].find_all("a")]
        results.append({
            "id":         challenge_id,
            "title":      title,
            "difficulty": diff_raw,
            "fcsc":       fcsc,
            "tags":       tags,
            "page_url":   full_href.rstrip("/") + "/",
        })
    return results


def _parselist_regex(html: str) -> list[dict]:
    results = []
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.DOTALL)
    for row in rows:
        cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.DOTALL)
        if len(cells) < 5:
            continue
        m = re.search(r'href="(/fr/challenges/(?:[^/"]+/)?([^/"]+)/)"', cells[1])
        if not m:
            continue
        href_rel, challenge_id = m.group(1), m.group(2)
        title    = re.sub(r"<[^>]+>", "", cells[1]).strip()
        diff_raw = re.sub(r"<[^>]+>", "", cells[2]).strip().lower()
        fcsc_m   = re.search(r">([^<]+)", cells[3])
        fcsc     = fcsc_m.group(1).strip() if fcsc_m else ""
        tags     = [t.lower() for t in re.findall(r">([^<]+)", cells[4])]
        results.append({
            "id":         challenge_id,
            "title":      title,
            "difficulty": diff_raw,
            "fcsc":       fcsc,
            "tags":       tags,
            "page_url":   BASE_URL + href_rel,
        })
    return results


# ── Parsing page individuelle ─────────────────────────────────────────────────

def parse_challenge_page(html: str) -> dict:
    """
    Extrait depuis la page HTML d'un challenge :
      - description
      - hash SHA256 du flag
      - liste des fichiers publics [(filename, url), ...]
      - compose_url (docker-compose)
      - runtime : docker / netcat / file
      - port exposé
    """
    info = {
        "description": "",
        "flag_hash":   "",
        "files":       [],
        "compose_url": None,
        "runtime":     "file",
        "port":        None,
    }

    if HAS_BS4:
        soup      = BeautifulSoup(html, "html.parser")
        full_text = soup.get_text(" ")

        # Description
        desc_tag = soup.find(["h2", "h3"], string=re.compile(r"description", re.I))
        if desc_tag:
            parts = []
            for sib in desc_tag.find_next_siblings():
                if sib.name and sib.name.startswith("h"):
                    break
                t = sib.get_text(" ", strip=True)
                if t:
                    parts.append(t)
            info["description"] = " ".join(parts).strip()

        # Hash SHA256 du flag
        for code in soup.find_all("code"):
            m = re.search(r"possible output:\s*([a-f0-9]{64})", code.get_text())
            if m:
                info["flag_hash"] = m.group(1)
                break

        # Fichiers publics (section "Files")
        files_tag = soup.find(["h2", "h3"], string=re.compile(r"^files?$", re.I))
        if files_tag:
            ul = files_tag.find_next("ul")
            if ul:
                for a in ul.find_all("a"):
                    href = a.get("href", "")
                    if not href:
                        continue
                    url      = href if href.startswith("http") else BASE_URL + href
                    filename = a.get_text(strip=True) or url.split("/")[-1]
                    if "docker-compose" not in filename:
                        info["files"].append((filename, url))

        # docker-compose URL
        m = re.search(
            r"curl (https://hackropole\.fr/challenges/[^\s]+/docker-compose\.public\.yml)",
            full_text,
        )
        if m:
            info["compose_url"] = m.group(1)

        # Port
        m_port = re.search(r"http://localhost:(\d{2,5})", full_text)
        if m_port:
            info["port"] = int(m_port.group(1))
        else:
            m_nc = re.search(r"nc localhost (\d{2,5})", full_text)
            if m_nc:
                info["port"] = int(m_nc.group(1))

        # Runtime
        if info["compose_url"]:
            if "nc localhost" in full_text or "netcat" in full_text.lower():
                info["runtime"] = "netcat"
            else:
                info["runtime"] = "docker"
        elif info["files"]:
            info["runtime"] = "file"

    else:
        # Fallback regex
        m = re.search(r"possible output:\s*([a-f0-9]{64})", html)
        if m:
            info["flag_hash"] = m.group(1)

        m = re.search(
            r"curl (https://hackropole\.fr/challenges/[^\s]+/docker-compose\.public\.yml)",
            html,
        )
        if m:
            info["compose_url"] = m.group(1)
            info["runtime"] = "netcat" if "nc localhost" in html else "docker"

        m_port = re.search(r"http://localhost:(\d{2,5})", html)
        if m_port:
            info["port"] = int(m_port.group(1))
        else:
            m_nc = re.search(r"nc localhost (\d{2,5})", html)
            if m_nc:
                info["port"] = int(m_nc.group(1))

        for m in re.finditer(
            r'href="(https://hackropole\.fr/challenges/[^"]+/public/([^"]+))"',
            html,
        ):
            info["files"].append((m.group(2), m.group(1)))
        if info["files"]:
            info["runtime"] = "file"

    return info


# ── Helpers ───────────────────────────────────────────────────────────────────

def get_category(tags: list[str]) -> str:
    for tag in tags:
        if tag in CATEGORY_MAP:
            return CATEGORY_MAP[tag]
    return "misc"


def normalize_difficulty(raw: str) -> str:
    raw = raw.lower().strip()
    for key, val in DIFFICULTY_MAP.items():
        if key in raw:
            return val
    return "medium"


def make_name(challenge_id: str) -> str:
    """fcsc2020-web-babel-web → hackropole_babel_web"""
    name = re.sub(r"fcsc\d{4}-[a-z]+-", "", challenge_id)
    if name == challenge_id:
        name = re.sub(r"fcsc\d{4}-", "", challenge_id)
    return f"hackropole_{name.replace('-', '_')}"


def build_yaml(chall: dict, page: dict, name: str, category: str) -> dict:
    theme = chall["tags"][0] if chall["tags"] else category

    data = {
        "name":        name,
        "source":      "hackropole",
        "url":         chall["page_url"],
        "theme":       theme,
        "category":    category,
        "difficulty":  normalize_difficulty(chall["difficulty"]),
        "description": page["description"] or f"Challenge {chall['title']} — {chall['fcsc']}",
        "runtime":     page["runtime"],
    }

    if page["runtime"] in ("docker", "netcat"):
        data["compose"] = "docker-compose.yml"
        if page["port"]:
            data["port"] = page["port"]
        if page["runtime"] == "netcat":
            data["host"] = "127.0.0.1"
    elif page["runtime"] == "file":
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
    parser.add_argument("--output-dir",  default="./dlnlab")
    parser.add_argument("--category",    default=None)
    parser.add_argument("--difficulty",  default=None)
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

    # ── 2. Filtres ────────────────────────────────────────────────────────────
    if args.category:
        cat = args.category.lower()
        challenges = [c for c in challenges if cat in c["tags"]]
        print(f"[*] Filtre '{cat}' → {len(challenges)} challenges")

    if args.difficulty:
        diff = args.difficulty.lower()
        challenges = [c for c in challenges if diff in c["difficulty"]]
        print(f"[*] Filtre difficulté '{diff}' → {len(challenges)} challenges")

    if args.limit:
        challenges = challenges[: args.limit]
        print(f"[*] Limité à {args.limit} challenges")

    # ── 3. Traitement ─────────────────────────────────────────────────────────
    stats = {"docker": 0, "netcat": 0, "file": 0, "skip": 0, "error": 0}

    for i, chall in enumerate(challenges, 1):
        name      = make_name(chall["id"])
        category  = get_category(chall["tags"])

        print(f"\n[{i:3}/{len(challenges)}] {chall['title']}")
        print(f"  cat={category}  diff={chall['difficulty']}")

        catalog_dir    = root / "catalog" / category
        boxes_dir      = root / "boxes" / name
        challenges_dir = root / "challenges" / category / name

        if args.dry_run:
            print(f"  [dry-run] → catalog/{category}/{name}.yml")
            stats["skip"] += 1
            continue

        # Skip si déjà fait
        yaml_path = catalog_dir / f"{name}.yml"
        if yaml_path.exists():
            print(f"  déjà présent, skip")
            stats["skip"] += 1
            time.sleep(args.delay)
            continue

        # Fetch page
        page_html = fetch(chall["page_url"], delay=args.delay)
        if not page_html:
            alt_url   = f"{BASE_URL}/fr/challenges/{chall['id']}/"
            page_html = fetch(alt_url, delay=args.delay)

        if not page_html:
            print(f"  [!] Page inaccessible, skip")
            stats["error"] += 1
            time.sleep(args.delay)
            continue

        page     = parse_challenge_page(page_html)
        flag_ok  = "✓" if page["flag_hash"] else "✗"
        print(f"  runtime={page['runtime']}  port={page['port']}  "
              f"files={len(page['files'])}  flag={flag_ok}")

        # ── Téléchargements ───────────────────────────────────────────────────
        if page["runtime"] in ("docker", "netcat") and page["compose_url"]:
            boxes_dir.mkdir(parents=True, exist_ok=True)
            dest = boxes_dir / "docker-compose.yml"
            if not dest.exists():
                ok = download_binary(page["compose_url"], dest)
                print(f"  boxes/{name}/docker-compose.yml → {'✓' if ok else '✗'}")
            else:
                print(f"  docker-compose déjà présent")

        elif page["runtime"] == "file" and page["files"]:
            challenges_dir.mkdir(parents=True, exist_ok=True)
            for filename, url in page["files"]:
                dest = challenges_dir / filename
                if not dest.exists():
                    ok = download_binary(url, dest)
                    print(f"  challenges/{category}/{name}/{filename} → {'✓' if ok else '✗'}")
                else:
                    print(f"  {filename} déjà présent")

        # ── Écriture YAML ─────────────────────────────────────────────────────
        catalog_dir.mkdir(parents=True, exist_ok=True)
        yaml_data = build_yaml(chall, page, name, category)

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
