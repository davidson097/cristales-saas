# Import all models to ensure relationships are resolved
from .modules.empresas.models import Empresa
from .modules.inventario.models import Almacen, StockConfig, MovimientoInventario, AlertaStock
from .modules.catalogo.models import CatalogItem
from .modules.usuarios.models import Usuario
from .modules.clientes.models import Cliente
from .modules.vehiculos.models import Vehiculo
from .modules.zonas.models import Zona
from .modules.ordenes.models import Orden
from .modules.facturacion.models import Factura
from .modules.pagos.models import Pago
from .modules.perfiles.models import Perfil
from .rbac.models import Role