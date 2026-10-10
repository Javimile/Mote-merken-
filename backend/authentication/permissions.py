from functools import wraps

from django.http import JsonResponse
from django.db import connection


def usuario_tiene_rol(usuario, *roles):
    if not usuario or not usuario.is_authenticated:
        return False

    if not roles:
        return False

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT 1
            FROM public.usr_rol ur
            INNER JOIN public.rol r
                ON r.rol_id_rol = ur.uro_id_rol
            WHERE ur.uro_id_usr = %s
              AND r.rol_est_rol = TRUE
              AND LOWER(r.rol_nom_rol) = ANY(%s)
            LIMIT 1
            """,
            [
                usuario.usr_id_usr,
                [rol.strip().lower() for rol in roles],
            ],
        )

        return cursor.fetchone() is not None


def requiere_rol(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return JsonResponse(
                    {
                        "error": "Debes iniciar sesión."
                    },
                    status=401,
                )

            if not usuario_tiene_rol(request.user, *roles):
                return JsonResponse(
                    {
                        "error": "No tienes permisos para realizar esta acción."
                    },
                    status=403,
                )

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator



def obtener_roles_usuario(usuario):
    if not usuario or not usuario.is_authenticated:
        return []

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT r.rol_nom_rol
            FROM public.usr_rol ur
            INNER JOIN public.rol r
                ON r.rol_id_rol = ur.uro_id_rol
            WHERE ur.uro_id_usr = %s
              AND r.rol_est_rol = TRUE
            ORDER BY r.rol_id_rol
            """,
            [usuario.usr_id_usr],
        )

        return [fila[0] for fila in cursor.fetchall()]


def obtener_roles_usuario(usuario):
    if not usuario or not usuario.is_authenticated:
        return []

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT r.rol_nom_rol
            FROM public.usr_rol ur
            INNER JOIN public.rol r
                ON r.rol_id_rol = ur.uro_id_rol
            WHERE ur.uro_id_usr = %s
              AND r.rol_est_rol = TRUE
            ORDER BY r.rol_id_rol
            """,
            [usuario.usr_id_usr],
        )

        return [fila[0] for fila in cursor.fetchall()]