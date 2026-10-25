#!/bin/zsh
cd "${0:A:h}" || exit 1
source .venv/bin/activate
printf '\nTrusted agent lab\n\n'
python -m trusted_lab doctor
printf '\nRun a small live check: python -m trusted_lab smoke\nRun the pilot: python -m trusted_lab run\n\n'
exec /bin/zsh -i
