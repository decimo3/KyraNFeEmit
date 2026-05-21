#!/bin/env bash

set -e

if [[ -z "$VIRTUAL_ENV" ]]; then
    source venv/Scripts/activate
fi

# DONE - Fetch tags and get the latest one
git fetch --tags
version=$(git describe --tags $(git rev-list --tags --max-count=1))
version_number="${version#v}"  # Remove 'v' prefix if the tag has it
echo "Version: $version_number"

# Extract major, minor, and patch versions
IFS='.' read -r MAJOR_VERSION MINOR_VERSION PATCH_VERSION <<< "$version_number"
export MAJOR_VERSION MINOR_VERSION PATCH_VERSION
echo "Major version: $MAJOR_VERSION"
echo "Minor version: $MINOR_VERSION"
echo "Patch version: $PATCH_VERSION"

# Write version file
envsubst < version_file.txt > version_file.tmp
mv version_file.tmp version_file.txt
cat version_file.txt

# Install dependencies
pip install -r requirements.txt

# Lint with pylint
#pylint src/nfe_bot.py

# Test with pytest
#pytest src/test_nfe_bot.py

# Build executable with pyinstaller
pyinstaller --icon nfe_bot.ico --version-file version_file.txt --collect-all selenium src/nfe_bot.py --noconfirm

# Restore files with sensible data
cp src/nfe_bot.conf src/nfe_bot.conf.bak
git restore src/nfe_bot.conf

# Compress executable and related files
zip -j nfe_bot.zip readme.md src/nfe_bot.conf src/nfe_bot.path src/ISS.xls src/Cota\ de\ Impostos\ Estruturados.xls src/Codes\ Complementares\ por\ Municipio.xls
cd dist/nfe_bot && zip -r ../../nfe_bot.zip . && cd ../..

# Create a release on GitHub
gh release create $version --verify-tag --notes-file release_notes.md --title "NFE_BOT ${version} release" nfe_bot.zip

# Reverting placeholder files
git restore version_file.txt

# Retrieve sensible data from files
rm src/nfe_bot.conf && mv src/nfe_bot.conf.bak src/nfe_bot.conf
