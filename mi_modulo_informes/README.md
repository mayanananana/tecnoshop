# Módulo de Informes Personalizados en Odoo 18

Este módulo para Odoo 18 demuestra cómo crear un informe QWeb-PDF a partir de datos que no residen en una tabla estándar de Odoo, utilizando en su lugar una **vista de base de datos SQL**.

## Estructura del Módulo y Funcionalidad

El objetivo principal de este módulo es generar un informe PDF que muestre una lista de registros con su nombre y un valor total. La particularidad es que estos datos se obtienen de una vista SQL en lugar de una tabla creada por el ORM de Odoo.

### Flujo de Funcionamiento

1.  **Acceso al Asistente**: El usuario navega a un nuevo menú principal llamado **"Informes Personalizados"** y hace clic en el submenú **"Informe de Datos Externos"**.
2.  **Apertura del Asistente (Wizard)**: Se abre una ventana emergente (un `TransientModel`) que presenta al usuario un único botón: "Imprimir".
3.  **Llamada a la Acción de Informe**: Al hacer clic en "Imprimir", el asistente ejecuta un método en Python. Este método busca todos los registros disponibles en el modelo virtual `external.data` (que está mapeado a nuestra vista SQL) y pasa sus IDs a la acción de informe.
4.  **Generación del PDF**: Odoo invoca la acción de informe, que a su vez utiliza una plantilla QWeb (`report_template.xml`) para renderizar los datos de los registros solicitados en un documento PDF.
5.  **Descarga del Informe**: El navegador del usuario descarga el archivo PDF generado.

## Descripción de Archivos Clave

A continuación se detalla qué hace cada archivo importante dentro del módulo:

### `__manifest__.py`

-   **Propósito**: Archivo de metadatos del módulo.
-   **Contenido**:
    -   Define el nombre del módulo (`Mi Módulo de Informes`), versión, autor, etc.
    -   Establece las dependencias necesarias (`base`, `web`).
    -   Enumera los archivos de datos (XML) y de seguridad (CSV) que deben cargarse, definiendo el orden de carga.

### `models/external_data.py`

-   **Propósito**: Definir el modelo de datos "virtual" que se conecta a la vista SQL.
-   **Clave**:
    -   `_name = 'external.data'`: Nombre técnico del modelo en Odoo.
    -   `_auto = False`: **Instrucción crítica**. Le dice a Odoo que **NO** debe crear una tabla en la base de datos para este modelo.
    -   `_table = 'external_data_sql_view'`: Mapea este modelo de Odoo a la vista SQL con ese nombre.
    -   `init(self)`: Este método se ejecuta durante la instalación o actualización del módulo. Contiene el SQL para crear la vista `external_data_sql_view`. En este caso, la vista contiene datos de ejemplo hardcodeados.
    -   `nombre` y `total`: Campos (`fields.Char`, `fields.Float`) que se corresponden con las columnas de la vista SQL. Son de solo lectura (`readonly=True`).

### `wizard/report_data_wizard.py`

-   **Propósito**: Define la lógica del asistente que inicia la generación del informe.
-   **Clave**:
    -   `_name = 'report.data.wizard'`: Modelo transitorio (los registros se borran periódicamente).
    -   `action_print_report(self)`: El método que se ejecuta al pulsar el botón "Imprimir". Busca todos los registros en `external.data` y llama a la acción de informe (`action_report_external_data`) pasándole los IDs de dichos registros.

### `wizard/report_data_wizard_view.xml`

-   **Propósito**: Define la interfaz de usuario del asistente.
-   **Contenido**:
    -   Una vista de formulario (`ir.ui.view`) que muestra un mensaje y los botones "Imprimir" y "Cancelar".
    -   Una acción de ventana (`ir.actions.act_window`) que abre esta vista de formulario en un diálogo modal (`target='new'`).

### `report/report_action.xml`

-   **Propósito**: Define la acción de informe que Odoo debe ejecutar.
-   **Contenido**:
    -   `id="action_report_external_data"`: El identificador único de la acción.
    -   `model = 'external.data'`: Especifica que el informe opera sobre el modelo `external.data`.
    -   `report_type = 'qweb-pdf'`: Indica que el resultado será un archivo PDF.
    -   `report_name = 'mi_modulo_informes.report_external_data_template'`: El nombre completo de la plantilla QWeb que se usará para el cuerpo del informe.

### `report/report_template.xml`

-   **Propósito**: La plantilla QWeb que diseña el contenido del PDF.
-   **Contenido**:
    -   Utiliza HTML estándar y directivas de QWeb (`t-call`, `t-foreach`, `t-esc`).
    -   Itera sobre la variable `docs`, que es un recordset de los registros de `external.data` pasados por el asistente.
    -   Para cada registro, muestra los campos `nombre` y `total`.

### `views/report_menu.xml`

-   **Propósito**: Crear las opciones de menú para que el usuario pueda acceder a la funcionalidad.
-   **Contenido**:
    -   Un `menuitem` principal ("Informes Personalizados").
    -   Un `menuitem` secundario ("Informe de Datos Externos") que, al hacer clic, ejecuta la acción de ventana del asistente (`action_window_report_data_wizard`).

### `security/ir.model.access.csv`

-   **Propósito**: Controlar los permisos de acceso a los modelos del módulo.
-   **Contenido**:
    -   Concede permiso de **lectura** (`perm_read=1`) sobre el modelo `external.data` al grupo de usuarios base (`base.group_user`). Esto es necesario para que puedan ver los datos en el informe.
    -   Concede permisos completos (crear, leer, escribir, borrar) sobre el asistente (`report.data.wizard`) para que los usuarios puedan abrirlo e interactuar con él.
