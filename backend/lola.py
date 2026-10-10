import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()




from django.contrib.auth import authenticate
from django.contrib.auth.hashers import identify_hasher
from authentication.models import Usuario

correo = input("Correo: ").strip()
password = input("Contraseña de prueba: ")

usuario = authenticate(username=correo, password=password)

print("Autenticación:", usuario is not None)

if usuario:
    print("ID:", usuario.usr_id_usr)
    print("Username:", usuario.get_username())
    print("Correo:", usuario.correo)
    print("Activo:", usuario.is_active)

    usuario.refresh_from_db()

    try:
        print("Algoritmo guardado:", identify_hasher(usuario.usr_con_has).algorithm)
    except ValueError:
        print("La contraseña aún no tiene un formato de hash reconocido.")