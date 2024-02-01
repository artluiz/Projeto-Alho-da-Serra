from django.db import connections, models
from .models import Estufa, Atividade, Produtos, TipoIrrigador, FichaDeAplicacao
from django.core.management import call_command
from .models import FichaDeAplicacao
from django.utils.timezone import make_aware
from django.utils import timezone
import pytz
import json
from datetime import datetime, date


class FichaDeAplicacaoRouter:
    """
    Um router para controlar todas as operações de banco de dados no modelo 'FichaDeAplicacao'.
    """

    def db_for_read(self, model, **hints):
        """
        As leituras vão para o banco de dados SQLite por padrão.
        """
        if model == FichaDeAplicacao:
            return "default"
        return None


class DatabaseSynchronizer:
    @staticmethod
    def sync_db():
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT * FROM todos_fichadeaplicacao ORDER BY id;")
            rows = cursor.fetchall()

        with connections["secondary"].cursor() as cursor:
            latest_date_in_database = FichaDeAplicacao.objects.using(
                "secondary"
            ).aggregate(models.Max("data_criada"))["data_criada__max"]
            if latest_date_in_database:
                latest_date_in_database = latest_date_in_database.astimezone(
                    pytz.timezone("Europe/London")
                )
            for row in rows:
                ficha_data_criada_utc = row[1].replace(tzinfo=pytz.UTC)
                ficha_data_criada = ficha_data_criada_utc.astimezone(
                    timezone.get_default_timezone()
                ).replace(tzinfo=timezone.get_default_timezone())
                ficha_data_atualizado = datetime.combine(row[11], datetime.min.time())
                if (
                    not latest_date_in_database
                    or ficha_data_criada > latest_date_in_database
                ):
                    area = row[2] if row[2] is not None else 0.0
                    dados = json.loads(row[3] if row[3] is not None else {})
                    data_aplicada = datetime.combine(row[4], datetime.min.time())
                    atividade_id = row[5] if row[5] is not None else 0
                    estufa_id = row[6] if row[6] is not None else 0
                    irrigador_id = row[7] if row[7] is not None else 0
                    ativo = row[8] if row[8] is not None else False
                    pendente = row[9] if row[9] is not None else False
                    obs = row[10] if row[10] is not None else ""

                    FichaDeAplicacao.objects.using("secondary").create(
                        data_criada=ficha_data_criada,
                        data_atualizado=ficha_data_atualizado,
                        area=area,
                        dados=dados,
                        data_aplicada=data_aplicada,
                        atividade_id=atividade_id,
                        estufa_id=estufa_id,
                        irrigador_id=irrigador_id,
                        ativo=ativo,
                        pendente=pendente,
                        obs=obs,
                    )
            for row in rows:
                id_default = row[0]
                data_atualizacao_default = row[11]

                cursor.execute(
                    "SELECT * FROM todos_fichadeaplicacao WHERE id = %s", [id_default]
                )
                row_secondary = cursor.fetchone()

                if row_secondary:
                    data_atualizacao_secondary = row_secondary[8]

                    data_atualizacao_default = data_atualizacao_default.astimezone(
                        pytz.timezone("Europe/London")
                    )
                    data_atualizacao_secondary = data_atualizacao_secondary.astimezone(
                        pytz.timezone("Europe/London")
                    )

                    if data_atualizacao_default > data_atualizacao_secondary:
                        dados_jsonb = json.dumps(row[3]) if row[3] is not None else None
                        dados_jsonb = json.loads(dados_jsonb)
                        cursor.execute(
                            "UPDATE todos_fichadeaplicacao SET "
                            "data_criada = %s, "
                            "data_atualizado = %s, "
                            "area = %s, "
                            "dados = %s, "
                            "data_aplicada = %s, "
                            "atividade_id = %s, "
                            "estufa_id = %s, "
                            "irrigador_id = %s, "
                            "ativo = %s, "
                            "pendente = %s, "
                            "obs = %s "
                            "WHERE id = %s",
                            [
                                row[1],
                                row[11],
                                row[2],
                                dados_jsonb,
                                datetime.combine(row[4], datetime.min.time()),
                                row[5],
                                row[6],
                                row[7],
                                row[8],
                                row[9],
                                row[10],
                                id_default,
                            ],
                        )

    #########################################################################################################

    @staticmethod
    def sync_db_produto():
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT * FROM todos_produtos ORDER BY id;")
            rows = cursor.fetchall()

        with connections["secondary"].cursor() as cursor:
            latest_date_in_database = Produtos.objects.using("secondary").aggregate(
                models.Max("data_criada")
            )["data_criada__max"]
            if latest_date_in_database:
                latest_date_in_database = latest_date_in_database.astimezone(
                    pytz.timezone("Europe/London")
                )
            for row in rows:
                ficha_data_criada_utc = row[6].replace(tzinfo=pytz.UTC)
                ficha_data_criada = ficha_data_criada_utc.astimezone(
                    timezone.get_default_timezone()
                ).replace(tzinfo=timezone.get_default_timezone())

                if (
                    not latest_date_in_database
                    or ficha_data_criada > latest_date_in_database
                ):
                    produto = row[4] if row[4] is not None else 0
                    codigo = row[1] if row[1] is not None else 0
                    descricao = row[2] if row[2] is not None else ""
                    ativo = row[3] if row[3] is not None else ""

                    Produtos.objects.using("default").create(
                        data_criada=ficha_data_criada,
                        data_atualizado=row[5],
                        produto=produto,
                        codigo=codigo,
                        descricao=descricao,
                        ativo=ativo,
                    )
            for row in rows:
                id_default = row[0]
                data_atualizacao_default = row[5]

                cursor.execute(
                    "SELECT * FROM todos_produtos WHERE id = %s", [id_default]
                )
                row_secondary = cursor.fetchone()

                if row_secondary:
                    data_atualizacao_secondary = row_secondary[5]

                    data_atualizacao_default = data_atualizacao_default.astimezone(
                        pytz.timezone("Europe/London")
                    )
                    data_atualizacao_secondary = data_atualizacao_secondary.astimezone(
                        pytz.timezone("Europe/London")
                    )

                    if data_atualizacao_default > data_atualizacao_secondary:
                        cursor.execute(
                            "UPDATE todos_produtos SET "
                            "data_criada = %s, "
                            "data_atualizado = %s, "
                            "codigo = %s, "
                            "descricao = %s, "
                            "ativo = %s, "
                            "produto = %s "
                            "WHERE id = %s",
                            [
                                row[6],
                                row[5],
                                row[1],
                                row[2],
                                row[3],
                                row[4],
                                id_default,
                            ],
                        )

    #########################################################################################################

    @staticmethod
    def sync_db_estufa():
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT * FROM todos_estufa ORDER BY id;")
            rows = cursor.fetchall()

        with connections["secondary"].cursor() as cursor:
            latest_date_in_database = Estufa.objects.using("secondary").aggregate(
                models.Max("data_criada")
            )["data_criada__max"]
            if latest_date_in_database:
                latest_date_in_database = latest_date_in_database.astimezone(
                    pytz.timezone("Europe/London")
                )
            for row in rows:
                ficha_data_criada_utc = row[6].replace(tzinfo=pytz.UTC)
                ficha_data_criada = ficha_data_criada_utc.astimezone(
                    timezone.get_default_timezone()
                ).replace(tzinfo=timezone.get_default_timezone())

                if (
                    not latest_date_in_database
                    or ficha_data_criada > latest_date_in_database
                ):
                    fazenda = row[4] if row[4] is not None else ""
                    nome_estufa = row[1] if row[1] is not None else ""
                    area = row[2] if row[2] is not None else 0.0
                    ativo = row[3] if row[3] is not None else True

                    Estufa.objects.using("secondary").create(
                        data_criada=ficha_data_criada,
                        data_atualizado=row[5],
                        fazenda=fazenda,
                        nome_estufa=nome_estufa,
                        area=area,
                        ativo=ativo,
                    )
            for row in rows:
                id_default = row[0]
                data_atualizacao_default = row[5]

                cursor.execute("SELECT * FROM todos_estufa WHERE id = %s", [id_default])
                row_secondary = cursor.fetchone()

                if row_secondary:
                    data_atualizacao_secondary = row_secondary[5]

                    data_atualizacao_default = data_atualizacao_default.astimezone(
                        pytz.timezone("Europe/London")
                    )
                    data_atualizacao_secondary = data_atualizacao_secondary.astimezone(
                        pytz.timezone("Europe/London")
                    )

                    if data_atualizacao_default > data_atualizacao_secondary:
                        cursor.execute(
                            "UPDATE todos_estufa SET "
                            "data_criada = %s, "
                            "data_atualizado = %s, "
                            "nome_estufa = %s, "
                            "area = %s, "
                            "ativo = %s, "
                            "fazenda = %s "
                            "WHERE id = %s",
                            [
                                row[6],
                                row[5],
                                row[1],
                                row[2],
                                row[3],
                                row[4],
                                id_default,
                            ],
                        )

    #########################################################################################################

    @staticmethod
    def sync_db_atividade():
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT * FROM todos_atividade ORDER BY id;")
            rows = cursor.fetchall()

        with connections["secondary"].cursor() as cursor:
            latest_date_in_database = Atividade.objects.using("secondary").aggregate(
                models.Max("data_criada")
            )["data_criada__max"]
            if latest_date_in_database:
                latest_date_in_database = latest_date_in_database.astimezone(
                    pytz.timezone("Europe/London")
                )
            for row in rows:
                ficha_data_criada_utc = row[3].replace(tzinfo=pytz.UTC)
                ficha_data_criada = ficha_data_criada_utc.astimezone(
                    timezone.get_default_timezone()
                ).replace(tzinfo=timezone.get_default_timezone())

                if (
                    not latest_date_in_database
                    or ficha_data_criada > latest_date_in_database
                ):
                    nome = row[1] if row[1] is not None else ""
                    ativo = row[2] if row[2] is not None else True

                    Atividade.objects.using("secondary").create(
                        data_criada=ficha_data_criada,
                        data_atualizado=row[4],
                        nome=nome,
                        ativo=ativo,
                    )
            for row in rows:
                id_default = row[0]
                data_atualizacao_default = row[3]

                cursor.execute(
                    "SELECT * FROM todos_atividade WHERE id = %s", [id_default]
                )
                row_secondary = cursor.fetchone()

                if row_secondary:
                    data_atualizacao_secondary = row_secondary[4]

                    data_atualizacao_default = data_atualizacao_default.astimezone(
                        pytz.timezone("Europe/London")
                    )
                    data_atualizacao_secondary = data_atualizacao_secondary.astimezone(
                        pytz.timezone("Europe/London")
                    )

                    if data_atualizacao_default > data_atualizacao_secondary:
                        cursor.execute(
                            "UPDATE todos_atividade SET "
                            "data_criada = %s, "
                            "data_atualizado = %s, "
                            "nome = %s, "
                            "ativo = %s "
                            "WHERE id = %s",
                            [
                                row[3],
                                row[4],
                                row[1],
                                row[2],
                                id_default,
                            ],
                        )


