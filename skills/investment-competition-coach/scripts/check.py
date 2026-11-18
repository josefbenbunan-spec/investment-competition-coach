#!/usr/bin/env python3
"""Comprobaciones numéricas para equipos de competiciones de inversión.

El equipo hace primero sus cuentas; este script sirve para verificarlas.
Solo usa la biblioteca estándar de Python 3.

Subcomandos:
  rentabilidad   Rentabilidad anual requerida para llegar a un objetivo.
  asignacion     Pesos por clase de activo frente a los rangos del IPS,
                 concentración por sector y por posición.
  resultado      Rentabilidad de la cartera frente al benchmark y
                 contribución de cada posición.

Los porcentajes se escriben como número: 3 significa 3 %.
Los números pueden llevar coma o punto decimal (12500,50 o 12500.50).

Ejemplos:
  python check.py rentabilidad --hoy 100000 --objetivo 160000 --anos 10 \\
      --aportacion 2000 --flujo 2:-20000 --inflacion 2.5
  python check.py asignacion --cartera cartera.csv \\
      --rango "Renta variable=55-65" --rango "Renta fija=25-35" \\
      --max-sector 25 --max-posicion 10
  python check.py resultado --cartera resultado.csv --benchmark 3.1
"""

import argparse
import csv
import sys
from collections import defaultdict


# ---------------------------------------------------------------- utilidades

def num(texto):
    """Convierte '12.500,50', '12500.50', '7 %' o '$1,200.00' en float."""
    s = str(texto).strip()
    for simbolo in ("€", "$", "%", " ", " "):
        s = s.replace(simbolo, "")
    if not s:
        raise ValueError("celda vacía")
    if "," in s and "." in s:
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    elif "," in s:
        s = s.replace(",", ".")
    return float(s)


def pct(x):
    return f"{x * 100:,.2f} %".replace(",", "X").replace(".", ",").replace("X", ".")


def dinero(x):
    return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


ALIAS = {
    "ticker": ["ticker", "simbolo", "símbolo", "valor", "nombre", "symbol", "name"],
    "clase": ["clase", "clase de activo", "class", "asset class"],
    "sector": ["sector"],
    "peso": ["peso", "peso %", "weight"],
    "importe": ["importe", "value", "market value", "importe actual"],
    "inicial": ["inicial", "importe inicial", "start", "start value"],
    "final": ["final", "importe final", "end", "end value"],
}


def leer_csv(ruta):
    with open(ruta, newline="", encoding="utf-8-sig") as f:
        muestra = f.read(4096)
        f.seek(0)
        try:
            dialecto = csv.Sniffer().sniff(muestra, delimiters=",;\t")
        except csv.Error:
            dialecto = csv.excel
        filas = list(csv.DictReader(f, dialect=dialecto))
    if not filas:
        sys.exit(f"El archivo {ruta} no tiene filas.")
    columnas = {c.strip().lower(): c for c in filas[0].keys() if c}
    mapa = {}
    for campo, nombres in ALIAS.items():
        for n in nombres:
            if n in columnas:
                mapa[campo] = columnas[n]
                break
    return filas, mapa


def exigir(mapa, campos, ruta):
    faltan = [c for c in campos if c not in mapa]
    if faltan:
        sys.exit(f"Faltan columnas en {ruta}: {', '.join(faltan)}. "
                 f"Columnas aceptadas: {ALIAS}")


# ------------------------------------------------------ rentabilidad requerida

def valor_futuro(r, hoy, anos, aportacion, flujos):
    total = hoy * (1 + r) ** anos
    for t in range(1, anos + 1):
        total += aportacion * (1 + r) ** (anos - t)
    for t, importe in flujos:
        total += importe * (1 + r) ** (anos - t)
    return total


