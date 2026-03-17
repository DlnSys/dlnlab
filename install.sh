#!/usr/bin/env bash
set -e

DLNLAB_DIR="/opt/dlnlab"

# ── Vérification des prérequis ────────────────────────────────────────────────
echo "[*] Vérification des prérequis..."

if ! command -v git &>/dev/null; then
    echo "[!] Git non trouvé. Installation..."
    sudo apt-get install -y git
fi

if ! command -v python3 &>/dev/null || ! python3 -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)"; then
    echo "[!] Python 3.10+ requis."
    echo "    Installe-le via : sudo apt-get install python3"
    exit 1
fi

if ! command -v pip3 &>/dev/null; then
    echo "[!] pip non trouvé. Installation..."
    sudo apt-get install -y python3-pip
fi

if ! command -v docker &>/dev/null; then
    echo "[!] Docker non trouvé. Installe Docker : https://docs.docker.com/engine/install/"
    exit 1
fi

if ! docker compose version &>/dev/null; then
    echo "[!] Docker Compose non trouvé. Installe Docker Compose plugin."
    exit 1
fi

echo "[+] Prérequis OK"

echo "[*] Clonage de DLNLab dans $DLNLAB_DIR..."
sudo git clone https://github.com/DlnSys/dlnlab.git "$DLNLAB_DIR"

echo "[*] Création du venv..."
sudo python3 -m venv "$DLNLAB_DIR/.venv"

echo "[*] Installation des dépendances..."
sudo "$DLNLAB_DIR/.venv/bin/pip" install -r "$DLNLAB_DIR/requirements.txt"

echo "[*] Permissions..."
sudo chmod +x "$DLNLAB_DIR/dlnlab"
sudo chown -R "$USER:$USER" "$DLNLAB_DIR"

echo "[*] Création du workspace..."
mkdir -p ~/dlnlab/workspace

echo "[*] Ajout de dlnlab au PATH..."

SHELL_RC="${ZDOTDIR:-$HOME}/.zshrc"

if [ ! -f "$SHELL_RC" ]; then
    SHELL_RC="$HOME/.bashrc"
    [ -f "$SHELL_RC" ] || touch "$SHELL_RC"
fi

if ! grep -q "$DLNLAB_DIR" "$SHELL_RC" 2>/dev/null; then
    echo "export PATH=\"\$PATH:$DLNLAB_DIR\"" >> "$SHELL_RC"
    echo "[+] PATH mis à jour dans $SHELL_RC"
else
    echo "[*] dlnlab déjà dans le PATH"
fi

echo ""
echo "[+] Installation terminée !"
echo "    Redémarre ton terminal ou tape : source $SHELL_RC"