import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.db import connection


tablas_necesarias = [
    "django_session",
    "django_migrations",
    "django_content_type",
    "auth_permission",
]


with connection.cursor() as cursor:
    tablas_existentes = set(
        connection.introspection.table_names(cursor)
    )


print("\nEstado de las tablas de Django:\n")

for tabla in tablas_necesarias:
    estado = "EXISTE" if tabla in tablas_existentes else "NO EXISTE"
    print(f"{tabla}: {estado}")

print()