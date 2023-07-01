# KUNUNUA

Kununua es una aplicación móvil que permite a los usuarios realizar la compra de productos de supermercado de manera eficiente. Para ello, la aplicación permite a los usuarios crear cestas de la compra con productos de distintos supermercados que, posteriormente pueden ser optimizadas para que el usuario ahorre dinero y tiempo.

# Manual para desarrolladores

Este manual es una guía de desarrollador cuyo objetivo es utilizar el
proyecto con fines de experimentación o de manera local para adaptarlo.
Su contenido está pensado exclusivamente para usuarios técnicos.

## Lanzamiento del proyecto en máquina local

### Requisitos previos

Antes de comenzar a lanzar KUNUNUA en la máquina local, es necesario
tener instalado el siguiente software:

-   `Flutter:` 3.10.3

-   `CocoaPods:` 1.11.3

-   `Dart:` 3.0.3

-   `Python:` 3.8.13

### Pasos previos

1.  Clonar el ropositorio
```bash
    git clone https://github.com/Kununua/kununua-app.git
```

### Backend

1.  Crear una base de datos en PostgreSQL y un usuario con todos los
    permisos sobre ella. (De ahora en adelante, nos referiremos a esta
    BD con el nombre: `kununua_db`):

    - Accedemos a la consola de PostgreSQL:

    ```bash
        psql postgres
    ```

    - Creamos la base de datos y el usuario (en este caso, con credenciales: `kununua_user` y `kununua_password`):

    ```postgresql
        CREATE DATABASE kununua_db;
        CREATE USER kununua_user WITH PASSWORD 'kununua_password';
        GRANT ALL PRIVILEGES ON DATABASE kununua_db TO kununua_user;
    ```
    - Salimos de la consola de PostgreSQL con: `\q`

2.  Accedemos a la carpeta `kununua_backend` del proyecto.

3.  Instalamos todos los requisitos (recomendamos hacerlo dentro de un
    entorno virtual):
    
    ```
        pip install -r requirements.txt
    ```

4.  Creamos y ejecutamos todas las migraciones de los modelos de django
    a la base de datos:

    ```
        python manage.py makemigrations
        python manage.py migrate
    ```

5.  Poblamos la base de datos con información sobre las marcas de los
    productos, países y divisas:

    ```
        python manage.py populate_countries
        python manage.py populate_brands
    ```

6.  Instalamos el solver CPLEX en el módulo de amplpy y activamos
    nuestra licencia:

    ```
        python -m amplpy.modules install cplex
        python -m amplpy.modules activate <uuid-licencia>
    ```

7.  Colocamos en los ajustes del proyecto de django la ruta de
    instalación de ampl. En
    “kununua_backend/kununua_backend/settings/development.py”:

    ```python
        ...
        # The AMPL instalation path that is being used by amplpy
        AMPL_PATH = r"/path/to/ampl/intstallation/dir"
        ...
    ```

8.  Lanzamos el backend de la aplicación en el puerto 8000:

    ```
        python manage.py runserver
    ```

### Backend

1.  Accedemos a la carpeta `kununua_app` del proyecto

2.  Descargamos todas las dependencias:

    ```
        flutter pub get
    ```

3.  Lanzamos el proyecto en modo de desarrollo en el dispositivo que
    tengamos seleccionado:

    ```
        flutter run
    ```

## Comandos disponibles para gestionar los datos

Debido a la complejidad que posee el backend del proyecto, hemos puesto
a disposición de los desarrolladores una serie de comandos que facilitan
la ejecución de algunas tareas. A continuación se detalla cada uno de
ellos:

-   **download_images:**

    -   **Descripción:** descarga las imágenes de todos los productos
        almacenados en la BD que tienen en campo correspondiente un
        enlace web para almacenarlas en el ordenador (o servidor,
        depende de dónde instalemos el proyecto).

    -   **Precondiciones:** Tener la base de datos de PostgreSQL con
        información del los productos tras el postprocesado.

-   **download_spanish_model:**

    -   **Descripción:** descarga en el ordenador del usuario el modelo
        de español que utiliza stanza, un paquete de python que permite
        analizar sintácticamente oraciones.

    -   **Precondiciones:** Tener instalado el paquete de Stanza.

-   **cart_optimization_experiment:**

    -   **Descripción:** con este comando se lanza el experimento de
        optimización de la sección
        <a href="#exp:optimization" data-reference-type="ref"
        data-reference="exp:optimization">[exp:optimization]</a>.
        Almacenará en el mismo directorio un archivo `.xlsx` con los
        resultados. Dentro del archivo que referencia el comando pueden
        activarse o desactivarse distintas funcionalidades. Por ejemplo:
        imprimir por consola los resultados o exportarlos a `.csv` en
        lugar de `.xlsx`.

    -   **Precondiciones:** Tener la base de datos poblada con
        productos.

-   **populate_brands:**

    -   **Descripción:** puebla la base de datos con los nombres de más
        de 2500 marcas de productos (Figura
        <a href="#fig:brands" data-reference-type="ref"
        data-reference="fig:brands">[fig:brands]</a>).

    -   **Precondiciones:** Ninguna.

-   **populate_countries:**

    -   **Descripción:** puebla la base de datos configurada con
        información de los paises del mundo y sus divisas (Figura
        <a href="#fig:countries" data-reference-type="ref"
        data-reference="fig:countries">[fig:countries]</a>).

    -   **Precondiciones:** Ninguna.

-   **post_process_data:**

    -   **Descripción:** ejecuta el proceso de postprocesado de datos
        extraídos de los supermercados a partir de la base de datos
        temporal de SQLite.

    -   **Precondiciones:** Tener una base de datos SQLite con la
        información “cruda” de la extracción de los supermercados. Haber
        lanzado los comandos `populate_countries`, `populate_brands`.

-   **run_scraper:**

    -   **Descripción:** lanza la extracción de datos de las páginas web
        de los supermercados con los scrapers. Dentro del archivo que
        referencia el comando puede seleccionarse qué scarpers lanzar.

    -   **Precondiciones:** Ninguna.