import pandas as pd
import plotly.express as px
import os

class DataService:
    """Centraliza la carga y limpieza de datos."""
    def get_sales_data(self):
        nombre_archivo = "data.csv"
        
        # Si el archivo existe, lo lee. Si no, crea datos de prueba.
        if os.path.exists(nombre_archivo):
            return pd.read_csv(nombre_archivo)
        else:
            print(f"⚠️ Archivo {nombre_archivo} no encontrado. Usando datos de prueba.")
            datos_prueba = {
                "Producto": ["Rosas", "Tulipanes", "Girasoles", "Lirios"],
                "Ventas": [150, 200, 120, 180]
            }
            return pd.DataFrame(datos_prueba)

class ChartFactory:
    """Genera visualizaciones con un estilo uniforme."""
    @staticmethod
    def build_bar_chart(df, x, y):
        # px.bar ahora funcionará porque ya lo importamos arriba
        fig = px.bar(df, x=x, y=y, 
                     title="Reporte de Ventas",
                     template="plotly_dark")
        
        fig.update_traces(marker_color='#007bff') # Color azul profesional
        fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
        return fig

class UIFormatter:
    """Utilidades para el formato de la interfaz."""
    @staticmethod
    def money_format(value):
        # Formatea números como moneda: 1000 -> $1,000.00 USD
        return f"${value:,.2f} USD"

# --- BLOQUE DE EJECUCIÓN (Para probar que todo funciona) ---
if __name__ == "__main__":
    # 1. Instanciar el servicio y obtener datos
    servicio = DataService()
    df = servicio.get_sales_data()
    
    # 2. Crear el gráfico usando la fábrica
    grafico = ChartFactory.build_bar_chart(df, x="Producto", y="Ventas")
    
    # 3. Mostrar el resultado (Se abrirá en tu navegador)
    print("✅ Generando visualización...")
    grafico.show()
    
    # 4. Ejemplo del formateador
    ejemplo_precio = UIFormatter.money_format(2500.50)
    print(f"✅ Ejemplo de formato: {ejemplo_precio}")