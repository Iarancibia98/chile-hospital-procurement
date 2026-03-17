import requests

TICKET = "F8537A18-6766-4DEF-9E59-426B4FEE2844"
FECHA  = "16032026"

PALABRAS_CLAVE = [
    "hospital", "salud", "médico", "medico",
    "farmac", "clínica", "clinica", "insumo",
    "quirúrgico", "quirurgico", "sanitario",
    "servicio de salud"
]
PALABRAS_EXCLUIR = [
    "tabiquería",
    "construcción",
    "infraestructura",
    "pintura",
    "aseo",
    "limpieza",
    "vigilancia",
    "seguridad",
    "alimentación",
    "cocina",
]


def es_licitacion_hospitalaria(nombre):
    nombre = nombre.lower()
    tiene_clave   = any(p in nombre for p in PALABRAS_CLAVE)
    esta_excluida = any(p in nombre for p in PALABRAS_EXCLUIR)
    return tiene_clave and not esta_excluida


url = f"https://api.mercadopublico.cl/servicios/v1/Publico/Licitaciones.json?fecha={FECHA}&ticket={TICKET}"

response = requests.get(url)
data = response.json()

total   = data["Cantidad"]
listado = data["Listado"]

hospitalarias = [l for l in listado if es_licitacion_hospitalaria(l["Nombre"])]

print(f"Total licitaciones del día  : {total}")
print(f"Sin filtro de exclusión     : 222")
print(f"Con filtro de exclusión     : {len(hospitalarias)}")
print(f"Porcentaje                  : {len(hospitalarias)/total*100:.1f}%")
print(f"\nEjemplos encontrados:")
for l in hospitalarias[:8]:
    print(f"  - {l['Nombre'][:80]}")