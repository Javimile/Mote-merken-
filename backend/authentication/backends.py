from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.db import connection, transaction

from .models import Usuario


class UsuarioBackend:
    def authenticate(self, request, username=None, password=None, **kwargs):
        correo = username or kwargs.get("email")

        if not correo or not password:
            return None

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT u.usr_id_usr
                FROM public.usr u
                INNER JOIN public.per p
                    ON p.per_id_per = u.usr_id_per
                WHERE LOWER(TRIM(p.per_cor_per)) = LOWER(TRIM(%s))
                  AND u.usr_est_usr = TRUE
                LIMIT 1
                """,
                [correo],
            )
            fila = cursor.fetchone()

        if not fila:
            return None

        try:
            usuario = Usuario.objects.get(
                usr_id_usr=fila[0],
                usr_est_usr=True,
            )
        except Usuario.DoesNotExist:
            return None

        valor_guardado = usuario.usr_con_has

        if not valor_guardado:
            return None

        # Primero, intentamos validar como hash de Django.
        try:
            coincide = check_password(password, valor_guardado)
        except (ValueError, TypeError):
            coincide = False

        if coincide:
            return usuario

        # Compatibilidad temporal para las contraseñas antiguas
        # en texto plano. Solo se permite en desarrollo.
        if not settings.DEBUG or password != valor_guardado:
            return None

        # Convertimos la contraseña antigua a un hash de Django.
        nuevo_hash = make_password(password)

        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE public.usr
                    SET usr_con_has = %s
                    WHERE usr_id_usr = %s
                      AND usr_con_has = %s
                      AND usr_est_usr = TRUE
                    """,
                    [nuevo_hash, usuario.usr_id_usr, valor_guardado],
                )

                actualizadas = cursor.rowcount

        if actualizadas != 1:
            return None

        usuario.usr_con_has = nuevo_hash
        return usuario

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(
                usr_id_usr=user_id,
                usr_est_usr=True,
            )
        except (Usuario.DoesNotExist, ValueError, TypeError):
            return None


