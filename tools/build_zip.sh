#!/bin/sh
# Builds the Claude.ai upload ZIP: the skill folder at the top level of the archive.
set -e
cd "$(dirname "$0")/../skills"
mkdir -p ../dist
rm -f ../dist/bd-income-tax-return-2026-27.zip
zip -qr ../dist/bd-income-tax-return-2026-27.zip bd-income-tax-return -x '*__pycache__*' '*.pyc'
echo "dist/bd-income-tax-return-2026-27.zip"