def cmd_rentabilidad(a):
    flujos = []
    for f in a.flujo or []:
        try:
            t, importe = f.split(":")
            t = int(t)
        except ValueError:
            sys.exit(f"Flujo mal escrito: {f}. Formato: AÑO:IMPORTE, p. ej. 3:-20000")
        if not 1 <= t <= a.anos:
            sys.exit(f"El flujo {f} cae fuera del horizonte de {a.anos} años.")
        flujos.append((t, num(importe)))

    inflacion = a.inflacion / 100
    objetivo = a.objetivo
    if a.objetivo_en_dinero_de_hoy:
        objetivo = a.objetivo * (1 + inflacion) ** a.anos

    def f(r):
        return valor_futuro(r, a.hoy, a.anos, a.aportacion, flujos) - objetivo

    lo, hi = -0.99, 2.0
    if f(lo) * f(hi) > 0:
        sys.exit("No hay una rentabilidad entre -99 % y 200 % anual que alcance el "
                 "objetivo con estos datos. Revisad importes y signos de los flujos.")
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    r = (lo + hi) / 2
    real = (1 + r) / (1 + inflacion) - 1

    print("Datos")
    print(f"  Valor hoy:              {dinero(a.hoy)}")
    print(f"  Objetivo:               {dinero(a.objetivo)}"
          + (" (en dinero de hoy)" if a.objetivo_en_dinero_de_hoy else ""))
    if a.objetivo_en_dinero_de_hoy:
        print(f"  Objetivo nominal:       {dinero(objetivo)} "
              f"con inflación del {pct(inflacion)}")
    print(f"  Horizonte:              {a.anos} años")
    if a.aportacion:
        print(f"  Aportación anual:       {dinero(a.aportacion)} (al final de cada año)")
    for t, importe in flujos:
        tipo = "aportación" if importe > 0 else "retirada"
        print(f"  Año {t}:                  {tipo} de {dinero(abs(importe))}")
    print()
    print(f"Rentabilidad requerida nominal: {pct(r)} anual")
    if inflacion:
        print(f"Rentabilidad requerida real:    {pct(real)} anual "
              f"(descontada una inflación del {pct(inflacion)})")
    print()
    print("Comprobación: con esa rentabilidad la cartera termina en "
          f"{dinero(valor_futuro(r, a.hoy, a.anos, a.aportacion, flujos))}.")


# ----------------------------------------------------------------- asignación

def cmd_asignacion(a):
    filas, mapa = leer_csv(a.cartera)
    exigir(mapa, ["ticker", "clase"], a.cartera)
    if "peso" in mapa:
        importes = [num(f[mapa["peso"]]) for f in filas]
    elif "importe" in mapa:
        importes = [num(f[mapa["importe"]]) for f in filas]
    else:
        sys.exit("La cartera necesita una columna 'peso' (en %) o 'importe'.")
    total = sum(importes)
    if total <= 0:
        sys.exit("La suma de pesos o importes es cero.")
    if "peso" in mapa and abs(total - 100) > 0.5:
        print(f"AVISO: los pesos suman {total:.2f} %, no 100 %. Se normalizan.\n")

    pesos = [x / total for x in importes]
    por_clase = defaultdict(float)
    por_sector = defaultdict(float)
    for fila, p in zip(filas, pesos):
        por_clase[fila[mapa["clase"]].strip()] += p
        if "sector" in mapa and fila[mapa["sector"]].strip():
            por_sector[fila[mapa["sector"]].strip()] += p

    rangos = {}
    for r in a.rango or []:
        try:
            clase, tramo = r.split("=")
            minimo, maximo = tramo.split("-")
            rangos[clase.strip()] = (num(minimo) / 100, num(maximo) / 100)
        except ValueError:
            sys.exit(f"Rango mal escrito: {r}. Formato: \"Clase=MIN-MAX\"")

    incidencias = 0
    print("Pesos por clase de activo")
    for clase in sorted(set(por_clase) | set(rangos)):
        p = por_clase.get(clase, 0.0)
        linea = f"  {clase:<24} {pct(p):>10}"
        if clase in rangos:
            minimo, maximo = rangos[clase]
            ok = minimo - 1e-9 <= p <= maximo + 1e-9
            linea += f"   rango {pct(minimo)} a {pct(maximo)}   {'OK' if ok else 'FUERA DE RANGO'}"
            incidencias += not ok
        elif rangos:
            linea += "   sin rango en el IPS"
        print(linea)

    if por_sector:
        print("\nPesos por sector")
        for sector, p in sorted(por_sector.items(), key=lambda x: -x[1]):
            aviso = ""
            if a.max_sector is not None and p > a.max_sector / 100 + 1e-9:
                aviso = f"   supera el máximo de {pct(a.max_sector / 100)}"
                incidencias += 1
            print(f"  {sector:<24} {pct(p):>10}{aviso}")

    if a.max_posicion is not None:
        grandes = [(f[mapa["ticker"]], p) for f, p in zip(filas, pesos)
                   if p > a.max_posicion / 100 + 1e-9]
        print(f"\nPosiciones por encima de {pct(a.max_posicion / 100)}")
        if grandes:
            for t, p in sorted(grandes, key=lambda x: -x[1]):
                print(f"  {t:<24} {pct(p):>10}")
            incidencias += len(grandes)
        else:
            print("  Ninguna")

    print(f"\n{len(filas)} posiciones. Incidencias: {incidencias}.")


