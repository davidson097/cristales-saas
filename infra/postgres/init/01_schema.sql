-- PostgreSQL Schema for Cristales SaaS
-- Generated from DBML model

-- Create enums
CREATE TYPE base_comision AS ENUM ('PRECIO_VENTA', 'UTILIDAD');
CREATE TYPE estado_alerta AS ENUM ('ABIERTA', 'VISTA', 'RESUELTA');
CREATE TYPE estado_comision AS ENUM ('PENDIENTE', 'LIQUIDADA', 'ANULADA');
CREATE TYPE estado_factura AS ENUM ('EMITIDA', 'ANULADA', 'PAGADA');
CREATE TYPE estado_liquidacion AS ENUM ('ABIERTA', 'CERRADA', 'PAGADA');
CREATE TYPE estado_orden AS ENUM ('PENDIENTE', 'EN_PROGRESO', 'COMPLETADA', 'CANCELADA');
CREATE TYPE estado_sesion AS ENUM ('ACTIVA', 'REVOCADA', 'EXPIRADA');
CREATE TYPE lado_cristal AS ENUM ('IZQ', 'DER', 'AMBOS');
CREATE TYPE metodo_pago AS ENUM ('EFECTIVO', 'TARJETA', 'TRANSFERENCIA', 'CHEQUE');
CREATE TYPE origen_orden AS ENUM ('PARTICULAR', 'TALLER', 'ASEGURADOR');
CREATE TYPE plan_saas AS ENUM ('BASIC', 'PROFESSIONAL', 'ENTERPRISE');
CREATE TYPE rol_comision AS ENUM ('VENDEDOR', 'INSTALADOR', 'GERENTE');
CREATE TYPE severidad_alerta AS ENUM ('WARNING', 'CRITICAL');
CREATE TYPE tipo_cliente AS ENUM ('PERSONA', 'EMPRESA');
CREATE TYPE tipo_comision AS ENUM ('PORCENTAJE', 'FIJO');
CREATE TYPE tipo_cristal AS ENUM ('STANDARD', 'TEMPLADO', 'BLINDADO');
CREATE TYPE tipo_documento AS ENUM ('FACTURA', 'NOTA_CREDITO', 'REMISION');
CREATE TYPE tipo_documento_id AS ENUM ('CEDULA', 'RNC', 'PASAPORTE');
CREATE TYPE tipo_empresa AS ENUM ('TALLER', 'DISTRIBUIDOR', 'FABRICANTE');
CREATE TYPE tipo_item_orden AS ENUM ('CRISTAL', 'TRAMO', 'SERVICIO', 'ACCESORIO');
CREATE TYPE tipo_mov_inv AS ENUM ('ENTRADA', 'SALIDA', 'AJUSTE', 'DEVOLUCION');
CREATE TYPE tipo_usuario_labor AS ENUM ('VENDEDOR', 'INSTALADOR', 'GERENTE', 'ADMINISTRATIVO');

