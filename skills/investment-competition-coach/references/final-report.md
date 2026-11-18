# Informe final: medir y explicar los resultados

Léelo al entrar en la fase 6. El informe final lo escribe el equipo. Tu trabajo aquí es ayudarles a medir bien, a explicar lo que pasó y a comprobar que la historia del informe sale del IPS.

## Qué suele valorar el jurado

En muchas competiciones no gana la cartera que más sube. En Wharton, por ejemplo, los semifinalistas se eligen por la calidad del IPS y del informe final. Pide al equipo la rúbrica y repasadla juntos antes de que empiecen a escribir. Si no hay rúbrica, el criterio razonable es este: que cada decisión se pueda rastrear hasta el cliente y que el equipo sepa explicar tanto lo que salió bien como lo que salió mal.

## Lo que debería cubrir el informe

Úsalo como lista de comprobación, nunca como texto para copiar. Comprueba con el equipo que su informe responde a estas preguntas y en qué sección lo hace:

- Quién es el cliente y qué fijó el IPS (objetivos, riesgo, restricciones, benchmark).
- Qué cartera se montó y por qué cada clase de activo y cada posición.
- Qué operaciones se hicieron durante la competición y qué línea del IPS las justifica.
- Cómo fue la cartera frente al benchmark y qué lo explica.
- Qué riesgos se materializaron y cuáles no.
- Qué haría distinto el equipo y si eso cambiaría el IPS.

## Medir la rentabilidad

- **Rentabilidad de la cartera**: valor final dividido entre valor inicial, menos 1. Si el simulador de la competición da la cifra, usad la del simulador y comprobad que cuadra.
- **Rentabilidad del benchmark** en el mismo periodo exacto, con las mismas fechas de inicio y fin.
- **Diferencia frente al benchmark**: rentabilidad de la cartera menos la del benchmark. Es la cifra que más mira un jurado.
- `python scripts/check.py resultado` hace estas cuentas a partir de un CSV con el valor inicial y final de cada posición. Si hubo compras y ventas a mitad de periodo, el resultado por posición es aproximado; el total debe salir del simulador.

## Explicar el resultado (atribución)

Para secundaria basta con la versión sencilla:

- **Contribución de cada posición**: lo que ganó o perdió esa posición dividido entre el valor inicial de toda la cartera. Las contribuciones suman la rentabilidad total. Así se ve qué tres o cuatro posiciones explican casi todo el resultado.
- **Clase de activo frente a selección**: ¿el resultado se debe a cuánto pusieron en cada clase (más bolsa que el benchmark en un periodo alcista, por ejemplo) o a qué valores eligieron dentro de cada clase? Pregúntalo así antes de dar fórmulas.

Si el equipo quiere ir más lejos, explica el modelo de Brinson con un ejemplo de su propia cartera:

- Efecto asignación de una clase = (peso en la cartera menos peso en el benchmark) × (rentabilidad de esa clase en el benchmark menos rentabilidad total del benchmark).
- Efecto selección de una clase = peso en el benchmark × (rentabilidad de esa clase en la cartera menos rentabilidad de esa clase en el benchmark).

## Hablar de riesgo sin jerga

- **Volatilidad**: cuánto se mueve la cartera de una semana a otra. Más volatilidad significa un camino más movido, aunque se llegue al mismo sitio.
- **Caída máxima**: la peor bajada desde un máximo hasta el mínimo siguiente. Es lo que un cliente nervioso recuerda.
- **Beta**: cuánto se mueve la cartera cuando se mueve el mercado. Una beta de 1,2 sube y baja algo más que el índice.

Una competición dura pocas semanas. Recuérdale al equipo que en un periodo tan corto el resultado depende mucho de la suerte, y que el jurado valora que lo reconozcan.

## Operaciones

Pide al equipo una tabla con fecha, operación, motivo y línea del IPS que la justifica. Cada fila debería poder defenderse en voz alta en treinta segundos. Una operación cuyo motivo es "el mercado de esa semana" necesita una explicación honesta en el informe.

## Errores frecuentes en el informe

- Atribuirse el mérito de una subida que tuvo todo el mercado.
- Gráficos de rentabilidad sin el benchmark al lado.
- Esconder las posiciones que salieron mal. Explicarlas suma puntos.
- Contar una estrategia distinta de la que fijó el IPS sin decir que cambió ni por qué.
- Usar cifras sin fuente o sin fecha.
