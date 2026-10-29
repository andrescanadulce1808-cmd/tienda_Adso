from fastapi import APIRouter
from app.database import conectar

router = APIRouter(prefix='/reportes', tags=['Reportes'])

@router.get('/ventas-por-cliente')
def ventas_por_cliente():
    # Solo lectura: no modifica ningún registro. Los pedidos cancelados no cuentan como venta.
    with conectar() as db:
        with db.cursor() as cur:
            cur.execute('''SELECT c.id, c.nombre,
                                  COUNT(p.id) AS num_pedidos,
                                  COALESCE(SUM(p.total), 0) AS total_vendido
                           FROM clientes c
                           LEFT JOIN pedidos p ON p.cliente_id = c.id AND p.estado <> 'cancelado'
                           GROUP BY c.id, c.nombre
                           ORDER BY total_vendido DESC, c.id''')
            return cur.fetchall()