-- Create tables
CREATE TABLE empresas (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  nombre TEXT NOT NULL,
  tipo tipo_empresa NOT NULL DEFAULT 'TALLER',
  telefono TEXT,
  email TEXT,
  activo BOOLEAN NOT NULL DEFAULT true,
  plan plan_saas NOT NULL DEFAULT 'BASIC',
  creado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_empresas_nombre ON empresas(nombre);

CREATE TABLE zonas (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  empresa_id UUID NOT NULL REFERENCES empresas(id),
  nombre TEXT NOT NULL,
  pais TEXT NOT NULL DEFAULT 'DO',
  provincia TEXT,
  municipio TEXT,
  sector TEXT,
  activo BOOLEAN NOT NULL DEFAULT true
);

CREATE UNIQUE INDEX uq_zona_empresa_nombre ON zonas(empresa_id, nombre);

CREATE TABLE usuarios (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  empresa_id UUID NOT NULL REFERENCES empresas(id),
  username TEXT NOT NULL,
  email TEXT,
  nombre TEXT NOT NULL,
  password_hash TEXT NOT NULL,
  activo BOOLEAN NOT NULL DEFAULT true,
  ultimo_login TIMESTAMPTZ,
  creado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX uq_usuario_empresa_username ON usuarios(empresa_id, username);
CREATE UNIQUE INDEX uq_usuario_empresa_email ON usuarios(empresa_id, email);

CREATE TABLE sesiones (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  empresa_id UUID NOT NULL REFERENCES empresas(id),
  usuario_id UUID NOT NULL REFERENCES usuarios(id),
  token_hash TEXT NOT NULL UNIQUE,
  estado estado_sesion NOT NULL DEFAULT 'ACTIVA',
  ip TEXT,
  user_agent TEXT,
  creado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
  expira_en TIMESTAMPTZ NOT NULL,
  revocado_en TIMESTAMPTZ
);

CREATE TABLE permisos (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  codigo TEXT NOT NULL UNIQUE,
  descripcion TEXT NOT NULL
);

CREATE TABLE roles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  empresa_id UUID NOT NULL REFERENCES empresas(id),
  nombre TEXT NOT NULL,
  descripcion TEXT,
  activo BOOLEAN NOT NULL DEFAULT true
);

CREATE UNIQUE INDEX uq_rol_empresa_nombre ON roles(empresa_id, nombre);

CREATE TABLE rol_permisos (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  empresa_id UUID NOT NULL REFERENCES empresas(id),
  rol_id UUID NOT NULL REFERENCES roles(id),
  permiso_id UUID NOT NULL REFERENCES permisos(id)
);

CREATE UNIQUE INDEX uq_rol_permiso_empresa ON rol_permisos(empresa_id, rol_id, permiso_id);

CREATE TABLE usuario_roles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  empresa_id UUID NOT NULL REFERENCES empresas(id),
  usuario_id UUID NOT NULL REFERENCES usuarios(id),
  rol_id UUID NOT NULL REFERENCES roles(id),
  activo BOOLEAN NOT NULL DEFAULT true
);

CREATE UNIQUE INDEX uq_usuario_rol_empresa ON usuario_roles(empresa_id, usuario_id, rol_id);

