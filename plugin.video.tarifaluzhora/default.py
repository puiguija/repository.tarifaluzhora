import xbmcplugin, xbmcgui, sys, os
from resources.lib.scraper import fetch_prices
from resources.lib.graficos import generar_grafico_linea, generar_grafico_barras
import datetime

# Get the plugin url in plugin:// notation.
HANDLE = int(sys.argv[1])
# Get a plugin handle as an integer number.
BASE_URL = sys.argv[0]

ADDON_PATH = xbmc.translatePath("special://home/addons/plugin.video.tarifaluzhora/")
MEDIA_PATH = os.path.join(ADDON_PATH, "resources", "media")
os.makedirs(MEDIA_PATH, exist_ok=True)

grafico_linea_path = os.path.join(MEDIA_PATH, "grafico_linea.png")
grafico_barras_path = os.path.join(MEDIA_PATH, "grafico_barras.png")

data = fetch_prices()
if not data:
    xbmcgui.Dialog().notification("Error", "No se pudieron obtener datos")
    xbmcplugin.endOfDirectory(HANDLE); sys.exit()

current = data["current"]
_min = data["min"]
_max = data["max"]
msg = (f"Actual  {current['value']:.2f} €/MWh\n"
       f"Mínimo  { _min['value']:.2f} €/MWh a las { _min['datetime'][11:16]}\n"
       f"Máximo  {_max['value']:.2f} €/MWh a las {_max['datetime'][11:16]}")
xbmcgui.Dialog().ok("Tarifa Luz Hora", msg)

generar_grafico_linea(data["values"], grafico_linea_path)
generar_grafico_barras(data["values"], grafico_barras_path)

img1 = xbmcgui.ListItem("📈 Gráfico Evolutivo")
img1.setArt({"thumb": grafico_linea_path})
xbmcplugin.addDirectoryItem(HANDLE, BASE_URL, img1, False)

img2 = xbmcgui.ListItem("📊 Gráfico por Tramos")
img2.setArt({"thumb": grafico_barras_path})
xbmcplugin.addDirectoryItem(HANDLE, BASE_URL, img2, False)

for v in data["values"]:
    hora = v["datetime"][11:16]
    precio = v["value"]
    li = xbmcgui.ListItem(label=f"{hora} – {precio:.2f} €/MWh")
    xbmcplugin.addDirectoryItem(HANDLE, BASE_URL, li, False)

xbmcplugin.endOfDirectory(HANDLE)
