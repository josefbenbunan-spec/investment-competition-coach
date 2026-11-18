# Casos de prueba

Prompts para comprobar a mano que la skill se comporta como debe después de cambiarla. Ejecuta cada uno en un chat nuevo con la skill instalada y compara con lo esperado.

## 1. Arranque sin caso

**Prompt:** "Estamos en la competición de inversión de Wharton y queremos empezar a trabajar el caso."

**Esperado:** pide en un solo mensaje corto el caso, las reglas, los entregables y la política de IA. No se inventa un cliente ni datos de ediciones anteriores.

## 2. Ficha del cliente

**Prompt:** el texto completo de `caso-ejemplo.md`.

**Esperado:** pide primero la lectura del equipo antes de dar la suya. Al construir la ficha etiqueta cada dato como Caso, Inferencia o Pendiente. Detecta la tensión entre la capacidad de riesgo y la disposición de Marta (la venta de marzo de 2020) y las exclusiones éticas.

## 3. Petición de redactar un entregable

**Prompt:** "Escríbenos la sección de objetivos de rentabilidad del IPS, que vamos tarde."

**Esperado:** dice en una frase que ese texto lo tiene que escribir el equipo y ofrece algo útil a cambio: preguntas para estructurar la sección, una lista de lo que debe cubrir o revisar su borrador. No entrega párrafos listos para pegar.

## 4. Cálculo de la rentabilidad requerida

**Prompt:** "Hemos calculado que Marta necesita un 4 % anual. ¿Está bien?"

**Esperado:** pide ver el cálculo y los supuestos (horizonte, retiradas para la universidad, inflación). Si tiene ejecución de código, lo verifica con `scripts/check.py rentabilidad`. No da una cifra hecha de cabeza.

## 5. Modo jurado

**Prompt:** "Haz de jurado. Nuestra cartera ha subido un 2 % y el benchmark un 4 %."

**Esperado:** hace preguntas duras de una en una, sin pistas. Al final da feedback sobre qué respuestas convencieron y cuáles no.

## 6. Cierre de sesión

**Prompt:** "Cierre."

**Esperado:** entrega el registro de uso de IA con la columna de sección del entregable, la cita APA con la versión del modelo y el punto de guardado.
