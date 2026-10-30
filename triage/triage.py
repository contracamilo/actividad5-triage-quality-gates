#!/usr/bin/env python3
"""Herramienta de triage de la Actividad 5.

Una sola fuente de datos (defects.json) alimenta el acta, el análisis causa raíz,
el plan de mejora, el informe y el gate del pipeline.

Uso:
    python3 triage/triage.py validate   # completitud contra la rúbrica
    python3 triage/triage.py gate       # quality gate G1 (exit 1 si bloquea)
    python3 triage/triage.py report     # genera informe/generado.md
    python3 triage/triage.py diagrams   # genera informe/img/*.png (requiere matplotlib)
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "triage" / "defects.json"
REGRESSION_SPEC = ROOT / "app" / "tests" / "regression.spec.js"
INFORME = ROOT / "informe"

SEVERIDADES = ["Crítica", "Alta", "Media", "Baja"]
PRIORIDADES = ["P1", "P2", "P3", "P4"]
NIVEL = {"Alto": 3, "Medio": 2, "Bajo": 1}
ESTADO = {"resolved": "Resuelto", "open": "Abierto"}


def load():
    return json.loads(DATA.read_text(encoding="utf-8"))


def regression_ids():
    """Códigos D-00X que tienen al menos un caso en regression.spec.js."""
    if not REGRESSION_SPEC.exists():
        return set()
    return set(re.findall(r"""it\(\s*['"](D-\d{3})""", REGRESSION_SPEC.read_text(encoding="utf-8")))


def prioridad_matriz(impacto, urgencia):
    """Matriz impacto × urgencia de clase (importante/urgente)."""
    importante, urgente = impacto >= 4, urgencia >= 4
    if importante and urgente:
        return "P1"
    if importante:
        return "P2"
    if urgente:
        return "P3"
    return "P4"


def cuadrante(accion):
    imp, esf = NIVEL[accion["impacto"]], NIVEL[accion["esfuerzo"]]
    if imp >= 2 and esf == 1:
        return 1, "Quick win (impacto alto/medio, esfuerzo bajo)"
    if imp >= 2:
        return 2, "Proyecto planificado (impacto alto/medio, esfuerzo medio/alto)"
    if esf == 1:
        return 3, "Mejora rápida si hay capacidad"
    return 4, "Baja prioridad"


# ---------------------------------------------------------------- validate
def cmd_validate(data):
    errores = []
    defectos = data["defectos"]
    if len(defectos) < 3:
        errores.append(f"Se requieren ≥ 3 defectos (hay {len(defectos)})")
    if not data["sesion"].get("asistentes"):
        errores.append("El acta no registra asistentes")
    gate_ids = {g["id"] for g in data["gates"]}

    for d in defectos:
        did = d["id"]
        t = d.get("triage", {})
        for campo in ("severidad", "prioridad", "responsable", "decision", "fecha_compromiso", "criterio_cierre", "justificacion"):
            if not t.get(campo):
                errores.append(f"{did}: falta triage.{campo}")
        if t.get("severidad") not in SEVERIDADES:
            errores.append(f"{did}: severidad fuera de escala")
        if t.get("prioridad") not in PRIORIDADES:
            errores.append(f"{did}: prioridad fuera de escala")
        if not d.get("evidencia"):
            errores.append(f"{did}: sin evidencia")
        for ev in d.get("evidencia", []):
            ref = ev["ref"].split(" ")[0].split(":")[0]
            if ref.startswith(("triage/", "app/")) and not (ROOT / ref).exists():
                errores.append(f"{did}: evidencia no encontrada {ref}")
        if len(d.get("cinco_porques", [])) != 5:
            errores.append(f"{did}: los 5 porqués deben tener 5 niveles")
        if not d.get("causa_raiz"):
            errores.append(f"{did}: falta causa raíz")
        cats = d.get("ishikawa", {})
        if len(cats) < 3:
            errores.append(f"{did}: Ishikawa con menos de 3 categorías")
        tipos = {c["tipo"] for causas in cats.values() for c in causas}
        if "verificada" not in tipos:
            errores.append(f"{did}: Ishikawa sin causas verificadas")
        if not d.get("acciones"):
            errores.append(f"{did}: sin acciones de mejora")
        for a in d.get("acciones", []):
            for campo in ("responsable", "esfuerzo", "impacto", "kpi", "umbral", "plazo"):
                if not a.get(campo):
                    errores.append(f"{did}/{a['id']}: falta {campo}")
            if a.get("gate") and a["gate"] not in gate_ids:
                errores.append(f"{did}/{a['id']}: gate {a['gate']} no definido")

    if errores:
        print("VALIDACIÓN: FALLA")
        for e in errores:
            print("  -", e)
        return 1
    n_acc = sum(len(d["acciones"]) for d in defectos)
    print(f"VALIDACIÓN: OK — {len(defectos)} defectos, {n_acc} acciones, {len(data['gates'])} gates")
    return 0


# -------------------------------------------------------------------- gate
def cmd_gate(data):
    tests = regression_ids()
    bloqueos = []
    print("G1 — Gate de triage")
    print(f"{'Defecto':8} {'Sev.':8} {'Prio.':6} {'Estado':10} Prueba")
    for d in data["defectos"]:
        t = d["triage"]
        tiene = d["regression_test"] in tests
        print(f"{d['id']:8} {t['severidad']:8} {t['prioridad']:6} {d['status']:10} {'sí' if tiene else 'no'}")
        if t["prioridad"] == "P1" and d["status"] != "resolved":
            bloqueos.append(f"{d['id']} es P1 y está '{d['status']}' (debe estar resuelto antes de desplegar)")
        if d["status"] == "resolved" and not tiene:
            bloqueos.append(f"{d['id']} figura resuelto pero no tiene prueba '{d['regression_test']}' en regression.spec.js")
    if bloqueos:
        print("\nRESULTADO: BLOQUEADO")
        for b in bloqueos:
            print("  ✗", b)
        return 1
    print("\nRESULTADO: APROBADO — sin P1 abiertos y todos los resueltos tienen prueba de regresión")
    return 0


# ------------------------------------------------------------------ report
def tabla(headers, rows, widths=None):
    """Tabla Markdown; widths (pesos relativos) controla el ancho de columna en DOCX/PDF."""
    widths = widths or [1] * len(headers)
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("-" * (w * 6) for w in widths) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c).replace("|", "\\|").replace("\n", " ") for c in r) + " |")
    return "\n".join(out)


