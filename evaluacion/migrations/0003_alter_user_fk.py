# Generated manually to alter FK to users

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evaluacion', '0002_initial'),
        ('users', '0001_initial'),
        ('contenidos', '0001_initial'),
        ('seguimiento', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            "ALTER TABLE auth_user_groups DROP CONSTRAINT IF EXISTS auth_user_groups_user_id_6a12ed8b_fk_auth_user_id;",
            reverse_sql="ALTER TABLE auth_user_groups ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id);"
        ),
        migrations.RunSQL(
            "ALTER TABLE auth_user_groups ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_users_users_id FOREIGN KEY (user_id) REFERENCES users_users(id);",
            reverse_sql="ALTER TABLE auth_user_groups DROP CONSTRAINT IF EXISTS auth_user_groups_user_id_6a12ed8b_fk_users_users_id;"
        ),
        migrations.RunSQL(
            "ALTER TABLE auth_user_user_permissions DROP CONSTRAINT IF EXISTS auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id;",
            reverse_sql="ALTER TABLE auth_user_user_permissions ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id);"
        ),
        migrations.RunSQL(
            "ALTER TABLE auth_user_user_permissions ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_users_users_id FOREIGN KEY (user_id) REFERENCES users_users(id);",
            reverse_sql="ALTER TABLE auth_user_user_permissions DROP CONSTRAINT IF EXISTS auth_user_user_permissions_user_id_a95ead1b_fk_users_users_id;"
        ),
        migrations.RunSQL(
            "ALTER TABLE django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_user_id_c564eba6_fk_auth_user_id;",
            reverse_sql="ALTER TABLE django_admin_log ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id);"
        ),
        migrations.RunSQL(
            "ALTER TABLE django_admin_log ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_users_users_id FOREIGN KEY (user_id) REFERENCES users_users(id);",
            reverse_sql="ALTER TABLE django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_user_id_c564eba6_fk_users_users_id;"
        ),
        migrations.RunSQL(
            "ALTER TABLE calificaciones DROP CONSTRAINT IF EXISTS calificaciones_user_id_c4f549bc_fk_auth_user_id;",
            reverse_sql="ALTER TABLE calificaciones ADD CONSTRAINT calificaciones_user_id_c4f549bc_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id);"
        ),
        migrations.RunSQL(
            "ALTER TABLE calificaciones ADD CONSTRAINT calificaciones_user_id_c4f549bc_fk_users_users_id FOREIGN KEY (user_id) REFERENCES users_users(id);",
            reverse_sql="ALTER TABLE calificaciones DROP CONSTRAINT IF EXISTS calificaciones_user_id_c4f549bc_fk_users_users_id;"
        ),
        migrations.RunSQL(
            "ALTER TABLE cuestionarios DROP CONSTRAINT IF EXISTS cuestionarios_autor_id_85c92de0_fk_auth_user_id;",
            reverse_sql="ALTER TABLE cuestionarios ADD CONSTRAINT cuestionarios_autor_id_85c92de0_fk_auth_user_id FOREIGN KEY (autor_id) REFERENCES auth_user(id);"
        ),
        migrations.RunSQL(
            "ALTER TABLE cuestionarios ADD CONSTRAINT cuestionarios_autor_id_85c92de0_fk_users_users_id FOREIGN KEY (autor_id) REFERENCES users_users(id);",
            reverse_sql="ALTER TABLE cuestionarios DROP CONSTRAINT IF EXISTS cuestionarios_autor_id_85c92de0_fk_users_users_id;"
        ),
        migrations.RunSQL(
            "ALTER TABLE intentos_cuestionario DROP CONSTRAINT IF EXISTS intentos_cuestionario_user_id_f8b618eb_fk_auth_user_id;",
            reverse_sql="ALTER TABLE intentos_cuestionario ADD CONSTRAINT intentos_cuestionario_user_id_f8b618eb_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id);"
        ),
        migrations.RunSQL(
            "ALTER TABLE intentos_cuestionario ADD CONSTRAINT intentos_cuestionario_user_id_f8b618eb_fk_users_users_id FOREIGN KEY (user_id) REFERENCES users_users(id);",
            reverse_sql="ALTER TABLE intentos_cuestionario DROP CONSTRAINT IF EXISTS intentos_cuestionario_user_id_f8b618eb_fk_users_users_id;"
        ),
        migrations.RunSQL(
            "ALTER TABLE preguntas DROP CONSTRAINT IF EXISTS preguntas_autor_id_ccdaf78c_fk_auth_user_id;",
            reverse_sql="ALTER TABLE preguntas ADD CONSTRAINT preguntas_autor_id_ccdaf78c_fk_auth_user_id FOREIGN KEY (autor_id) REFERENCES auth_user(id);"
        ),
        migrations.RunSQL(
            "ALTER TABLE preguntas ADD CONSTRAINT preguntas_autor_id_ccdaf78c_fk_users_users_id FOREIGN KEY (autor_id) REFERENCES users_users(id);",
            reverse_sql="ALTER TABLE preguntas DROP CONSTRAINT IF EXISTS preguntas_autor_id_ccdaf78c_fk_users_users_id;"
        ),
        migrations.RunSQL(
            "ALTER TABLE comentarios DROP CONSTRAINT IF EXISTS comentarios_user_id_36fc42f5_fk_auth_user_id;",
            reverse_sql="ALTER TABLE comentarios ADD CONSTRAINT comentarios_user_id_36fc42f5_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id);"
        ),
        migrations.RunSQL(
            "ALTER TABLE comentarios ADD CONSTRAINT comentarios_user_id_36fc42f5_fk_users_users_id FOREIGN KEY (user_id) REFERENCES users_users(id);",
            reverse_sql="ALTER TABLE comentarios DROP CONSTRAINT IF EXISTS comentarios_user_id_36fc42f5_fk_users_users_id;"
        ),
        migrations.RunSQL(
            "ALTER TABLE user_videos_cursos DROP CONSTRAINT IF EXISTS user_videos_cursos_user_id_f1eeac73_fk_auth_user_id;",
            reverse_sql="ALTER TABLE user_videos_cursos ADD CONSTRAINT user_videos_cursos_user_id_f1eeac73_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id);"
        ),
        migrations.RunSQL(
            "ALTER TABLE user_videos_cursos ADD CONSTRAINT user_videos_cursos_user_id_f1eeac73_fk_users_users_id FOREIGN KEY (user_id) REFERENCES users_users(id);",
            reverse_sql="ALTER TABLE user_videos_cursos DROP CONSTRAINT IF EXISTS user_videos_cursos_user_id_f1eeac73_fk_users_users_id;"
        ),
    ]