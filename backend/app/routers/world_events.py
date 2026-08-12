from datetime import datetime, timezone
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix='/api/world-events', tags=['world-events'])

EVENTOS = [
    {
        'id': 'fiestas_patrias_2026',
        'nombre': 'Fiestas Patrias',
        'descripcion': 'Celebración nacional. Recorre Lota, completa las misiones patrias y canjea tu insignia.',
        'fecha_inicio': '2026-09-18',
        'fecha_fin': '2026-09-19',
        'npc_exclusiva': {
            'nombre': 'Doña Carmen',
            'rol': 'Empanadera de Lota',
            'historia': 'Doña Carmen horneaba empanadas en el barrio desde 1962. Cada Fiestas Patrias, sale a ofrecer sus recetas a los caminantes.',
            'zona_nombre': 'Parque Isidora Cousiño',
            'zona_id': 89121388,
            'ruta_fija': [
                {'lat': -37.0885, 'lon': -73.1585},
                {'lat': -37.0890, 'lon': -73.1578},
                {'lat': -37.0895, 'lon': -73.1582},
                {'lat': -37.0890, 'lon': -73.1585},
            ],
        },
        'misiones': [
            {
                'id': 'mision_empanadas',
                'nombre': 'El Sabor del Carbón',
                'descripcion': 'Encuentra a Doña Carmen en el Parque, clasifica sus empanadas y recibe el cupón patrio.',
                'pasos': 3,
                'recompensa_minerales': {'cobre': 100, 'oro': 10},
                'recompensa_insignia': 'catador_patrio',
                'recompensa_cupon': {
                    'id': 'cupon_fiestas_patrias_2026',
                    'nombre': '15% off en Panadería El Minero',
                    'comercio': 'Panadería El Minero',
                    'comercio_id': 'panaderia_el_minero',
                    'descuento': '15%',
                    'validez_dias': 30,
                },
            },
        ],
        'insignias': [
            {
                'id': 'catador_patrio',
                'nombre': 'Catador Patrio',
                'descripcion': 'Completaste las misiones de Fiestas Patrias 2026.',
                'imagen': '🏆',
                'caduca': False,
            },
        ],
        'tematica': 'fiestas_patrias',
        'colores': {'primario': '#E63946', 'secundario': '#FFD166', 'fondo': '#FDF0D5'},
        'activo': True,
    },
    {
        'id': 'san_juan_2026',
        'nombre': 'San Juan',
        'descripcion': 'La noche más larga. El Ciego enciende fogatas en el Chiflón.',
        'fecha_inicio': '2026-06-24',
        'fecha_fin': '2026-06-24',
        'npc_exclusiva': {
            'nombre': 'El Ciego de la Mina',
            'rol': 'Vigía de San Juan',
            'historia': 'Cada 24 de junio, el Ciego enciende las fogatas en el Chiflón para guiar a los mineros a casa.',
            'zona_nombre': 'Chiflón del Diablo',
            'zona_id': 480338029,
            'ruta_fija': [
                {'lat': -37.0705, 'lon': -73.1345},
                {'lat': -37.0710, 'lon': -73.1338},
                {'lat': -37.0705, 'lon': -73.1335},
            ],
        },
        'misiones': [
            {
                'id': 'mision_fogatas',
                'nombre': 'Fogatas del Ciego',
                'descripcion': 'Encuentra al Ciego en el Chiflón y enciende la fogata.',
                'pasos': 2,
                'recompensa_minerales': {'cobre': 80, 'oro': 5},
                'recompensa_insignia': 'viguia_san_juan',
                'recompensa_cupon': None,
            },
        ],
        'insignias': [
            {
                'id': 'viguia_san_juan',
                'nombre': 'Vigía de San Juan',
                'descripcion': 'Encendiste la fogata en San Juan 2026.',
                'imagen': '🔥',
                'caduca': False,
            },
        ],
        'tematica': 'san_juan',
        'colores': {'primario': '#FF9F1C', 'secundario': '#2EC4B6', 'fondo': '#1A1A2E'},
        'activo': True,
    },
]


class Insignia(BaseModel):
    id: str
    nombre: str
    descripcion: str
    imagen: str
    caduca: bool


class Cupon(BaseModel):
    id: str
    nombre: str
    comercio: str
    comercio_id: str
    descuento: str
    validez_dias: int


class Mission(BaseModel):
    id: str
    nombre: str
    descripcion: str
    pasos: int
    recompensa_minerales: dict
    recompensa_insignia: str
    recompensa_cupon: Cupon | None


class NpcExclusiva(BaseModel):
    nombre: str
    rol: str
    historia: str
    zona_nombre: str
    zona_id: int
    ruta_fija: list[dict]


class WorldEvent(BaseModel):
    id: str
    nombre: str
    descripcion: str
    fecha_inicio: str
    fecha_fin: str
    npc_exclusiva: NpcExclusiva
    misiones: list[Mission]
    insignias: list[Insignia]
    tematica: str
    colores: dict
    activo: bool


@router.get('', response_model=list[WorldEvent])
async def listar_eventos() -> list[WorldEvent]:
    return [WorldEvent(**e) for e in EVENTOS]


@router.get('/activos', response_model=list[WorldEvent])
async def eventos_activos() -> list[WorldEvent]:
    hoy = datetime.now(timezone.utc).date().isoformat()
    return [
        WorldEvent(**e) for e in EVENTOS
        if e['activo'] and e['fecha_inicio'] <= hoy <= e['fecha_fin']
    ]


@router.get('/proximos', response_model=list[WorldEvent])
async def eventos_proximos() -> list[WorldEvent]:
    hoy = datetime.now(timezone.utc).date().isoformat()
    return [
        WorldEvent(**e) for e in EVENTOS
        if e['activo'] and e['fecha_inicio'] > hoy
    ]


@router.get('/{event_id}', response_model=WorldEvent)
async def obtener_evento(event_id: str) -> WorldEvent:
    for e in EVENTOS:
        if e['id'] == event_id:
            return WorldEvent(**e)
    from fastapi import HTTPException, status
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Evento no encontrado')


@router.get('/{event_id}/npc/posicion')
async def npc_posicion(event_id: str, tick: int = 0) -> dict:
    for e in EVENTOS:
        if e['id'] == event_id:
            ruta = e['npc_exclusiva']['ruta_fija']
            idx = tick % len(ruta)
            return {
                'event_id': event_id,
                'npc': e['npc_exclusiva']['nombre'],
                'tick': tick,
                'posicion_idx': idx,
                'lat': ruta[idx]['lat'],
                'lon': ruta[idx]['lon'],
            }
    from fastapi import HTTPException, status
    raise HTTPException(status_code=404, detail='Evento no encontrado')
