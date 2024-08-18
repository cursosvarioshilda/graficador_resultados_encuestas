import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from io import BytesIO
from datetime import datetime
import matplotlib.backends.backend_pdf

def main():
    st.title("Graficador de Resultados de Encuestas")

    # Añadir logotipo al inicio
    st.image(r"C:\Users\Hilda Londoño\Desktop\logo.png", width=150)

    # Sección de instrucciones
    st.markdown("""
    ### Instrucciones:
     Este es un generador de gráficos  automáticos, el cual te genera un informe en PDF
     para que puedas  analizar y tomar decisiones de tu negocio de una forma fácil y sencilla.
    1. Carga tu archivo CSV de encuestas.
    2. Selecciona todas las columnas que deseas analizar.
    3. Si escoges columnas de texto NO sacar estadisticas. Hacer la consulta por separado para generar los númericos 
    4. Genera gráficos y estadísticas con los botones correspondientes y descargar a PDF.
    """)

    # Subir archivo CSV
    uploaded_file = st.file_uploader("Elige un archivo CSV", type="csv")
    
    if uploaded_file:
        # Leer el archivo CSV en un DataFrame
        data = pd.read_csv(uploaded_file)

        # Mostrar las columnas disponibles
        st.write("Columnas disponibles:")
        st.write(data.columns)

        # Seleccionar columnas para graficar
        selected_columns = st.multiselect("Selecciona las columnas para graficar", data.columns)

        # Botón para generar gráficos
        if st.button("Generar Gráficos"):
            if selected_columns:
                # Crear archivo PDF para gráficos
                pdf_graphs_buffer = BytesIO()
                pdf_graphs = matplotlib.backends.backend_pdf.PdfPages(pdf_graphs_buffer)

                # Crear gráficos para las columnas seleccionadas
                for i, column in enumerate(selected_columns):
                    fig, ax = plt.subplots(figsize=(14, 10))  # Crear una nueva figura y ejes

                    # Contar los valores y ordenarlos por serie
                    counts = data[column].value_counts()
                    ordered_index = sorted(counts.index, key=lambda x: str(x))
                    counts = counts.reindex(ordered_index)

                    # Graficar los conteos
                    counts.plot(kind='bar', ax=ax, color='skyblue', edgecolor='black')
                    
                    # Ajustar los títulos y etiquetas
                    ax.set_xlabel(column, fontsize=16)
                    ax.set_ylabel('Cantidad de Encuestados', fontsize=16)  # Título del eje Y
                    ax.set_title(f"Distribución de {column}", fontsize=18, fontweight='bold')
                    ax.tick_params(axis='both', labelsize=16)  # Tamaño de los valores de los ejes
                    
                    # Guardar la figura en el PDF
                    pdf_graphs.savefig(fig)
                    plt.close(fig)

                # Cerrar el archivo PDF de gráficos
                pdf_graphs.close()
                pdf_graphs_buffer.seek(0)
                
                # Opción para descargar el archivo PDF
                st.download_button(
                    label="Descargar gráficos en PDF",
                    data=pdf_graphs_buffer,
                    file_name="graphs.pdf",
                    mime="application/pdf"
                )
            else:
                st.warning("Por favor, selecciona al menos una columna para graficar.")

        # Botón para generar estadísticas
        if st.button("Generar Estadísticas"):
            if selected_columns:
                # Crear un resumen estadístico
                stats_summary = pd.DataFrame()
                stats_summary['Columna'] = selected_columns
                stats_summary['Máximo'] = [f"{data[col].max():.2f}" for col in selected_columns]
                stats_summary['Mínimo'] = [f"{data[col].min():.2f}" for col in selected_columns]
                stats_summary['Promedio'] = [f"{data[col].mean():.2f}" for col in selected_columns]
                stats_summary['Desviación Estándar'] = [f"{data[col].std():.2f}" for col in selected_columns]

                # Crear archivo PDF para estadísticas
                pdf_stats_buffer = BytesIO()
                pdf_stats = matplotlib.backends.backend_pdf.PdfPages(pdf_stats_buffer)
                
                fig, ax = plt.subplots(figsize=(14, 10))  # Crear una nueva figura y ejes
                
                # Agregar título general con fecha
                today_date = datetime.now().strftime('%d/%m/%Y')
                plt.suptitle(f'Resumen Estadístico {today_date}', fontsize=24, ha='center', fontweight='bold')
                
                # Crear una tabla con resumen estadístico
                table = plt.table(cellText=stats_summary.values,
                                  colLabels=stats_summary.columns,
                                  cellLoc='center',
                                  loc='center',
                                  bbox=[0.1, 0.2, 0.8, 0.7],  # Ajusta este valor según sea necesario
                                  colColours=['#689A67']*len(stats_summary.columns),
                                  cellColours=[['#ffffff']*len(stats_summary.columns)]*len(stats_summary),
                                  colWidths=[0.2]*len(stats_summary.columns))

                # Ajustar el tamaño de la fuente en la tabla
                table.auto_set_font_size(False)
                table.set_fontsize(16)  # Ajusta este valor según sea necesario
                
                # Ajustar el tamaño de las celdas para que el texto no se desborde
                table.auto_set_column_width([0, 1, 2, 3, 4])  # Ajusta los índices de las columnas según sea necesario
                table.scale(1.2, 1.2)  # Escala el tamaño de la tabla (ajusta según sea necesario)
                
                plt.title('Resumen Estadístico', fontsize=30, fontweight='bold')
                plt.axis('off')
                
                # Ajustar el diseño para que se vea bien
                plt.tight_layout(rect=[0, 0, 1, 0.9])
                
                # Guardar la figura en el PDF
                pdf_stats.savefig(fig)
                plt.close(fig)

                # Cerrar el archivo PDF de estadísticas
                pdf_stats.close()
                pdf_stats_buffer.seek(0)
                
                # Opción para descargar el archivo PDF
                st.download_button(
                    label="Descargar resumen estadístico en PDF",
                    data=pdf_stats_buffer,
                    file_name="stats_summary.pdf",
                    mime="application/pdf"
                )
            else:
                st.warning("Por favor, selecciona al menos una columna para generar estadísticas.")

    # Pie de página al final
    st.markdown("© 2024 Hilda Londoño, La Ceja- Antioquia . Todos los derechos reservados.")

if __name__ == "__main__":
    main()
