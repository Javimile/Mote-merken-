import json
from django.db import connection

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from .permissions import obtener_roles_usuario, requiere_rol



@require_GET
@ensure_csrf_cookie
def csrf_token(request):
    return JsonResponse({
        "csrfToken": get_token(request)
    })


@require_POST
def login_view(request):
    try:
        datos = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"error": "El cuerpo de la solicitud no es JSON válido."},
            status=400,
        )

    if not isinstance(datos, dict):
        return JsonResponse(
            {"error": "El cuerpo debe ser un objeto JSON."},
            status=400,
        )

    correo = datos.get("correo", "")
    password = datos.get("password", "")

    if not isinstance(correo, str) or not isinstance(password, str):
        return JsonResponse(
            {"error": "Correo o contraseña inválidos."},
            status=400,
        )

    correo = correo.strip()

    if not correo or not password:
        return JsonResponse(
            {"error": "Debes ingresar correo y contraseña."},
            status=400,
        )

    usuario = authenticate(
        request,
        username=correo,
        password=password,
    )

    if usuario is None:
        return JsonResponse(
            {"error": "Correo o contraseña incorrectos."},
            status=401,
        )

    login(request, usuario)

    return JsonResponse({
        "mensaje": "Inicio de sesión correcto.",
        "usuario": {
            "id": usuario.usr_id_usr,
            "username": usuario.usr_nom_usr,
            "nombre": usuario.nombre_persona,
            "correo": usuario.correo,
        },
    })


@require_POST
def logout_view(request):
    logout(request)

    return JsonResponse({
        "mensaje": "Sesión cerrada correctamente."
    })


@require_GET
@requiere_rol("Admin")
def admin_test(request):
    return JsonResponse({
        "mensaje": "Tienes permisos de administrador.",
        "usuario": request.user.usr_nom_usr,
    })

@require_GET
def me_view(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {
                "autenticado": False,
                "usuario": None,
            },
            status=401,
        )

    roles = obtener_roles_usuario(request.user)

    return JsonResponse({
        "autenticado": True,
        "usuario": {
            "id": request.user.usr_id_usr,
            "username": request.user.usr_nom_usr,
            "nombre": request.user.nombre_persona,
            "correo": request.user.correo,
            "roles": roles,
        },
    })

@require_POST
@requiere_rol("Admin")
def gestionar_rol(request):
    try:
        datos = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"error": "El cuerpo de la solicitud no es JSON válido."},
            status=400,
        )

    if not isinstance(datos, dict):
        return JsonResponse(
            {"error": "El cuerpo debe ser un objeto JSON."},
            status=400,
        )

    accion = datos.get("accion")
    usuario_id = datos.get("usuario")
    rol_id = datos.get("rol")

    if accion not in ("asignar", "revocar"):
        return JsonResponse(
            {"error": "Acción inválida."},
            status=400,
        )

    try:
        usuario_id = int(usuario_id)
        rol_id = int(rol_id)
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "Usuario o rol inválido."},
            status=400,
        )

    with connection.cursor() as cursor:

        # Verificar usuario
        cursor.execute(
            """
            SELECT usr_id_usr
            FROM public.usr
            WHERE usr_id_usr = %s
            """,
            [usuario_id],
        )

        if cursor.fetchone() is None:
            return JsonResponse(
                {"error": "El usuario no existe."},
                status=404,
            )

        # Verificar rol
        cursor.execute(
            """
            SELECT rol_id_rol, rol_nom_rol
            FROM public.rol
            WHERE rol_id_rol = %s
              AND rol_est_rol = TRUE
            """,
            [rol_id],
        )

        rol = cursor.fetchone()

        if rol is None:
            return JsonResponse(
                {"error": "El rol no existe o está inactivo."},
                status=404,
            )

        if accion == "asignar":
            cursor.execute(
                """
                SELECT 1
                FROM public.usr_rol
                WHERE uro_id_usr = %s
                  AND uro_id_rol = %s
                """,
                [usuario_id, rol_id],
            )

            if cursor.fetchone():
                return JsonResponse(
                    {
                        "error": "El usuario ya tiene este rol."
                    },
                    status=409,
                )

            cursor.execute(
                """
                INSERT INTO public.usr_rol (
                    uro_id_usr,
                    uro_id_rol
                )
                VALUES (%s, %s)
                """,
                [usuario_id, rol_id],
            )

            return JsonResponse({
                "mensaje": "Rol asignado correctamente.",
                "usuario": usuario_id,
                "rol": {
                    "id": rol[0],
                    "nombre": rol[1],
                },
            })

        # Revocar
        cursor.execute(
            """
            DELETE FROM public.usr_rol
            WHERE uro_id_usr = %s
              AND uro_id_rol = %s
            """,
            [usuario_id, rol_id],
        )

        if cursor.rowcount == 0:
            return JsonResponse(
                {"error": "El usuario no tiene ese rol."},
                status=404,
            )

        return JsonResponse({
            "mensaje": "Rol revocado correctamente.",
            "usuario": usuario_id,
            "rol": {
                "id": rol[0],
                "nombre": rol[1],
            },
        })