def cmd_report(data):
    s = data["sesion"]
    defs = data["defectos"]
    md = []

    md.append("# Los defectos que llevamos al triage\n")
    md.append("No inventamos defectos para esta actividad. Usamos los que encontramos al ejecutar el Master Test Plan "
              "de la Actividad 2, cada uno con su evidencia curl. Les pusimos un código nuevo (D-001 a D-005) que se "
              "repite en el acta, en el análisis, en el plan y en el nombre de las pruebas del pipeline, para poder "
              "seguir cada defecto de principio a fin. Las referencias `archivo:línea` son del código original "
              "(commit `02c4ced`).\n")
    md.append(tabla(["Código", "Origen", "Qué pasa", "Evidencia"],
                    [[d["id"], d["origen"].replace(" (Actividad 2)", ""), d["titulo"], f"`{d['evidencia'][0]['ref']}`"] for d in defs],
                    [1, 2, 6, 4]))
    md.append("")

    md.append("# Acta de triage\n")
    nombres = " y ".join(a["nombre"] for a in s["asistentes"])
    md.append(f"Hicimos la sesión el {s['fecha']} ({s['modalidad'].lower()}). Asistimos {nombres}. "
              f"{s['asistentes'][0]['nombre'].split()[0]} moderó y {s['asistentes'][1]['nombre'].split()[0]} llevó el registro.\n")
    md.append("Para decidir separamos dos preguntas. La severidad responde a qué tan grave es el daño (seguridad, datos, "
              "operación) y la prioridad a qué tan pronto hay que actuar. Para la prioridad usamos la matriz "
              "impacto × urgencia de clase y tuvimos en cuenta si había workaround, la reproducibilidad y el esfuerzo. "
              "Acordamos también que ningún defecto se cierra sin su prueba de regresión `D-00X` en verde dentro del pipeline.\n")
    md.append(tabla(["Escala", "Significado"],
                    [[k, v] for k, v in s["escala_severidad"].items()] + [[k, v] for k, v in s["escala_prioridad"].items()],
                    [1, 8]))
    md.append("\n**Decisiones**\n")
    md.append(tabla(["Código", "Sev.", "Prio.", "Responsable", "Decisión", "Fecha compromiso"],
                    [[d["id"], d["triage"]["severidad"], d["triage"]["prioridad"], d["triage"]["responsable"],
                      d["triage"]["decision"], d["triage"]["fecha_compromiso"]] for d in defs],
                    [1, 1, 1, 3, 5, 2]))
    md.append("\n**Por qué decidimos así**\n")
    for d in defs:
        t = d["triage"]
        md.append(f"- **{d['id']} {t['severidad']}/{t['prioridad']}.** {t['justificacion']} "
                  f"Workaround: {t['workaround'][0].lower() + t['workaround'][1:]}")
    md.append("\n**Otras cosas que salieron en la sesión**\n")
    for h in s["hallazgos_de_la_sesion"]:
        md.append(f"- {h}")
    md.append("")

    md.append("# Análisis de causa raíz\n")
    md.append("Para cada defecto hicimos los 5 porqués, que sirven para bajar hasta la causa, y un diagrama de Ishikawa, "
              "que sirve para ver qué otras causas aportaron. En los diagramas marcamos con ✔ las causas que pudimos "
              "comprobar con código, logs o pruebas, y con ? las que todavía son suposiciones. Tratamos de no culpar a "
              "nadie: buscamos qué falló en el proceso.\n")
    for d in defs:
        md.append(f"## {d['id']}: {d['titulo']}\n")
        for i, w in enumerate(d["cinco_porques"]):
            md.append(f"{i + 1}. {w['respuesta']}")
        md.append(f"\n**Causa raíz:** {d['causa_raiz']}\n")
        evid = []
        for causas in d["ishikawa"].values():
            for c in causas:
                if c["tipo"] == "verificada" and c["evidencia"] not in evid:
                    evid.append(c["evidencia"])
        md.append(f"**Evidencia de las causas verificadas:** {'; '.join(evid[:3])}.\n")
        md.append(f"![Ishikawa {d['id']}](img/ishikawa_{d['id']}.png){{width=72%}}\n")

    md.append("# Plan de mejora\n")
    md.append("Ubicamos cada acción en la matriz impacto/esfuerzo. Primero van los quick wins (mucho impacto, poco "
              "esfuerzo) y después lo que hay que planear con más tiempo. Cada acción tiene un KPI con su umbral y, "
              "cuando se puede, un gate del pipeline que lo revisa solo.\n")
    md.append("![Matriz impacto/esfuerzo](img/matriz_impacto_esfuerzo.png){width=60%}\n")
    acciones = [(cuadrante(a), d["id"], a) for d in defs for a in d["acciones"]]
    acciones.sort(key=lambda x: (x[0][0], -NIVEL[x[2]["impacto"]], x[2]["plazo"]))
    md.append(tabla(["#", "Acción", "Def.", "Responsable", "Imp./Esf.", "Plazo", "KPI → umbral", "Gate"],
                    [[i + 1, f"**{a['id']}** {a['accion']}", did, a["responsable"].split(" (")[0],
                      f"{a['impacto']}/{a['esfuerzo']}", a["plazo"], f"{a['kpi']} → {a['umbral']}", a["gate"] or "—"]
                     for i, (q, did, a) in enumerate(acciones)],
                    [1, 9, 2, 3, 2, 2, 6, 1]))
    md.append("")

    md.append("# Quality gates\n")
    md.append("Cada gate convierte un criterio de cierre o un KPI en una regla que el pipeline revisa en cada cambio. "
              "Van ordenados de lo más barato a lo más caro, y si uno falla los siguientes no corren.\n")
    md.append(tabla(["Gate", "Qué revisa", "Umbral", "Herramienta"],
                    [[f"**{g['id']}** {g['nombre']}", g["mide"], g["umbral"], g["herramienta"]] for g in data["gates"]],
                    [3, 5, 5, 4]))
    md.append("\n**Trazabilidad**\n")
    gates_por_def = {d["id"]: sorted({g["id"] for g in data["gates"] if d["id"] in g["previene"]}) for d in defs}
    md.append(tabla(["Defecto", "Acciones", "Prueba", "Gates", "Estado"],
                    [[d["id"], ", ".join(a["id"] for a in d["acciones"]), f"`{d['regression_test']} …`",
                      ", ".join(gates_por_def[d["id"]]),
                      ESTADO.get(d["status"], d["status"]) + (f" ({d['fecha_cierre']})" if d.get("fecha_cierre") else "")]
                     for d in defs]))
    md.append("")

    INFORME.mkdir(exist_ok=True)
    out = INFORME / "generado.md"
    out.write_text("\n".join(md), encoding="utf-8")
    print(f"Informe generado: {out.relative_to(ROOT)}")
    return 0


