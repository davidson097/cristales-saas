from __future__ import annotations

import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# Add backend to sys.path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Cargar .env (repo root o backend/.env)
try:
    from dotenv import load_dotenv

    here = os.path.dirname(__file__)  # backend/alembic
    candidates = [
        os.path.join(here, "..", "..", ".env"),   # repo/.env
        os.path.join(here, "..", ".env"),         # backend/.env
    ]
    for p in candidates:
        p = os.path.abspath(p)
        if os.path.exists(p):
            load_dotenv(p)
            break
except Exception:
    # Si no está python-dotenv, no rompas alembic; solo usará alembic.ini
    pass

config = context.config

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# =========================
# IMPORTA TU BASE AQUÍ
# =========================
# Ajusta UNA de estas rutas según tu proyecto.
# Si falla, cambia la primera y deja el resto igual.
try:
    from app.db.base import Base  # <- opción típica
except Exception as e:
    print(f"Error importing Base: {e}")
    try:
        from app.database import Base  # <- opción alternativa
    except Exception as e2:
        print(f"Error importing Base alt: {e2}")
        # Último recurso: si tu Base vive en otro lado, ponlo aquí
        # from app.algo import Base
        Base = None

if Base is None:
    raise RuntimeError(
        "No se pudo importar Base. Ajusta el import en alembic/env.py para apuntar "
        "al archivo donde defines tu SQLAlchemy Base."
    )

target_metadata = Base.metadata

# (Opcional pero MUY útil) Asegura que los modelos se importen
# para que se registren en Base.metadata y autogenerate detecte tablas.
# Ajusta el import según tu estructura real.
try:
    # Import all models from modules
    from app.modules.catalogo import models
    from app.modules.clientes import models
    from app.modules.comisiones import models
    from app.modules.empresas import models
    from app.modules.facturacion import models
    from app.modules.inventario import models
    from app.modules.ordenes import models
    from app.modules.pagos import models
    from app.modules.perfiles import models
    from app.modules.usuarios import models
    from app.modules.vehiculos import models
    from app.modules.zonas import models
    from app.rbac import models
except Exception as e:
    print(f"Error importing models: {e}")
    pass

# Usa DATABASE_URL si existe, si no usa sqlalchemy.url del alembic.ini
db_url = os.getenv("DATABASE_URL")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}) or {},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