@require_GET
@requiere_rol("Admin")
def usuario_roles_view(request):
    usuario_id = request.GET.get("usuario")

    try:
        usuario_id = int(usuario_id)
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "Usuario inválido."},
            status=400,
        )

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                r.rol_id_rol,
                r.rol_nom_rol
            FROM public.usr_rol ur
            INNER JOIN public.rol r
                ON r.rol_id_rol = ur.uro_id_rol
            WHERE ur.uro_id_usr = %s
              AND r.rol_est_rol = TRUE
            ORDER BY r.rol_id_rol
            """,
            [usuario_id],
        )

        roles = [
            {
                "rol_id_rol": fila[0],
                "rol_nom_rol": fila[1],
            }
            for fila in cursor.fetchall()
        ]

    return JsonResponse(roles, safe=False)


@require_GET
@requiere_rol("Admin")
def buscar_usuarios_view(request):
    buscar = request.GET.get("buscar", "").strip()

    if len(buscar) < 2:
        return JsonResponse([], safe=False)

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                u.usr_id_usr,
                u.usr_nom_usr,
                p.per_cor_per
            FROM public.usr u
            INNER JOIN public.per p
                ON p.per_id_per = u.usr_id_per
            WHERE
                LOWER(u.usr_nom_usr) LIKE LOWER(%s)
                OR LOWER(p.per_cor_per) LIKE LOWER(%s)
            ORDER BY u.usr_nom_usr
            LIMIT 10
            """,
            [
                f"%{buscar}%",
                f"%{buscar}%",
            ],
        )

        usuarios = [
            {
                "usr_id_usr": fila[0],
                "usr_nom_usr": fila[1],
                "per_cor_per": fila[2],
            }
            for fila in cursor.fetchall()
        ]

    return JsonResponse(usuarios, safe=False)

@require_GET
@requiere_rol("Admin")
def roles_view(request):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT rol_id_rol, rol_nom_rol
            FROM public.rol
            WHERE rol_est_rol = TRUE
            ORDER BY rol_id_rol
            """
        )

        roles = [
            {
                "rol_id_rol": fila[0],
                "rol_nom_rol": fila[1],
            }
            for fila in cursor.fetchall()
        ]

    return JsonResponse(roles, safe=False)

#itinerarios

@require_GET
def itinerario_por_tour_view(request, tour_id):
    try:
        tour_id = int(tour_id)
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "Tour inválido."},
            status=400,
        )

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                iti_id_iti,
                iti_id_tou,
                iti_tit_iti,
                iti_des_gen
            FROM public.iti
            WHERE iti_id_tou = %s
            """,
            [tour_id],
        )

        itinerario = cursor.fetchone()

    if itinerario is None:
        return JsonResponse(
            {"error": "El tour no tiene un itinerario."},
            status=404,
        )

    return JsonResponse({
        "iti_id_iti": itinerario[0],
        "iti_id_tou": itinerario[1],
        "iti_tit_iti": itinerario[2],
        "iti_des_gen": itinerario[3],
    })


