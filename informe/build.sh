#!/usr/bin/env bash
# Regenera el informe desde triage/defects.json: secciones, diagramas, DOCX y PDF.
#   bash informe/build.sh
set -euo pipefail
cd "$(dirname "$0")"
python3 ../triage/triage.py validate
python3 ../triage/triage.py report
python3 ../triage/triage.py diagrams 2>/dev/null
SRC=(00_intro.md generado.md 90_propuesta.md)
NAME=Informe_Actividad5_Triage
/opt/homebrew/bin/pandoc "${SRC[@]}" --toc --toc-depth=1 --number-sections -o "$NAME.docx"
/opt/homebrew/bin/pandoc "${SRC[@]}" --toc --toc-depth=1 --number-sections --standalone --embed-resources \
  --css estilo.css --metadata title-prefix="" -o "$NAME.html"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf="$PWD/$NAME.pdf" "file://$PWD/$NAME.html" 2>/dev/null
rm -f "$NAME.html"
echo "Generados: $NAME.docx, $NAME.pdf"
