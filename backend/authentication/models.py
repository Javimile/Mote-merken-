from django.db import models
from django.utils.crypto import salted_hmac


class Usuario(models.Model):
    usr_id_usr = models.BigAutoField(
        primary_key=True,
        db_column="usr_id_usr",
    )
    usr_id_per = models.BigIntegerField(db_column="usr_id_per")
    usr_nom_usr = models.CharField(max_length=50, db_column="usr_nom_usr")
    usr_con_has = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_column="usr_con_has",
    )
    usr_est_usr = models.BooleanField(db_column="usr_est_usr")
    usr_fec_reg = models.DateTimeField(db_column="usr_fec_reg")

    class Meta:
        managed = False
        db_table = "usr"

    @property
    def correo(self):
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT per_cor_per
                FROM public.per
                WHERE per_id_per = %s
                """,
                [self.usr_id_per],
            )
            resultado = cursor.fetchone()

        return resultado[0] if resultado else None

    @property
    def nombre_persona(self):
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT per_nom_per
                FROM public.per
                WHERE per_id_per = %s
                """,
                [self.usr_id_per],
            )
            resultado = cursor.fetchone()

        return resultado[0] if resultado else None

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_active(self):
        return self.usr_est_usr

    def get_username(self):
        return self.usr_nom_usr

    def get_session_auth_hash(self):
        return salted_hmac(
            "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash",
            self.usr_con_has or "",
            algorithm="sha256",
        ).hexdigest()

    def save(self, *args, **kwargs):
        update_fields = kwargs.get("update_fields")

        if update_fields and "last_login" in update_fields:
            return

        super().save(*args, **kwargs)


class Itinerario(models.Model):
    iti_id_iti = models.BigAutoField(
        primary_key=True,
        db_column="iti_id_iti",
    )
    iti_id_tou = models.BigIntegerField(
        db_column="iti_id_tou",
        unique=True,
    )
    iti_tit_iti = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        db_column="iti_tit_iti",
    )
    iti_des_gen = models.TextField(
        null=True,
        blank=True,
        db_column="iti_des_gen",
    )

    class Meta:
        managed = False
        db_table = "iti"

# itinerarios
class ItinerarioDetalle(models.Model):
    itd_id_itd = models.BigAutoField(
        primary_key=True,
        db_column="itd_id_itd",
    )
    itd_id_iti = models.BigIntegerField(
        db_column="itd_id_iti",
    )
    itd_dia_num = models.SmallIntegerField(
        db_column="itd_dia_num",
    )
    itd_ord_itd = models.SmallIntegerField(
        db_column="itd_ord_itd",
    )
    itd_tit_itd = models.CharField(
        max_length=150,
        db_column="itd_tit_itd",
    )
    itd_des_itd = models.TextField(
        null=True,
        blank=True,
        db_column="itd_des_itd",
    )
    itd_hor_ref = models.TimeField(
        null=True,
        blank=True,
        db_column="itd_hor_ref",
    )

    class Meta:
        managed = False
        db_table = "iti_det"