@require_POST
def crear_itinerario_view(request):
    try:
        datos = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"error": "El cuerpo de la solicitud no es JSON válido."},
            status=400,
        )

    if not isinstance(datos, dict):
        return JsonResponse(
            {"error": "El cuerpo debe ser un objeto JSON."},
            status=400,
        )

    tour_id = datos.get("iti_id_tou")
    titulo = datos.get("iti_tit_iti")
    descripcion = datos.get("iti_des_gen")

    try:
        tour_id = int(tour_id)
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "Tour inválido."},
            status=400,
        )

    if titulo is not None and not isinstance(titulo, str):
        return JsonResponse(
            {"error": "El título debe ser texto."},
            status=400,
        )

    if descripcion is not None and not isinstance(descripcion, str):
        return JsonResponse(
            {"error": "La descripción debe ser texto."},
            status=400,
        )

    with connection.cursor() as cursor:

        # Verificar que el tour exista
        cursor.execute(
            """
            SELECT tou_id_tou
            FROM public.tou
            WHERE tou_id_tou = %s
            """,
            [tour_id],
        )

        if cursor.fetchone() is None:
            return JsonResponse(
                {"error": "El tour no existe."},
                status=404,
            )

        # Verificar que el tour no tenga ya un itinerario
        cursor.execute(
            """
            SELECT iti_id_iti
            FROM public.iti
            WHERE iti_id_tou = %s
            """,
            [tour_id],
        )

        if cursor.fetchone() is not None:
            return JsonResponse(
                {"error": "El tour ya tiene un itinerario."},
                status=409,
            )

        # Crear itinerario
        cursor.execute(
            """
            INSERT INTO public.iti (
                iti_id_tou,
                iti_tit_iti,
                iti_des_gen
            )
            VALUES (%s, %s, %s)
            RETURNING
                iti_id_iti,
                iti_id_tou,
                iti_tit_iti,
                iti_des_gen
            """,
            [
                tour_id,
                titulo,
                descripcion,
            ],
        )

        itinerario = cursor.fetchone()

    return JsonResponse(
        {
            "mensaje": "Itinerario creado correctamente.",
            "itinerario": {
                "iti_id_iti": itinerario[0],
                "iti_id_tou": itinerario[1],
                "iti_tit_iti": itinerario[2],
                "iti_des_gen": itinerario[3],
            },
        },
        status=201,
    )


@require_GET
def actividades_itinerario_view(request, itinerario_id):
    try:
        itinerario_id = int(itinerario_id)
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "Itinerario inválido."},
            status=400,
        )

    with connection.cursor() as cursor:
        # Verificar que el itinerario exista
        cursor.execute(
            """
            SELECT iti_id_iti
            FROM public.iti
            WHERE iti_id_iti = %s
            """,
            [itinerario_id],
        )

        if cursor.fetchone() is None:
            return JsonResponse(
                {"error": "El itinerario no existe."},
                status=404,
            )

        # Obtener actividades ordenadas por día y orden
        cursor.execute(
            """
            SELECT
                itd_id_itd,
                itd_id_iti,
                itd_dia_num,
                itd_ord_itd,
                itd_tit_itd,
                itd_des_itd,
                itd_hor_ref
            FROM public.iti_det
            WHERE itd_id_iti = %s
            ORDER BY itd_dia_num, itd_ord_itd
            """,
            [itinerario_id],
        )

        actividades = [
            {
                "itd_id_itd": fila[0],
                "itd_id_iti": fila[1],
                "itd_dia_num": fila[2],
                "itd_ord_itd": fila[3],
                "itd_tit_itd": fila[4],
                "itd_des_itd": fila[5],
                "itd_hor_ref": fila[6].strftime("%H:%M:%S") if fila[6] else None,
            }
            for fila in cursor.fetchall()
        ]

    return JsonResponse(actividades, safe=False)


