<div align="center">

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&size=17&duration=900&pause=120&color=00FFFF&center=true&vCenter=true&width=950&lines=%5B+0.001s+%5D+init+pdf.engine...;%5B+0.032s+%5D+loading+styles...;%5B+0.087s+%5D+professional.theme+ready;%5B+0.142s+%5D+dark.neon.theme+ready;%5B+0.201s+%5D+layout.system+initialized;%5B+0.248s+%5D+flask.server+online;%5B+0.301s+%5D+form.studio+loaded;%5B+0.355s+%5D+table.editor+active;%5B+0.402s+%5D+section.builder+ready;%5B+0.447s+%5D+logo.upload+enabled;%5B+0.501s+%5D+integrity+check+%5BOK%5D;%5B+0.533s+%5D+style.system+%5BENABLED%5D;%5B+0.600s+%5D+pdf.studio+%3A+READY;%3E+SYSTEM+READY+%C2%B7+RENDER+ENGINE+ONLINE_)](https://git.io/typing-svg)

# PDF STYLE ENGINE · v2.0

[![English](https://img.shields.io/badge/🌐-English-blue?style=for-the-badge&labelColor=0d1117)](README.md)
![Status](https://img.shields.io/badge/STATUS-ACTIVO-00ffff?style=for-the-badge&labelColor=0d1117)
![Python](https://img.shields.io/badge/Python-3.10+-ffd700?style=for-the-badge&labelColor=0d1117)
![PDF](https://img.shields.io/badge/PDF-ReportLab-ff6b6b?style=for-the-badge&labelColor=0d1117)
![Flask](https://img.shields.io/badge/Web-Flask-39ff6e?style=for-the-badge&labelColor=0d1117)
![Styles](https://img.shields.io/badge/Estilos-2_Temas-ff00ff?style=for-the-badge&labelColor=0d1117)

**Motor PDF Modular · Temas Professional & Dark Neon · Formulario Web Dinámico · Servidor Flask · Construido con ReportLab**

</div>

---

## 📚 ÍNDICE

- [⚡ Stack Tecnológico](#-stack-tecnológico)
- [🎨 Sistema de Estilos](#-sistema-de-estilos)
- [🗂 Estructura del Proyecto](#-estructura-del-proyecto)
- [🎯 Características](#-características)
- [📦 Instalación](#-instalación)
- [🌐 Web Form Studio](#-web-form-studio)
- [💻 API Python](#-api-python)
- [⌨ CLI](#-cli)
- [🧱 Estructura de Datos](#-estructura-de-datos)
- [🖌 Extender con Estilos Personalizados](#-extender-con-estilos-personalizados)
- [⚠️ Aviso de Seguridad](#️-aviso-de-seguridad)
- [📜 Licencia y Términos de Uso](#-licencia-y-términos-de-uso)
- [📑 Requisitos](#-requisitos)

---

## ⚡ Stack Tecnológico

| Capa       | Tecnología       | Rol                             |
|------------|------------------|---------------------------------|
| Core       | Python 3.10+     | Motor de generación PDF         |
| PDF        | ReportLab        | Renderizado de documentos       |
| Servidor Web| Flask           | Servidor de formularios local   |
| Frontend   | HTML + Vanilla JS| Interfaz de formulario interactiva |
| CLI        | argparse         | Generación desde terminal       |
| Layout     | Custom           | Patrón strategy modular         |
| Fuentes    | Helvetica        | Tipografía adaptativa limpia    |

---

## 🎨 Sistema de Estilos

✔️ Arquitectura desacoplada — cada estilo es completamente independiente
✔️ Patrón strategy — intercambia o extiende estilos sin tocar el núcleo
✔️ Renderizado dinámico — los campos ausentes se omiten silenciosamente, sin huecos en blanco

| Professional | Dark Neon |
|:---:|:---:|
| ![Vista previa Professional](images/sample_professional_preview.png) | ![Vista previa Cyber](images/sample_cyber_preview.png) |
| Diseño corporativo limpio · Helvetica · paleta neutra · logo opcional | Carbón oscuro · acentos verde eléctrico · cuadrícula de puntos · neón minimalista |

---

## 🗂 Estructura del Proyecto

```
pdf_generator/
│
├── pdf_generator.py       # Motor core — ProfessionalStyle + CyberStyle
├── form_app.py            # Servidor Flask — sirve el formulario y llama al motor
├── form.html              # UI de formulario web interactivo (archivo único, sin deps)
├── generate_samples.py    # Herramienta CLI + datos de ejemplo para ambos estilos
│
└── output/
    ├── sample_professional.pdf
    └── sample_cyber.pdf
```

---

## 🎯 Características

### Motor PDF (`pdf_generator.py`)
- **Estilo Professional** — márgenes amplios, jerarquía Helvetica, acento azul `#007ACC`, carga de logo opcional, filas alternas en tablas, separadores limpios de sección, desbordamiento consciente de página
- **Estilo Dark Neon** — carbón profundo `#0D0D0D`, acentos verde eléctrico `#39FF6E`, fondo de cuadrícula de puntos sutil, franja neón en el borde izquierdo, secciones con superficie de tarjeta, tabla con reglas neón, bloque de arte ASCII, hash SHA-256 en el pie de página
- **Salida determinista** — los mismos datos siempre producen bytes idénticos
- **Campos dinámicos** — cada clave es opcional; los campos ausentes no producen espacio en blanco

### Web Form Studio (`form_app.py` + `form.html`)
- **Navegación lateral de 5 paneles** — Estilo, Metadatos, Secciones, Tabla, Arte ASCII
- **Selector de estilo en vivo** — alternancia visual de tarjetas entre Professional y Dark Neon
- **Carga de logo** — arrastrar y soltar PNG/JPG, vista previa en vivo antes de generar
- **Constructor de secciones dinámico** — añadir/eliminar/reordenar secciones de contenido al vuelo
- **Editor de tabla inline** — añadir/eliminar columnas y filas, la primera fila se trata automáticamente como cabecera
- **Generar y descargar con un clic** — el PDF se transmite directamente al navegador, sin recarga de página
- **Cero dependencias frontend** — HTML puro + Vanilla JS, sin npm, sin CDN

---

## 📦 Instalación

```bash
pip install reportlab flask
```

---

## 🌐 Web Form Studio

La forma más rápida de crear PDFs completamente personalizados — rellena un formulario, haz clic en generar, descarga.

```bash
python form_app.py
```

Luego abre **[http://localhost:5050](http://localhost:5050)** en tu navegador.

> ⚠️ **Advertencia de seguridad**: `form_app.py` ejecuta un **servidor de desarrollo local** (`debug=False`, sin HTTPS, sin autenticación). Está destinado **estrictamente para uso personal y offline** en tu propia máquina. **No expongas este servidor a internet público** ni lo ejecutes en redes abiertas. No hay sanitización de entradas más allá de la verificación básica de tipos de archivo, y los archivos subidos se almacenan en directorios temporales. Para despliegues en producción, utiliza un servidor WSGI adecuado (Gunicorn, uWSGI) detrás de un proxy inverso con terminación TLS y autenticación.

### Paneles del formulario

| Panel | Campos |
|---|---|
| 🎨 **Estilo** | Selector de tema (Professional / Dark Neon) · Carga de logo |
| 📋 **Metadatos** | Título · Subtítulo · Fecha · ID de referencia · Empresa · Contacto · Hash ID |
| 📝 **Secciones** | Secciones ilimitadas — cada una con encabezado + cuerpo de texto libre |
| 📊 **Tabla** | Editor de celdas en vivo · añadir/eliminar filas y columnas dinámicamente |
| 🌑 **Arte ASCII** | Bloque de arte monoespaciado (estilo Dark Neon únicamente) |

> Todos los campos son opcionales. Los campos vacíos se omiten automáticamente del PDF final.

---

## 💻 API Python

```python
from pdf_generator import generate_pdf

data = {
    "title":     "Annual Technology Review 2025",
    "subtitle":  "Strategic Infrastructure Assessment",
    "date":      "2025-05-06",
    "reference": "TEC-2025-0042",
    "company":   "Nexus Consulting Group",
    "contact":   "info@nexus.io · +1 800 555 0199",
    "sections": [
        {
            "heading": "Executive Summary",
            "body": "Cloud adoption accelerated by 34% YoY..."
        }
    ],
    "table": {
        "headers": ["System", "Status", "Coverage"],
        "rows": [
            ["AWS Cloud",   "Operational", "100%"],
            ["On-Prem K8s", "Degraded",    "94%"],
        ]
    }
}

# Estilo Professional
generate_pdf("professional", data, "report.pdf")

# Estilo Dark Neon
generate_pdf("cyber", data, "report_dark.pdf")
```

---

## ⌨ CLI

```bash
# Generar ambos PDFs de ejemplo
python generate_samples.py

# Generar un solo estilo
python generate_samples.py --style professional
python generate_samples.py --style cyber

# Directorio de salida personalizado
python generate_samples.py --out /ruta/a/carpeta
```

---

## 🧱 Estructura de Datos

Todas las claves son opcionales. Los campos no presentes en el dict se saltan silenciosamente.

```python
{
    # ── Encabezado / Metadatos ─────────────────────────────────
    "title":       str,   # Título principal del documento
    "subtitle":    str,   # Subtítulo
    "date":        str,   # Fecha mostrada en el encabezado
    "reference":   str,   # Referencia / ID del documento
    "company":     str,   # Nombre de empresa o autor (pie de página)
    "contact":     str,   # Línea de contacto (pie de página)

    # ── Solo Professional ──────────────────────────────────────
    "logo_path":   str,   # Ruta absoluta a un logo PNG/JPG

    # ── Solo Dark Neon ─────────────────────────────────────────
    "hash_id":     str,   # Hash en el pie (SHA-256 automático si se omite)
    "ascii_art":   str,   # Bloque de arte ASCII preformateado

    # ── Contenido ──────────────────────────────────────────────
    "sections": [
        {
            "heading": str,   # Título de sección (opcional)
            "body":    str,   # Texto de cuerpo (ajuste de palabras automático)
        }
    ],

    # ── Tabla ──────────────────────────────────────────────────
    "table": {
        "headers": ["Col A", "Col B", "Col C"],
        "rows": [
            ["val1", "val2", "val3"],
        ]
    }
}
```

---

## 🖌 Extender con Estilos Personalizados

Subclasea `BaseStyle` y regístralo bajo cualquier nombre:

```python
from pdf_generator import BaseStyle, register_style
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

class RetroStyle(BaseStyle):
    def build(self, output_path: str) -> None:
        c = canvas.Canvas(output_path, pagesize=A4)
        # tu lógica de dibujo aquí
        c.save()

# Registrar y usar como cualquier estilo integrado
register_style("retro", RetroStyle)
generate_pdf("retro", data, "retro_doc.pdf")
```

---

## ⚠️ Aviso de Seguridad

> **🔒 Solo Uso Local**
>
> Este proyecto incluye un servidor de desarrollo Flask (`form_app.py`) destinado **exclusivamente para uso local y personal**. **No está endurecido para producción** y carece de:
> - HTTPS / cifrado TLS
> - Autenticación o control de acceso
> - Protección CSRF
> - Limitación de tasa (rate limiting)
> - Validación exhaustiva de entradas
>
> **Nunca expongas `form_app.py` a internet público.** Ejecútalo siempre en `localhost` o dentro de una red privada de confianza. Los logos subidos se almacenan en archivos temporales y se eliminan tras la generación, pero no se ofrecen garantías contra payloads maliciosos.
>
> Para cualquier escenario más allá de la generación personal de PDFs en tu propia máquina, despliega detrás de un proxy inverso (Nginx, Caddy) con TLS, utiliza un servidor WSGI de producción e implementa autenticación adecuada.

---

## 📜 Licencia y Términos de Uso

Este proyecto está licenciado bajo **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International** (CC BY-NC-ND 4.0).

### Qué significa esto:

| ✅ PUEDES | ❌ NO PUEDES |
|---|---|
| Usar, descargar y ejecutar este software para **fines personales, educativos o de investigación** | Usar este software o su salida para **fines comerciales** (vender, monetizar o integrar en productos/servicios de pago) |
| Compartir el código fuente original sin modificar con atribución | Crear y compartir **versiones modificadas** (derivadas) de este software |
| Generar PDFs para uso personal o sin ánimo de lucro | Eliminar o alterar los avisos de atribución / copyright |
| Referenciar este proyecto en contextos académicos o educativos | Usar el código como parte de un SaaS comercial, servicio de agencia o producto propietario |

### Texto Legal Completo

El texto completo de la licencia está disponible en [`LICENSE`](LICENSE) o en:
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

### Requisito de Atribución

Si compartes este proyecto, debes incluir:
- El crédito al autor original
- Un enlace a este repositorio
- Un aviso de que el material está licenciado bajo CC BY-NC-ND 4.0
- Un enlace al texto completo de la licencia

### Licenciamiento Comercial

Si deseas usar este proyecto para **fines comerciales** — incluyendo pero no limitado a:
- Integrarlo en un producto o servicio de pago
- Usarlo como parte de trabajo para cliente o entregables de agencia
- Incluirlo en una plataforma SaaS
- Redistribuir versiones modificadas

**Por favor contacta al autor para discutir una licencia comercial separada.**

> **TL;DR**: Gratis para uso personal. No gratis para uso empresarial. No remixes sin permiso. Atribución requerida.

---

## 📑 Requisitos

- Python 3.10+
- ReportLab 4.0+
- Flask 3.0+ *(solo requerido para el formulario web)*

---

<div align="center">

![Visitors](https://hits.sh/github.com/ogclau/ReportLabStyleSuite.svg?style=for-the-badge&color=39ff6e&labelColor=0d1117)

Python · ReportLab · Flask · Arquitectura Modular

</div>
