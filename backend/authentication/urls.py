from django.urls import path
from . import views


urlpatterns = [
    path("roles/usuario/", views.usuario_roles_view, name="usuario_roles"),
    path("usuarios/buscar/", views.buscar_usuarios_view, name="buscar_usuarios"),
    path("roles/gestionar/", views.gestionar_rol, name="gestionar_rol"),
    path("me/", views.me_view, name="me"),
    path("csrf/", views.csrf_token, name="csrf_token"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("admin-test/", views.admin_test, name="admin_test"),
    path("roles/", views.roles_view, name="roles"),

    # Itinerarios

    path(
    "tours/admin/",
    views.tours_admin_view,
    name="tours_admin",
),
    path(
        "tours/<int:tour_id>/itinerario/",
        views.itinerario_por_tour_view,
        name="itinerario_por_tour",
    ),
    path(
        "itinerarios/",
        views.crear_itinerario_view,
        name="crear_itinerario",
        
    ),
    path(
        "itinerarios/<int:itinerario_id>/actividades/",
         views.actividades_itinerario_view,
         name="actividades_itinerario",
       ),
    path(
       "itinerarios/<int:itinerario_id>/actividades/crear/",
        views.crear_actividad_view,
        name="crear_actividad",
          ),
    path(
    "itinerarios/<int:itinerario_id>/actividades/<int:actividad_id>/",
    views.editar_actividad_view,
    name="editar_actividad",
      ),
      path(
    "itinerarios/<int:itinerario_id>/actividades/<int:actividad_id>/eliminar/",
    views.eliminar_actividad_view,
    name="eliminar_actividad",
),
]


