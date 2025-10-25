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
            """
            DO $$
            BEGIN
                IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'calificaciones_user_id_c4f549bc_fk_auth_user_id') THEN
                    ALTER TABLE calificaciones DROP CONSTRAINT calificaciones_user_id_c4f549bc_fk_auth_user_id;
                    ALTER TABLE calificaciones ADD CONSTRAINT calificaciones_user_id_c4f549bc_fk_users_users_id FOREIGN KEY (user_id) REFERENCES users_users(id);
                END IF;
            END $$;
            """,
            reverse_sql="""
            DO $$
            BEGIN
                IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'calificaciones_user_id_c4f549bc_fk_users_users_id') THEN
                    ALTER TABLE calificaciones DROP CONSTRAINT calificaciones_user_id_c4f549bc_fk_users_users_id;
                    ALTER TABLE calificaciones ADD CONSTRAINT calificaciones_user_id_c4f549bc_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id);
                END IF;
            END $$;
            """
        ),
        migrations.RunSQL(
            """
            DO $$
            BEGIN
                IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'cuestionarios_autor_id_85c92de0_fk_auth_user_id') THEN
                    ALTER TABLE cuestionarios DROP CONSTRAINT cuestionarios_autor_id_85c92de0_fk_auth_user_id;
                    ALTER TABLE cuestionarios ADD CONSTRAINT cuestionarios_autor_id_85c92de0_fk_users_users_id FOREIGN KEY (autor_id) REFERENCES users_users(id);
                END IF;
            END $$;
            """,
            reverse_sql="""
            DO $$
            BEGIN
                IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'cuestionarios_autor_id_85c92de0_fk_users_users_id') THEN
                    ALTER TABLE cuestionarios DROP CONSTRAINT cuestionarios_autor_id_85c92de0_fk_users_users_id;
                    ALTER TABLE cuestionarios ADD CONSTRAINT cuestionarios_autor_id_85c92de0_fk_auth_user_id FOREIGN KEY (autor_id) REFERENCES auth_user(id);
                END IF;
            END $$;
            """
        ),
        migrations.RunSQL(
            """
            DO $$
            BEGIN
                IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'intentos_cuestionario_user_id_f8b618eb_fk_auth_user_id') THEN
                    ALTER TABLE intentos_cuestionario DROP CONSTRAINT intentos_cuestionario_user_id_f8b618eb_fk_auth_user_id;
                    ALTER TABLE intentos_cuestionario ADD CONSTRAINT intentos_cuestionario_user_id_f8b618eb_fk_users_users_id FOREIGN KEY (user_id) REFERENCES users_users(id);
                END IF;
            END $$;
            """,
            reverse_sql="""
            DO $$
            BEGIN
                IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'intentos_cuestionario_user_id_f8b618eb_fk_users_users_id') THEN
                    ALTER TABLE intentos_cuestionario DROP CONSTRAINT intentos_cuestionario_user_id_f8b618eb_fk_users_users_id;
                    ALTER TABLE intentos_cuestionario ADD CONSTRAINT intentos_cuestionario_user_id_f8b618eb_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id);
                END IF;
            END $$;
            """
        ),
        migrations.RunSQL(
            """
            DO $$
            BEGIN
                IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'preguntas_autor_id_ccdaf78c_fk_auth_user_id') THEN
                    ALTER TABLE preguntas DROP CONSTRAINT preguntas_autor_id_ccdaf78c_fk_auth_user_id;
                    ALTER TABLE preguntas ADD CONSTRAINT preguntas_autor_id_ccdaf78c_fk_users_users_id FOREIGN KEY (autor_id) REFERENCES users_users(id);
                END IF;
            END $$;
            """,
            reverse_sql="""
            DO $$
            BEGIN
                IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'preguntas_autor_id_ccdaf78c_fk_users_users_id') THEN
                    ALTER TABLE preguntas DROP CONSTRAINT preguntas_autor_id_ccdaf78c_fk_users_users_id;
                    ALTER TABLE preguntas ADD CONSTRAINT preguntas_autor_id_ccdaf78c_fk_auth_user_id FOREIGN KEY (autor_id) REFERENCES auth_user(id);
                END IF;
            END $$;
            """
        ),
        migrations.RunSQL(
            """
            DO $$
            BEGIN
                IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'comentarios_user_id_36fc42f5_fk_auth_user_id') THEN
                    ALTER TABLE comentarios DROP CONSTRAINT comentarios_user_id_36fc42f5_fk_auth_user_id;
                    ALTER TABLE comentarios ADD CONSTRAINT comentarios_user_id_36fc42f5_fk_users_users_id FOREIGN KEY (user_id) REFERENCES users_users(id);
                END IF;
            END $$;
            """,
            reverse_sql="""
            DO $$
            BEGIN
                IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'comentarios_user_id_36fc42f5_fk_users_users_id') THEN
                    ALTER TABLE comentarios DROP CONSTRAINT comentarios_user_id_36fc42f5_fk_users_users_id;
                    ALTER TABLE comentarios ADD CONSTRAINT comentarios_user_id_36fc42f5_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id);
                END IF;
            END $$;
            """
        ),
        migrations.RunSQL(
            """
            DO $$
            BEGIN
                IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'user_videos_cursos_user_id_f1eeac73_fk_auth_user_id') THEN
                    ALTER TABLE user_videos_cursos DROP CONSTRAINT user_videos_cursos_user_id_f1eeac73_fk_auth_user_id;
                    ALTER TABLE user_videos_cursos ADD CONSTRAINT user_videos_cursos_user_id_f1eeac73_fk_users_users_id FOREIGN KEY (user_id) REFERENCES users_users(id);
                END IF;
            END $$;
            """,
            reverse_sql="""
            DO $$
            BEGIN
                IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'user_videos_cursos_user_id_f1eeac73_fk_users_users_id') THEN
                    ALTER TABLE user_videos_cursos DROP CONSTRAINT user_videos_cursos_user_id_f1eeac73_fk_users_users_id;
                    ALTER TABLE user_videos_cursos ADD CONSTRAINT user_videos_cursos_user_id_f1eeac73_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id);
                END IF;
            END $$;
            """
        ),
    ]