#########################################################################################################


class DatabaseDownloader:
    @staticmethod
    def sync_db():
        with connections["secondary"].cursor() as cursor:
            cursor.execute("SELECT * FROM todos_fichadeaplicacao ORDER BY id;")
            rows = cursor.fetchall()

        with connections["default"].cursor() as cursor:
            latest_date_in_database = FichaDeAplicacao.objects.using(
                "default"
            ).aggregate(models.Max("data_criada"))["data_criada__max"]

            latest_date_in_database = latest_date_in_database.astimezone(
                pytz.timezone("Europe/London")
            )
            print(latest_date_in_database)

            for row in rows:
                ficha_data_criada_utc = row[1].replace(tzinfo=pytz.UTC)
                ficha_data_criada = ficha_data_criada_utc.astimezone(
                    timezone.get_default_timezone()
                ).replace(tzinfo=timezone.get_default_timezone())

                if (
                    not latest_date_in_database
                    or ficha_data_criada > latest_date_in_database
                ):
                    area = row[5] if row[5] is not None else 0.0
                    dados = json.loads(row[6]) if row[6] is not None else {}
                    data_aplicada = datetime.combine(row[7], datetime.min.time())
                    atividade_id = row[2] if row[2] is not None else 0
                    estufa_id = row[3] if row[3] is not None else 0
                    irrigador_id = row[4] if row[4] is not None else 0
                    ativo = row[9] if row[9] is not None else False
                    pendente = row[10] if row[10] is not None else False
                    obs = row[11] if row[11] is not None else ""

                    FichaDeAplicacao.objects.using("default").create(
                        data_criada=ficha_data_criada,
                        data_atualizado=row[8],
                        area=area,
                        dados=dados,
                        data_aplicada=data_aplicada,
                        atividade_id=atividade_id,
                        estufa_id=estufa_id,
                        irrigador_id=irrigador_id,
                        ativo=ativo,
                        pendente=pendente,
                        obs=obs,
                    )

            for row in rows:
                id_secondary = row[0]
                data_atualizacao_secondary = row[8]

                cursor.execute(
                    "SELECT * FROM todos_fichadeaplicacao WHERE id = %s", [id_secondary]
                )
                row_default = cursor.fetchone()

                if row_default:
                    data_atualizacao_default = row_default[11]

                    data_atualizacao_secondary = data_atualizacao_secondary.astimezone(
                        pytz.timezone("Europe/London")
                    )
                    data_atualizacao_default = data_atualizacao_default.astimezone(
                        pytz.timezone("Europe/London")
                    )

                    if data_atualizacao_secondary > data_atualizacao_default:
                        dados_jsonb = json.dumps(row[6]) if row[6] is not None else None
                        dados_jsonb = json.loads(dados_jsonb)
                        cursor.execute(
                            "UPDATE todos_fichadeaplicacao SET "
                            "data_criada = %s, "
                            "data_atualizado = %s, "
                            "area = %s, "
                            "dados = %s, "
                            "data_aplicada = %s,"
                            "atividade_id = %s, "
                            "estufa_id = %s, "
                            "irrigador_id = %s, "
                            "ativo = %s, "
                            "pendente = %s, "
                            "obs = %s "
                            "WHERE id = %s",
                            [
                                row[1],
                                row[8],
                                row[5],
                                dados_jsonb,
                                row[7],
                                row[2],
                                row[3],
                                row[4],
                                row[9],
                                row[10],
                                row[11],
                                id_secondary,
                            ],
                        )

    #########################################################################################################

    def sync_db_produto():
        with connections["secondary"].cursor() as cursor:
            cursor.execute("SELECT * FROM todos_produtos ORDER BY id;")
            rows = cursor.fetchall()

        with connections["default"].cursor() as cursor:
            latest_date_in_database = Produtos.objects.using("default").aggregate(
                models.Max("data_criada")
            )["data_criada__max"]

            latest_date_in_database = latest_date_in_database.astimezone(
                pytz.timezone("Europe/London")
            )
            print(latest_date_in_database)

            for row in rows:
                ficha_data_criada_utc = row[6].replace(tzinfo=pytz.UTC)
                ficha_data_criada = ficha_data_criada_utc.astimezone(
                    timezone.get_default_timezone()
                ).replace(tzinfo=timezone.get_default_timezone())

                if (
                    not latest_date_in_database
                    or ficha_data_criada > latest_date_in_database
                ):
                    produto = row[1] if row[1] is not None else 0
                    codigo = row[2] if row[2] is not None else 0
                    descricao = row[3] if row[3] is not None else ""
                    ativo = row[4] if row[4] is not None else ""

                    Produtos.objects.using("default").create(
                        data_criada=ficha_data_criada,
                        data_atualizado=row[5],
                        produto=produto,
                        codigo=codigo,
                        descricao=descricao,
                        ativo=ativo,
                    )

            for row in rows:
                id_secondary = row[0]
                data_atualizacao_secondary = row[5]

                cursor.execute(
                    "SELECT * FROM todos_produtos WHERE id = %s", [id_secondary]
                )
                row_default = cursor.fetchone()

                if row_default:
                    data_atualizacao_default = row_default[5]

                    data_atualizacao_secondary = data_atualizacao_secondary.astimezone(
                        pytz.timezone("Europe/London")
                    )
                    data_atualizacao_default = data_atualizacao_default.astimezone(
                        pytz.timezone("Europe/London")
                    )

                    if data_atualizacao_secondary > data_atualizacao_default:
                        cursor.execute(
                            "UPDATE todos_produtos SET "
                            "data_criada = %s, "
                            "data_atualizado = %s, "
                            "produto = %s, "
                            "codigo = %s, "
                            "descricao = %s, "
                            "ativo = %s "
                            "WHERE id = %s",
                            [
                                row[6],
                                row[5],
                                row[1],
                                row[2],
                                row[3],
                                row[4],
                                id_secondary,
                            ],
                        )

    #########################################################################################################
    def sync_db_estufa():
        with connections["secondary"].cursor() as cursor:
            cursor.execute("SELECT * FROM todos_estufa ORDER BY id;")
            rows = cursor.fetchall()

        with connections["default"].cursor() as cursor:
            latest_date_in_database = Estufa.objects.using("default").aggregate(
                models.Max("data_criada")
            )["data_criada__max"]

            latest_date_in_database = latest_date_in_database.astimezone(
                pytz.timezone("Europe/London")
            )
            print(latest_date_in_database)

            for row in rows:
                ficha_data_criada_utc = row[6].replace(tzinfo=pytz.UTC)
                ficha_data_criada = ficha_data_criada_utc.astimezone(
                    timezone.get_default_timezone()
                ).replace(tzinfo=timezone.get_default_timezone())

                if (
                    not latest_date_in_database
                    or ficha_data_criada > latest_date_in_database
                ):
                    fazenda = row[3] if row[3] is not None else ""
                    nome_estufa = row[1] if row[1] is not None else ""
                    area = row[2] if row[2] is not None else 0.0
                    ativo = row[4] if row[4] is not None else True

                    Estufa.objects.using("default").create(
                        data_criada=ficha_data_criada,
                        data_atualizado=row[5],
                        fazenda=fazenda,
                        nome_estufa=nome_estufa,
                        area=area,
                        ativo=ativo,
                    )

            for row in rows:
                id_secondary = row[0]
                data_atualizacao_secondary = row[5]

                cursor.execute(
                    "SELECT * FROM todos_estufa WHERE id = %s", [id_secondary]
                )
                row_default = cursor.fetchone()

                if row_default:
                    data_atualizacao_default = row_default[5]

                    data_atualizacao_secondary = data_atualizacao_secondary.astimezone(
                        pytz.timezone("Europe/London")
                    )
                    data_atualizacao_default = data_atualizacao_default.astimezone(
                        pytz.timezone("Europe/London")
                    )

                    if data_atualizacao_secondary > data_atualizacao_default:
                        cursor.execute(
                            "UPDATE todos_estufa SET "
                            "data_criada = %s, "
                            "data_atualizado = %s, "
                            "nome_estufa = %s, "
                            "area = %s, "
                            "ativo = %s, "
                            "fazenda = %s "
                            "WHERE id = %s",
                            [
                                row[6],
                                row[5],
                                row[1],
                                row[2],
                                row[4],
                                row[3],
                                id_secondary,
                            ],
                        )

    #########################################################################################################
    def sync_db_atividade():
        with connections["secondary"].cursor() as cursor:
            cursor.execute("SELECT * FROM todos_atividade ORDER BY id;")
            rows = cursor.fetchall()

        with connections["default"].cursor() as cursor:
            latest_date_in_database = Estufa.objects.using("default").aggregate(
                models.Max("data_criada")
            )["data_criada__max"]

            latest_date_in_database = latest_date_in_database.astimezone(
                pytz.timezone("Europe/London")
            )
            print(latest_date_in_database)

            for row in rows:
                ficha_data_criada_utc = row[4].replace(tzinfo=pytz.UTC)
                ficha_data_criada = ficha_data_criada_utc.astimezone(
                    timezone.get_default_timezone()
                ).replace(tzinfo=timezone.get_default_timezone())

                if (
                    not latest_date_in_database
                    or ficha_data_criada > latest_date_in_database
                ):
                    nome = row[1] if row[1] is not None else ""
                    ativo = row[2] if row[2] is not None else True

                    Atividade.objects.using("secondary").create(
                        data_criada=ficha_data_criada,
                        data_atualizado=row[3],
                        nome=nome,
                        ativo=ativo,
                    )

            for row in rows:
                id_secondary = row[0]
                data_atualizacao_secondary = row[3]

                cursor.execute(
                    "SELECT * FROM todos_atividade WHERE id = %s", [id_secondary]
                )
                row_default = cursor.fetchone()

                if row_default:
                    data_atualizacao_default = row_default[3]

                    data_atualizacao_secondary = data_atualizacao_secondary.astimezone(
                        pytz.timezone("Europe/London")
                    )
                    data_atualizacao_default = data_atualizacao_default.astimezone(
                        pytz.timezone("Europe/London")
                    )

                    if data_atualizacao_secondary > data_atualizacao_default:
                        cursor.execute(
                            "UPDATE todos_atividade SET "
                            "data_criada = %s, "
                            "data_atualizado = %s, "
                            "nome = %s, "
                            "ativo = %s "
                            "WHERE id = %s",
                            [
                                row[4],
                                row[3],
                                row[1],
                                row[2],
                                id_secondary,
                            ],
                        )
