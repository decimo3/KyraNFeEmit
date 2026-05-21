# KyraNfeEmit

Program that automates the issuance of invoices on the Brazilian portal `EmissorNacional`.

The program performs the form filling by calculating the information in measurement spreadsheets, going through each step according to specific instructions. This program was not built for general use.

## Installation

The program is self-contained; it is only necessary to unzip the files in any location where it has free access, and after configuration, it will be ready to run.

## Development

It is necessary to have Python installed in the version specified in `.tools-version`.

```sh
# 1. Create and activate a virtual environment
python -m venv venv
source venv/Scripts/activate
# 2. Install the dependencies defined in `requirements.txt`
pip install -r requirements.txt
# 2. Or install the main packages directly
pip install python-dotenv xlrd pandas python-Levenshtein requests selenium pyinstaller
# 3. Develop, test and run
cd src
python nfe_bot.py
# 4. Publish and distribute with pyinstaller
./release.sh
```
