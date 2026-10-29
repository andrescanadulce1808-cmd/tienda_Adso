from fastapi import APIRouter, HTTPException
from pymysql.err import IntegrityError
from app.database import conectar
from app.schemas import ClienteCrear, ClienteRespuesta

router = APIRouter(prefix='/clientes', tags=['Clientes'])

@router.get('', response_model=list[ClienteRespuesta])
def listar():
    with conectar() as db:
        with db.cursor() as cur:
            cur.execute('SELECT * FROM clientes ORDER BY id')
            return cur.fetchall()

@router.get('/{cliente_id}', response_model=ClienteRespuesta)
def obtener(cliente_id: int):
    with conectar() as db:
        with db.cursor() as cur:
            cur.execute('SELECT * FROM clientes WHERE id=%s', (cliente_id,))
            cliente = cur.fetchone()
    if cliente is None:
        raise HTTPException(404, 'Cliente no encontrado')
    return cliente

@router.post('', response_model=ClienteRespuesta, status_code=201)
def crear(datos: ClienteCrear):
    try:
        with conectar() as db:
            with db.cursor() as cur:
                cur.execute('INSERT INTO clientes (nombre,correo) VALUES (%s,%s)', (datos.nombre, str(datos.correo)))
                nuevo_id = cur.lastrowid
                cur.execute('SELECT * FROM clientes WHERE id=%s', (nuevo_id,))
                return cur.fetchone()
    except IntegrityError as exc:
        raise HTTPException(409, 'Correo ya registrado') from exc

# ---- Reto C: actualizar y eliminar ----
@router.put('/{cliente_id}', response_model=ClienteRespuesta)
def actualizar(cliente_id: int, datos: ClienteCrear):
    try:
        with conectar() as db:
            with db.cursor() as cur:
                cur.execute('UPDATE clientes SET nombre=%s, correo=%s WHERE id=%s',
                            (datos.nombre, str(datos.correo), cliente_id))
                if cur.rowcount == 0:
                    raise HTTPException(404, 'Cliente no encontrado')
                cur.execute('SELECT * FROM clientes WHERE id=%s', (cliente_id,))
                return cur.fetchone()
    except IntegrityError as exc:
        raise HTTPException(409, 'Correo ya registrado por otro cliente') from exc

@router.delete('/{cliente_id}', status_code=204)
def eliminar(cliente_id: int):
    try:
        with conectar() as db:
            with db.cursor() as cur:
                cur.execute('SELECT id FROM clientes WHERE id=%s', (cliente_id,))
                if cur.fetchone() is None:
                    raise HTTPException(404, 'Cliente no encontrado')
                cur.execute('SELECT COUNT(*) AS total FROM pedidos WHERE cliente_id=%s', (cliente_id,))
                if cur.fetchone()['total'] > 0:
                    raise HTTPException(409, 'No se puede eliminar: el cliente tiene pedidos')
                cur.execute('DELETE FROM clientes WHERE id=%s', (cliente_id,))
    except IntegrityError as exc:
        # Red de seguridad: la llave foránea también lo impide.
        raise HTTPException(409, 'No se puede eliminar: el cliente tiene pedidos') from exc

# ---- Reto A: pedidos de un cliente (JOIN, orden por fecha) ----
@router.get('/{cliente_id}/pedidos')
def pedidos_del_cliente(cliente_id: int):
    with conectar() as db:
        with db.cursor() as cur:
            cur.execute('SELECT id FROM clientes WHERE id=%s', (cliente_id,))
            if cur.fetchone() is None:
                raise HTTPException(404, 'Cliente no encontrado')
            cur.execute('''SELECT p.id, p.fecha, p.estado, p.total, c.nombre AS cliente
                           FROM pedidos p JOIN clientes c ON c.id=p.cliente_id
                           WHERE c.id=%s ORDER BY p.fecha DESC, p.id DESC''', (cliente_id,))
            return cur.fetchall()