CREATE TABLE usuario_perfil_laboral (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  empresa_id UUID NOT NULL REFERENCES empresas(id),
  usuario_id UUID NOT NULL REFERENCES usuarios(id),
  tipo tipo_usuario_labor NOT NULL,
  activo BOOLEAN NOT NULL DEFAULT true,
  telefono TEXT,
  nota TEXT,
  creado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX uq_perfil_laboral_usuario_tipo ON usuario_perfil_laboral(empresa_id, usuario_id, tipo);

CREATE TABLE clientes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  empresa_id UUID NOT NULL REFERENCES empresas(id),
  tipo tipo_cliente NOT NULL,
  nombre_comercial TEXT NOT NULL,
  documento_tipo tipo_documento_id,
  documento_numero TEXT,
  telefono_principal TEXT,
  email_principal TEXT,
  zona_id UUID REFERENCES zonas(id),
  direccion TEXT,
  activo BOOLEAN NOT NULL DEFAULT true,
  creado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_clientes_nombre ON clientes(empresa_id, nombre_comercial);
CREATE INDEX idx_clientes_doc ON clientes(empresa_id, documento_numero);
CREATE INDEX idx_clientes_tel ON clientes(empresa_id, telefono_principal);

CREATE TABLE vehiculos (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  empresa_id UUID NOT NULL REFERENCES empresas(id),
  cliente_id UUID NOT NULL REFERENCES clientes(id),
  placa TEXT,
  vin TEXT,
  marca TEXT NOT NULL,
  modelo TEXT NOT NULL,
  anio INT,
  color TEXT,
  zona_id UUID REFERENCES zonas(id),
  creado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX uq_vehiculo_empresa_placa ON vehiculos(empresa_id, placa);
CREATE UNIQUE INDEX uq_vehiculo_empresa_vin ON vehiculos(empresa_id, vin);

CREATE TABLE cristales (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  empresa_id UUID NOT NULL REFERENCES empresas(id),
  sku TEXT NOT NULL,
  descripcion TEXT NOT NULL,
  tipo tipo_cristal NOT NULL,
  lado lado_cristal,
  marca_cristal TEXT,
  costo NUMERIC(12, 2) NOT NULL DEFAULT 0,
  precio_base NUMERIC(12, 2) NOT NULL DEFAULT 0,
  activo BOOLEAN NOT NULL DEFAULT true,
  creado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX uq_cristal_empresa_sku ON cristales(empresa_id, sku);
CREATE INDEX idx_cristal_tipo ON cristales(empresa_id, tipo);

CREATE TABLE compatibilidad (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  empresa_id UUID NOT NULL REFERENCES empresas(id),
  cristal_id UUID NOT NULL REFERENCES cristales(id),
  marca TEXT NOT NULL,
  modelo TEXT NOT NULL,
  anio_desde INT,
  anio_hasta INT
);

CREATE INDEX idx_compat_marca_modelo ON compatibilidad(empresa_id, marca, modelo);

CREATE TABLE almacenes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  empresa_id UUID NOT NULL REFERENCES empresas(id),
  nombre TEXT NOT NULL,
  zona_id UUID REFERENCES zonas(id),
  activo BOOLEAN NOT NULL DEFAULT true
);

CREATE UNIQUE INDEX uq_almacen_empresa_nombre ON almacenes(empresa_id, nombre);

CREATE TABLE stock_config (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  empresa_id UUID NOT NULL REFERENCES empresas(id),
  almacen_id UUID NOT NULL REFERENCES almacenes(id),
  cristal_id UUID NOT NULL REFERENCES cristales(id),
  stock_min INT NOT NULL DEFAULT 0
);

CREATE UNIQUE INDEX uq_stock_cfg_empresa ON stock_config(empresa_id, almacen_id, cristal_id);

CREATE TABLE tramos (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  empresa_id UUID NOT NULL REFERENCES empresas(id),
  almacen_id UUID NOT NULL REFERENCES almacenes(id),
  nombre TEXT NOT NULL,
  referencia TEXT NOT NULL,
  descripcion TEXT,
  fecha_compra DATE,
  estado TEXT NOT NULL DEFAULT 'ABIERTO',
  activo BOOLEAN NOT NULL DEFAULT true,
  creado_por UUID REFERENCES usuarios(id),
  creado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
  actualizado_en TIMESTAMPTZ
);

CREATE INDEX idx_tramo_ref ON tramos(empresa_id, referencia);

CREATE TABLE tramo_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  empresa_id UUID NOT NULL REFERENCES empresas(id),
  tramo_id UUID NOT NULL REFERENCES tramos(id),
  cristal_id UUID NOT NULL REFERENCES cristales(id),
  cantidad_inicial INT NOT NULL DEFAULT 0,
  cantidad_actual INT NOT NULL DEFAULT 0
);

CREATE UNIQUE INDEX uq_tramo_item ON tramo_items(empresa_id, tramo_id, cristal_id);

CREATE TABLE movimientos_inventario (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  empresa_id UUID NOT NULL REFERENCES empresas(id),
  almacen_id UUID NOT NULL REFERENCES almacenes(id),
  cristal_id UUID NOT NULL REFERENCES cristales(id),
  tramo_id UUID REFERENCES tramos(id),
  tipo tipo_mov_inv NOT NULL,
  cantidad INT NOT NULL,
  costo_unit NUMERIC(12, 2),
  ref_tipo TEXT,
  ref_id UUID,
  nota TEXT,
  creado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
  creado_por UUID REFERENCES usuarios(id)
);

CREATE TABLE roturas_cristales (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  empresa_id UUID NOT NULL REFERENCES empresas(id),
  movimiento_id UUID NOT NULL REFERENCES movimientos_inventario(id),
  cristal_id UUID NOT NULL REFERENCES cristales(id),
  almacen_id UUID NOT NULL REFERENCES almacenes(id),
  tramo_id UUID REFERENCES tramos(id),
  cantidad INT NOT NULL,
  motivo TEXT NOT NULL,
  costo_perdida NUMERIC(12, 2),
  responsable_id UUID REFERENCES usuarios(id),
  evidencias_url TEXT,
  creado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE ordenes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  empresa_id UUID NOT NULL REFERENCES empresas(id),
  numero BIGINT NOT NULL,
  cliente_id UUID NOT NULL REFERENCES clientes(id),
  vehiculo_id UUID REFERENCES vehiculos(id),
  origen origen_orden NOT NULL DEFAULT 'PARTICULAR',
  taller_id UUID REFERENCES clientes(id),
  aseguradora_id UUID REFERENCES clientes(id),
  estado estado_orden NOT NULL,
  fecha TIMESTAMPTZ NOT NULL DEFAULT now(),
  instalador_id UUID REFERENCES usuario_perfil_laboral(id),
  vendedor_id UUID REFERENCES usuario_perfil_laboral(id),
  almacen_salida_id UUID REFERENCES almacenes(id),
  zona_id UUID REFERENCES zonas(id),
  observacion TEXT,
  creado_por UUID REFERENCES usuarios(id),
  creado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX uq_orden_empresa_num ON ordenes(empresa_id, numero);

CREATE TABLE orden_detalle (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  empresa_id UUID NOT NULL REFERENCES empresas(id),
  orden_id UUID NOT NULL REFERENCES ordenes(id),
  tipo_item tipo_item_orden NOT NULL,
  cristal_id UUID REFERENCES cristales(id),
  tramo_id UUID REFERENCES tramos(id),
  descripcion TEXT NOT NULL,
  cantidad INT NOT NULL DEFAULT 1,
  precio_unit NUMERIC(12, 2) NOT NULL DEFAULT 0,
  descuento NUMERIC(12, 2) NOT NULL DEFAULT 0
);

CREATE TABLE secuencias_documentos (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  empresa_id UUID NOT NULL REFERENCES empresas(id),
  tipo tipo_documento NOT NULL,
  serie TEXT NOT NULL DEFAULT 'A',
  proximo_num BIGINT NOT NULL DEFAULT 1
);

CREATE UNIQUE INDEX uq_seq_empresa_tipo_serie ON secuencias_documentos(empresa_id, tipo, serie);

CREATE TABLE facturas (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  empresa_id UUID NOT NULL REFERENCES empresas(id),
  tipo tipo_documento NOT NULL,
  serie TEXT NOT NULL DEFAULT 'A',
  numero BIGINT NOT NULL,
  cliente_id UUID NOT NULL REFERENCES clientes(id),
  orden_id UUID REFERENCES ordenes(id),
  instalador_id UUID REFERENCES usuario_perfil_laboral(id),
  vendedor_id UUID REFERENCES usuario_perfil_laboral(id),
  fecha TIMESTAMPTZ NOT NULL DEFAULT now(),
  moneda TEXT NOT NULL DEFAULT 'DOP',
  subtotal NUMERIC(12, 2) NOT NULL DEFAULT 0,
  descuento NUMERIC(12, 2) NOT NULL DEFAULT 0,
  impuesto NUMERIC(12, 2) NOT NULL DEFAULT 0,
  total NUMERIC(12, 2) NOT NULL DEFAULT 0,
  estado estado_factura NOT NULL DEFAULT 'EMITIDA',
  zona_id UUID REFERENCES zonas(id),
  creado_por UUID REFERENCES usuarios(id),
  creado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX uq_fact_empresa_tipo_serie_num ON facturas(empresa_id, tipo, serie, numero);

CREATE TABLE factura_detalle (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  empresa_id UUID NOT NULL REFERENCES empresas(id),
  factura_id UUID NOT NULL REFERENCES facturas(id),
  cristal_id UUID REFERENCES cristales(id),
  tramo_id UUID REFERENCES tramos(id),
  descripcion TEXT NOT NULL,
  cantidad INT NOT NULL DEFAULT 1,
  precio_unit NUMERIC(12, 2) NOT NULL DEFAULT 0,
  descuento NUMERIC(12, 2) NOT NULL DEFAULT 0
);

CREATE TABLE pagos (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  empresa_id UUID NOT NULL REFERENCES empresas(id),
  factura_id UUID NOT NULL REFERENCES facturas(id),
  fecha TIMESTAMPTZ NOT NULL DEFAULT now(),
  metodo metodo_pago NOT NULL,
  monto NUMERIC(12, 2) NOT NULL,
  referencia TEXT,
  recibido_por UUID REFERENCES usuarios(id),
  creado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE reglas_comision (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  empresa_id UUID NOT NULL REFERENCES empresas(id),
  rol rol_comision NOT NULL,
  perfil_laboral_id UUID REFERENCES usuario_perfil_laboral(id),
  cristal_id UUID REFERENCES cristales(id),
  tipo_cristal tipo_cristal,
  tipo tipo_comision NOT NULL DEFAULT 'PORCENTAJE',
  base base_comision NOT NULL DEFAULT 'PRECIO_VENTA',
  valor NUMERIC(8, 4) NOT NULL,
  activo BOOLEAN NOT NULL DEFAULT true,
  creado_por UUID REFERENCES usuarios(id),
  creado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE comisiones (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  empresa_id UUID NOT NULL REFERENCES empresas(id),
  rol rol_comision NOT NULL,
  perfil_laboral_id UUID NOT NULL REFERENCES usuario_perfil_laboral(id),
  factura_id UUID NOT NULL REFERENCES facturas(id),
  factura_detalle_id UUID REFERENCES factura_detalle(id),
  regla_id UUID REFERENCES reglas_comision(id),
  tipo tipo_comision NOT NULL,
  base base_comision NOT NULL,
  cantidad INT NOT NULL DEFAULT 1,
  monto_base NUMERIC(12, 2) NOT NULL,
  valor_aplicado NUMERIC(8, 4) NOT NULL,
  monto_comision NUMERIC(12, 2) NOT NULL,
  estado estado_comision NOT NULL DEFAULT 'PENDIENTE',
  creado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
  creado_por UUID REFERENCES usuarios(id)
);

CREATE TABLE liquidaciones (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  empresa_id UUID NOT NULL REFERENCES empresas(id),
  rol rol_comision NOT NULL,
  perfil_laboral_id UUID NOT NULL REFERENCES usuario_perfil_laboral(id),
  periodo_desde DATE NOT NULL,
  periodo_hasta DATE NOT NULL,
  total_comision NUMERIC(12, 2) NOT NULL DEFAULT 0,
  estado estado_liquidacion NOT NULL DEFAULT 'ABIERTA',
  creado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
  creado_por UUID REFERENCES usuarios(id),
  cerrado_en TIMESTAMPTZ,
  pagado_en TIMESTAMPTZ,
  nota TEXT
);

CREATE TABLE liquidacion_detalle (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  empresa_id UUID NOT NULL REFERENCES empresas(id),
  liquidacion_id UUID NOT NULL REFERENCES liquidaciones(id),
  comision_id UUID NOT NULL REFERENCES comisiones(id)
);

CREATE TABLE alertas_stock (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  empresa_id UUID NOT NULL REFERENCES empresas(id),
  almacen_id UUID NOT NULL REFERENCES almacenes(id),
  cristal_id UUID NOT NULL REFERENCES cristales(id),
  stock_min INT NOT NULL DEFAULT 0,
  stock_actual INT NOT NULL DEFAULT 0,
  severidad severidad_alerta NOT NULL DEFAULT 'WARNING',
  estado estado_alerta NOT NULL DEFAULT 'ABIERTA',
  ultima_detec TIMESTAMPTZ NOT NULL DEFAULT now(),
  resuelta_en TIMESTAMPTZ,
  resuelta_por UUID REFERENCES usuarios(id),
  nota TEXT
);

CREATE TABLE auditoria_eventos (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  empresa_id UUID NOT NULL REFERENCES empresas(id),
  actor_id UUID REFERENCES usuarios(id),
  entidad TEXT NOT NULL,
  entidad_id UUID,
  accion TEXT NOT NULL,
  detalle JSON,
  ip TEXT,
  creado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);
