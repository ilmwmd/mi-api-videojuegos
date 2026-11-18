# Mi API de videojuegos

API REST hecha con FastAPI para gestionar un catálogo personal de videojuegos.
Cada videojuego tiene `id` (lo calcula la API), `titulo`, `genero`, `plataforma` y `anio`.
Los datos se guardan en `videojuegos.json`, así que los cambios siguen ahí al reiniciar el servidor.

## Cómo arrancarla

Desde la carpeta del proyecto (`mi-api-videojuegos`):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
fastapi dev main.py
```

Si PowerShell no permite activar el entorno, ejecuta antes `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`.

También puedes abrir la carpeta en VS Code y ejecutar la tarea **Run API dev** (`Terminal → Run Task…` o `Ctrl+Shift+B`). El entorno virtual ya está creado en este proyecto, así que en tu caso basta con la última línea.

Si prefieres arrancar sin el CLI de FastAPI: `uvicorn main:app --reload`.

La API queda en http://127.0.0.1:8000 y la documentación interactiva en http://127.0.0.1:8000/docs.

> Importantísimo: arranca el servidor desde esta carpeta, porque `main.py` busca `videojuegos.json` en el directorio actual.

## Rutas

| Método | Ruta | Qué hace |
| --- | --- | --- |
| GET | `/` | Mensaje de bienvenida |
| GET | `/videojuegos` | Lista todos los videojuegos |
| GET | `/videojuegos?genero=RPG` | Filtra por género (también funciona `?plataforma=PC`; se pueden combinar) |
| GET | `/videojuegos/{id}` | Busca uno por id; 404 si no existe |
| POST | `/videojuegos` | Agrega uno con id automático; 409 si el título ya existe |
| PUT | `/videojuegos/{id}` | Edita uno; 404 si no existe, 409 si el nuevo título ya existe |
| DELETE | `/videojuegos/{id}` | Borra uno; 404 si no existe |

Ejemplo de cuerpo para POST y PUT:

```json
{
  "titulo": "Celeste",
  "genero": "Plataformas",
  "plataforma": "PC",
  "anio": 2018
}
```

## Extras incluidos

- **Filtros:** `genero` y `plataforma` son parámetros opcionales en `GET /videojuegos`. La comparación ignora mayúsculas y espacios.
- **Límites con `Field`:** el año debe estar entre 1950 y 2030; título, género y plataforma no pueden estar vacíos y tienen longitud máxima. Los valores inválidos devuelven 422.
- **Sin duplicados:** no se puede agregar (ni renombrar a) un título que ya esté en el catálogo; devuelve 409.
