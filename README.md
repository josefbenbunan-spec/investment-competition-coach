# investment-competition-coach

[English version](README.en.md)

Skill de Claude que hace de coach y sparring para equipos de estudiantes en competiciones de inversión: Wharton Global High School Investment Competition, CFA Research Challenge, ligas de bolsa escolares y cualquier concurso en el que haya que diseñar una estrategia o una cartera para un cliente a partir de un caso.

## Qué hace

- Pide en el chat el caso del cliente, las reglas, los entregables y la política de IA de la competición. No depende de ninguna edición concreta, así que sirve año tras año.
- Construye con el equipo una ficha del cliente donde cada dato va etiquetado como dato del caso, inferencia o pendiente.
- Acompaña por fases: entender al cliente, Investment Policy Statement (IPS), asset allocation, selección de valores, gestión durante la competición e informe final.
- Trabaja con preguntas socráticas, escenarios de estrés y simulacros de jurado.
- Verifica las cuentas del equipo con un script incluido: rentabilidad requerida, pesos frente a los rangos del IPS y resultado frente al benchmark.
- No redacta texto para los entregables. Al cerrar cada sesión genera el registro de uso de IA para los Works Cited y un punto de guardado para seguir en otro chat.

## Un ejemplo

> **Equipo:** Escríbenos la sección de objetivos de rentabilidad del IPS, que vamos tarde.
>
> **Coach:** Esa sección la tenéis que escribir vosotros, es lo que evalúa el jurado. Os ayudo a prepararla. ¿Qué objetivo de vuestra clienta tiene una fecha y una cantidad concretas?

*(Ejemplo ilustrativo del comportamiento esperado.)*

## Instalación

### Claude (web y escritorio)

1. Descarga `investment-competition-coach.zip` desde la [última release](https://github.com/josefbenbunan-spec/investment-competition-coach/releases/latest).
2. En Claude, abre la sección de Skills, pulsa **+**, luego **Create skill** y **Upload a skill**, y sube el ZIP.
3. Comprueba que la ejecución de código está activada en la configuración. La skill la usa para verificar cálculos.

### Claude Code

```bash
git clone https://github.com/josefbenbunan-spec/investment-competition-coach.git
cp -r investment-competition-coach/skills/investment-competition-coach ~/.claude/skills/
```

### Con el CLI de skills

```bash
npx skills add josefbenbunan-spec/investment-competition-coach
```

## Cómo se usa

Basta con escribir algo como *"Estamos en la competición de inversión de Wharton y queremos empezar a trabajar el caso"*. La skill pedirá lo que necesita.

Consejo: para cada competición, cread un Proyecto en Claude y subid el caso como archivo. Así no hay que pegarlo en cada chat.

Para probarla sin un caso real, usa el caso inventado de [`ejemplos/caso-ejemplo.md`](ejemplos/caso-ejemplo.md). Si modificas la skill, repasa los prompts de [`ejemplos/casos-de-prueba.md`](ejemplos/casos-de-prueba.md) para comprobar que sigue comportándose bien.

## Estructura

```
skills/investment-competition-coach/
├── SKILL.md                      # instrucciones principales
├── references/
│   ├── ips-framework.md          # marco conceptual del IPS
│   ├── sparring-questions.md     # preguntas por fase, modo jurado, escenarios de estrés
│   ├── final-report.md           # medir y explicar los resultados en el informe final
│   └── ai-use-log.md             # formato del registro de IA y punto de guardado
├── assets/
│   └── case-intake.md            # plantilla de la ficha del cliente
└── scripts/
    └── check.py                  # verificación de cálculos (solo biblioteca estándar)
ejemplos/
├── caso-ejemplo.md               # caso inventado para probar la skill
└── casos-de-prueba.md            # prompts para comprobar el comportamiento
```

## Aviso

Herramienta educativa. No constituye asesoramiento financiero. Cada equipo es responsable de cumplir las normas de su competición y de declarar el uso de IA tal como se exija.
