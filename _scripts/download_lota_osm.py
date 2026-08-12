import urllib.request
import json
import os

overpass_url = "https://overpass-api.de/api/interpreter"
overpass_query = """
[out:json][timeout:25];
(
  // Chiflón del Diablo
  way["name"~"Chiflón del Diablo",i];
  relation["name"~"Chiflón del Diablo",i];
  node["name"~"Chiflón del Diablo",i];
  
  // Parque de Lota / Isidora Cousiño
  way["name"~"Parque",i]["name"~"Lota|Isidora",i];
  relation["name"~"Parque",i]["name"~"Lota|Isidora",i];
  
  // Pabellón 83
  way["name"~"Pabellón 83",i];
  node["name"~"Pabellón 83",i];
);
out body;
>;
out skel qt;
"""

print("Consultando Overpass API para Lota...")
try:
    req = urllib.request.Request(
        overpass_url, 
        data=overpass_query.encode('utf-8'),
        headers={'User-Agent': 'LotaIndomito/1.0'}
    )
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
        
    os.makedirs('public/data', exist_ok=True)
    out_path = 'public/data/lota_pois_osm.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Datos OSM de Lota guardados exitosamente en: {out_path} ({len(data.get('elements', []))} elementos)")

except Exception as e:
    print(f"❌ Error al consultar Overpass API: {e}")