@require_POST
def crear_actividad_view(request, itinerario_id):
    try:
        itinerario_id = int(itinerario_id)
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "Itinerario inválido."},
            status=400,
        )

    try:
        datos = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"error": "El cuerpo de la solicitud no es JSON válido."},
            status=400,
        )

    if not isinstance(datos, dict):
        return JsonResponse(
            {"error": "El cuerpo debe ser un objeto JSON."},
            status=400,
        )

    dia_num = datos.get("itd_dia_num")
    orden = datos.get("itd_ord_itd")
    titulo = datos.get("itd_tit_itd")
    descripcion = datos.get("itd_des_itd")
    hora = datos.get("itd_hor_ref")

    # Validar día
    try:
        dia_num = int(dia_num)
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "El número de día es inválido."},
            status=400,
        )

    if dia_num < 1:
        return JsonResponse(
            {"error": "El número de día debe ser mayor o igual a 1."},
            status=400,
        )

    # Validar orden
    try:
        orden = int(orden)
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "El orden de la actividad es inválido."},
            status=400,
        )

    if orden < 1:
        return JsonResponse(
            {"error": "El orden debe ser mayor o igual a 1."},
            status=400,
        )

    # Validar título
    if not isinstance(titulo, str) or not titulo.strip():
        return JsonResponse(
            {"error": "El título de la actividad es obligatorio."},
            status=400,
        )

    titulo = titulo.strip()

    # Validar descripción
    if descripcion is not None and not isinstance(descripcion, str):
        return JsonResponse(
            {"error": "La descripción debe ser texto."},
            status=400,
        )

    # Validar hora
    if hora is not None and not isinstance(hora, str):
        return JsonResponse(
            {"error": "La hora debe tener formato HH:MM o HH:MM:SS."},
            status=400,
        )

    with connection.cursor() as cursor:

        # Verificar que el itinerario exista
        cursor.execute(
            """
            SELECT iti_id_iti
            FROM public.iti
            WHERE iti_id_iti = %s
            """,
            [itinerario_id],
        )

        if cursor.fetchone() is None:
            return JsonResponse(
                {"error": "El itinerario no existe."},
                status=404,
            )

        # Verificar que el orden no esté ocupado dentro del mismo día
        cursor.execute(
            """
            SELECT itd_id_itd
            FROM public.iti_det
            WHERE itd_id_iti = %s
              AND itd_dia_num = %s
              AND itd_ord_itd = %s
            """,
            [
                itinerario_id,
                dia_num,
                orden,
            ],
        )

        if cursor.fetchone() is not None:
            return JsonResponse(
                {
                    "error": (
                        "Ya existe una actividad con ese orden "
                        "para ese día del itinerario."
                    )
                },
                status=409,
            )

        # Insertar actividad
        cursor.execute(
            """
            INSERT INTO public.iti_det (
                itd_id_iti,
                itd_dia_num,
                itd_ord_itd,
                itd_tit_itd,
                itd_des_itd,
                itd_hor_ref
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING
                itd_id_itd,
                itd_id_iti,
                itd_dia_num,
                itd_ord_itd,
                itd_tit_itd,
                itd_des_itd,
                itd_hor_ref
            """,
            [
                itinerario_id,
                dia_num,
                orden,
                titulo,
                descripcion,
                hora,
            ],
        )

        actividad = cursor.fetchone()

    return JsonResponse(
        {
            "mensaje": "Actividad creada correctamente.",
            "actividad": {
                "itd_id_itd": actividad[0],
                "itd_id_iti": actividad[1],
                "itd_dia_num": actividad[2],
                "itd_ord_itd": actividad[3],
                "itd_tit_itd": actividad[4],
                "itd_des_itd": actividad[5],
                "itd_hor_ref": (
                    actividad[6].strftime("%H:%M:%S")
                    if actividad[6]
                    else None
                ),
            },
        },
        status=201,
    )
