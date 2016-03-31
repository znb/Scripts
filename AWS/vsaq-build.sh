#!/bin/bash
# Deployment script for VSAQ

VSAQDIR="/opt/vsaq"
VSAQSERVER="/opt/vsaq/vsaq_server.py"
VSAQGIT="https://github.com/google/vsaq.git"

echo ""
echo "[INFO] This will attempt to build and install VSAQ"
echo -n "Contiue ? (CTRL-C to exit)"
read CONT

echo "[INFO] Installing dependancies..."
apt-get update
apt-get install -qy language-pack-en git ant openjdk-7-jdk unzip

echo ""
echo "[INFO] Pulling VSAQ"
git clone ${VSAQGIT} ${VSAQDIR}
cd ${VSAQDIR}

echo ""
echo "[INFO] Installing MORE dependancies..."
./do.sh install_deps

echo ""
echo "[INFO] Building VSAQ"
./do.sh build

echo ""
echo "[INFO] Starting VSAQ"
sed -i 's/9000/80/' ${VSAQSERVER}
sed -i 's/127\.0\.0\.1/0\.0\.0\.0/' ${VSAQSERVER}
./do.sh run
