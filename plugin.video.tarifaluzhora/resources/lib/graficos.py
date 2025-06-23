import matplotlib.pyplot as plt
from datetime import datetime
import os

def generar_grafico_linea(data, path):
    horas = [datetime.fromisoformat(d["datetime"][:-6]).strftime("%H:%M") for d in data]
    precios = [d["value"] for d in data]
    plt.figure(figsize=(10, 4))
    plt.plot(horas, precios, marker='o')
    plt.title("Evolución del precio de la luz (€/MWh)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

def generar_grafico_barras(data, path):
    horas = [datetime.fromisoformat(d["datetime"][:-6]).strftime("%H:%M") for d in data]
    precios = [d["value"] for d in data]
    colores = []
    for precio in precios:
        if precio < 60:
            colores.append("green")
        elif precio < 100:
            colores.append("orange")
        else:
            colores.append("red")
    plt.figure(figsize=(10, 4))
    plt.bar(horas, precios, color=colores)
    plt.title("Precio de la luz por hora")
    plt.xticks(rotation=45)
    plt.grid(True, axis="y")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