@require_http_methods(["PUT"])
def editar_actividad_view(request, itinerario_id, actividad_id):
    try:
        itinerario_id = int(itinerario_id)
        actividad_id = int(actividad_id)
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "Itinerario o actividad inválidos."},
            status=400,
        )

    try:
        datos = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"error": "El cuerpo de la solicitud no es JSON válido."},
            status=400,
        )

    if not isinstance(datos, dict):
        return JsonResponse(
            {"error": "El cuerpo debe ser un objeto JSON."},
            status=400,
        )

    dia_num = datos.get("itd_dia_num")
    orden = datos.get("itd_ord_itd")
    titulo = datos.get("itd_tit_itd")
    descripcion = datos.get("itd_des_itd")
    hora = datos.get("itd_hor_ref")

    try:
        dia_num = int(dia_num)
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "El número de día es inválido."},
            status=400,
        )

    if dia_num < 1:
        return JsonResponse(
            {"error": "El número de día debe ser mayor o igual a 1."},
            status=400,
        )

    try:
        orden = int(orden)
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "El orden de la actividad es inválido."},
            status=400,
        )

    if orden < 1:
        return JsonResponse(
            {"error": "El orden debe ser mayor o igual a 1."},
            status=400,
        )

    if not isinstance(titulo, str) or not titulo.strip():
        return JsonResponse(
            {"error": "El título de la actividad es obligatorio."},
            status=400,
        )

    titulo = titulo.strip()

    if descripcion is not None and not isinstance(descripcion, str):
        return JsonResponse(
            {"error": "La descripción debe ser texto."},
            status=400,
        )

    if hora is not None and not isinstance(hora, str):
        return JsonResponse(
            {"error": "La hora debe tener formato HH:MM o HH:MM:SS."},
            status=400,
        )

    with connection.cursor() as cursor:

        # Verificar que la actividad pertenezca al itinerario
        cursor.execute(
            """
            SELECT itd_id_itd
            FROM public.iti_det
            WHERE itd_id_itd = %s
              AND itd_id_iti = %s
            """,
            [actividad_id, itinerario_id],
        )

        if cursor.fetchone() is None:
            return JsonResponse(
                {"error": "La actividad no existe en este itinerario."},
                status=404,
            )

        # Evitar duplicar día + orden con otra actividad
        cursor.execute(
            """
            SELECT itd_id_itd
            FROM public.iti_det
            WHERE itd_id_iti = %s
              AND itd_dia_num = %s
              AND itd_ord_itd = %s
              AND itd_id_itd <> %s
            """,
            [
                itinerario_id,
                dia_num,
                orden,
                actividad_id,
            ],
        )

        if cursor.fetchone() is not None:
            return JsonResponse(
                {
                    "error": (
                        "Ya existe otra actividad con ese orden "
                        "para ese día del itinerario."
                    )
                },
                status=409,
            )

        # Actualizar actividad
        cursor.execute(
            """
            UPDATE public.iti_det
            SET
                itd_dia_num = %s,
                itd_ord_itd = %s,
                itd_tit_itd = %s,
                itd_des_itd = %s,
                itd_hor_ref = %s
            WHERE itd_id_itd = %s
              AND itd_id_iti = %s
            RETURNING
                itd_id_itd,
                itd_id_iti,
                itd_dia_num,
                itd_ord_itd,
                itd_tit_itd,
                itd_des_itd,
                itd_hor_ref
            """,
            [
                dia_num,
                orden,
                titulo,
                descripcion,
                hora,
                actividad_id,
                itinerario_id,
            ],
        )

        actividad = cursor.fetchone()

    return JsonResponse({
        "mensaje": "Actividad actualizada correctamente.",
        "actividad": {
            "itd_id_itd": actividad[0],
            "itd_id_iti": actividad[1],
            "itd_dia_num": actividad[2],
            "itd_ord_itd": actividad[3],
            "itd_tit_itd": actividad[4],
            "itd_des_itd": actividad[5],
            "itd_hor_ref": (
                actividad[6].strftime("%H:%M:%S")
                if actividad[6]
                else None
            ),
        },
        
    })
@require_http_methods(["DELETE"])
def eliminar_actividad_view(request, itinerario_id, actividad_id):
    try:
        itinerario_id = int(itinerario_id)
        actividad_id = int(actividad_id)
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "Itinerario o actividad inválidos."},
            status=400,
        )

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT itd_id_itd
            FROM public.iti_det
            WHERE itd_id_itd = %s
              AND itd_id_iti = %s
            """,
            [actividad_id, itinerario_id],
        )

        if cursor.fetchone() is None:
            return JsonResponse(
                {"error": "La actividad no existe en este itinerario."},
                status=404,
            )

        cursor.execute(
            """
            DELETE FROM public.iti_det
            WHERE itd_id_itd = %s
              AND itd_id_iti = %s
            """,
            [actividad_id, itinerario_id],
        )

    return JsonResponse({
        "mensaje": "Actividad eliminada correctamente."
    })

@require_GET
def tours_admin_view(request):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                tou_id_tou,
                tou_nom_tou,
                tou_des_tou,
                tou_dur_hor,
                tou_dur_dia,
                tou_cup_max,
                tou_est_tou,
                tou_fec_cre
            FROM public.tou
            ORDER BY tou_id_tou
            """
        )

        tours = [
            {
                "tou_id_tou": fila[0],
                "tou_nom_tou": fila[1],
                "tou_des_tou": fila[2],
                "tou_dur_hor": float(fila[3]) if fila[3] is not None else None,
                "tou_dur_dia": fila[4],
                "tou_cup_max": fila[5],
                "tou_est_tou": fila[6],
                "tou_fec_cre": fila[7].isoformat() if fila[7] else None,
            }
            for fila in cursor.fetchall()
        ]

    return JsonResponse(tours, safe=False)