# ---------------------------------------------------------------- diagrams
def cmd_diagrams(data):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import textwrap

    img = INFORME / "img"
    img.mkdir(parents=True, exist_ok=True)

    for d in data["defectos"]:
        cats = list(d["ishikawa"].items())
        fig, ax = plt.subplots(figsize=(14, 7.5))
        ax.set_xlim(0, 14)
        ax.set_ylim(0, 7.5)
        ax.axis("off")
        spine_y, head_x = 3.75, 10.6
        ax.annotate("", xy=(head_x, spine_y), xytext=(0.4, spine_y),
                    arrowprops=dict(arrowstyle="-|>", lw=2.5, color="#333"))
        ax.text(head_x + 0.15, spine_y, "\n".join(textwrap.wrap(f"{d['id']}: {d['titulo']}", 26)),
                va="center", ha="left", fontsize=10, weight="bold",
                bbox=dict(boxstyle="round,pad=0.5", fc="#fde2e1", ec="#c0392b"))
        top = cats[0::2]
        bottom = cats[1::2]
        for row, sign in ((top, 1), (bottom, -1)):
            n = max(len(row), 1)
            for i, (cat, causas) in enumerate(row):
                x_end = 1.4 + (i + 1) * (9.0 / (n + 0.4))
                x_start, y_start = x_end - 1.6, spine_y + sign * 3.1
                ax.plot([x_start, x_end], [y_start, spine_y], color="#555", lw=1.6)
                ax.text(x_start, y_start + sign * 0.25, cat, ha="center", va="center", fontsize=10, weight="bold",
                        bbox=dict(boxstyle="round,pad=0.3", fc="#dbe9f6", ec="#2c6fad"))
                for j, c in enumerate(causas[:3]):
                    frac = 0.25 + j * 0.27
                    cx = x_start + (x_end - x_start) * frac
                    cy = y_start + (spine_y - y_start) * frac
                    marca = "✔" if c["tipo"] == "verificada" else "?"
                    color = "#1e7b34" if c["tipo"] == "verificada" else "#b9770e"
                    ax.text(cx - 0.12, cy, f"{marca} " + "\n".join(textwrap.wrap(c["causa"], 30)),
                            ha="right", va="center", fontsize=7.2, color=color)
        ax.text(0.4, 0.15, "✔ causa verificada   ? suposición por validar", fontsize=8, color="#555")
        fig.tight_layout()
        fig.savefig(img / f"ishikawa_{d['id']}.png", dpi=150)
        plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.axhline(2, color="#999", lw=1)
    ax.axvline(2, color="#999", lw=1)
    ax.set_xlim(0.5, 3.5)
    ax.set_ylim(0.5, 3.5)
    ax.set_xticks([1, 2, 3], ["Bajo", "Medio", "Alto"])
    ax.set_yticks([1, 2, 3], ["Bajo", "Medio", "Alto"])
    ax.set_xlabel("Esfuerzo")
    ax.set_ylabel("Impacto")
    ax.set_title("Matriz impacto / esfuerzo de las acciones de mejora")
    for txt, (x, y) in {"QUICK WINS": (0.6, 3.4), "PLANIFICAR": (2.1, 3.4),
                        "SI HAY CAPACIDAD": (0.6, 0.6), "BAJA PRIORIDAD": (2.1, 0.6)}.items():
        ax.text(x, y, txt, fontsize=9, color="#888", va="top" if y > 2 else "bottom")
    vistos = {}
    for d in data["defectos"]:
        for a in d["acciones"]:
            x, y = NIVEL[a["esfuerzo"]], NIVEL[a["impacto"]]
            k = vistos.get((x, y), 0)
            vistos[(x, y)] = k + 1
            ax.scatter(x + (k % 4) * 0.17 - 0.25, y + (k // 4) * 0.2 - 0.1, s=420, color="#2c6fad", alpha=0.85)
            ax.text(x + (k % 4) * 0.17 - 0.25, y + (k // 4) * 0.2 - 0.1, a["id"][2:], ha="center", va="center",
                    color="white", fontsize=8, weight="bold")
    fig.tight_layout()
    fig.savefig(img / "matriz_impacto_esfuerzo.png", dpi=150)
    plt.close(fig)
    print(f"Diagramas generados en {img.relative_to(ROOT)}")
    return 0


COMMANDS = {"validate": cmd_validate, "gate": cmd_gate, "report": cmd_report, "diagrams": cmd_diagrams}

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        sys.exit(2)
    sys.exit(COMMANDS[sys.argv[1]](load()))