# ------------------------------------------------------------------ resultado

def cmd_resultado(a):
    filas, mapa = leer_csv(a.cartera)
    exigir(mapa, ["ticker", "inicial", "final"], a.cartera)
    datos = []
    for f in filas:
        datos.append((f[mapa["ticker"]].strip(),
                      f[mapa["clase"]].strip() if "clase" in mapa else "",
                      num(f[mapa["inicial"]]), num(f[mapa["final"]])))
    total_ini = sum(d[2] for d in datos)
    total_fin = sum(d[3] for d in datos)
    if total_ini <= 0:
        sys.exit("El valor inicial total es cero.")
    rent = total_fin / total_ini - 1

    print(f"Valor inicial: {dinero(total_ini)}")
    print(f"Valor final:   {dinero(total_fin)}")
    print(f"Rentabilidad de la cartera: {pct(rent)}")
    if a.benchmark is not None:
        b = a.benchmark / 100
        print(f"Rentabilidad del benchmark: {pct(b)}")
        print(f"Diferencia frente al benchmark: {pct(rent - b)}")

    print("\nContribución de cada posición (suman la rentabilidad total)")
    contrib = sorted(((t, (fin - ini) / total_ini, fin / ini - 1 if ini else 0.0)
                      for t, _, ini, fin in datos), key=lambda x: -x[1])
    for t, c, r in contrib:
        print(f"  {t:<24} contribución {pct(c):>10}   rentabilidad propia {pct(r):>10}")

    if "clase" in mapa:
        print("\nContribución por clase de activo")
        por_clase = defaultdict(float)
        for _, clase, ini, fin in datos:
            por_clase[clase] += (fin - ini) / total_ini
        for clase, c in sorted(por_clase.items(), key=lambda x: -x[1]):
            print(f"  {clase:<24} {pct(c):>10}")

    print("\nNota: si hubo compras o ventas a mitad de periodo, las cifras por "
          "posición son aproximadas. La rentabilidad total oficial es la del simulador.")


# ----------------------------------------------------------------------- main

def main():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("rentabilidad", help="rentabilidad anual requerida")
    r.add_argument("--hoy", type=num, required=True, help="valor de la cartera hoy")
    r.add_argument("--objetivo", type=num, required=True,
                   help="importe que debe haber al final del horizonte")
    r.add_argument("--anos", type=int, required=True, help="horizonte en años")
    r.add_argument("--aportacion", type=num, default=0.0,
                   help="aportación anual al final de cada año (negativa = retirada)")
    r.add_argument("--flujo", action="append",
                   help="flujo puntual AÑO:IMPORTE, p. ej. 3:-20000 (repetible)")
    r.add_argument("--inflacion", type=num, default=0.0, help="inflación anual en %%")
    r.add_argument("--objetivo-en-dinero-de-hoy", action="store_true",
                   help="el objetivo está en dinero de hoy y se ajusta por inflación")
    r.set_defaults(func=cmd_rentabilidad)

    s = sub.add_parser("asignacion", help="pesos frente a los rangos del IPS")
    s.add_argument("--cartera", required=True,
                   help="CSV con ticker, clase, sector (opcional) y peso o importe")
    s.add_argument("--rango", action="append",
                   help='rango del IPS, p. ej. "Renta variable=55-65" (repetible)')
    s.add_argument("--max-sector", type=num, help="peso máximo por sector en %%")
    s.add_argument("--max-posicion", type=num, help="peso máximo por posición en %%")
    s.set_defaults(func=cmd_asignacion)

    t = sub.add_parser("resultado", help="rentabilidad frente al benchmark")
    t.add_argument("--cartera", required=True,
                   help="CSV con ticker, clase (opcional), inicial y final")
    t.add_argument("--benchmark", type=num,
                   help="rentabilidad del benchmark en el mismo periodo, en %%")
    t.set_defaults(func=cmd_resultado)

    a = p.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
