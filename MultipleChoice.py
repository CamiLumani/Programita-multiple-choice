import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter, A4, landscape, legal
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from Descarga import download_button
import os
import zipfile
import tempfile


st.title("Programita generador de exámenes")

st.header("Configuración", divider="grey")
st.markdown("**1. Importe el archivo con las preguntas.**")
url= "https://docs.google.com/spreadsheets/d/1GzFHVbIUVdZkhVweOMmi2QNw2KsYxiac/edit?usp=sharing&ouid=105103885863993836751&rtpof=true&sd=true"
st.markdown(":warning: ***Importante:*** El mismo debe ser en formato excel, con las preguntas en la primer columna (A) y las respuestas en las columnas sucesivas (B,C,D,etc). Aquí un ejemplo: [link](%s)"  % url)

ArchivoPreguntas = st.file_uploader("Preguntas:", type=["xlsx"], accept_multiple_files=False)

st.markdown("**2. Ingrese la cantidad de preguntas por examen:**")
PreguntasPorExamen = st.number_input('Preguntas:', min_value=1, max_value=1000, value=None)

st.markdown("**3.  Ingrese la cantidad de exámenes a imprimir:**")
Examenes = st.number_input('Examenes:', min_value=1, max_value=1000, value=None)

st.markdown("**4. Ingrese un encabezado para los archivos:**")
Encabezado= st.text_input("Encabezado")


st.header("Configuración del archivo de salida", divider="grey")
st.markdown("**5. Seleccione el tamaño de la hoja:**")
OpcionesPagina = {"Carta": letter, "A4": A4, "Oficio": legal, "A4 - Horizontal": landscape(A4)}
TamañoPagina = st.selectbox("Tamaño de la hoja:", list(OpcionesPagina.keys()))

st.markdown("**6. Ingrese el tamaño de la fuente del título:**")
TamañoTitulo = st.number_input('Tamaño del título:', min_value=8, max_value=100, value=15)

st.markdown("**7. Ingrese el tamaño de la fuente de las preguntas y respuestas:**")
TamañoPreguntas = st.number_input('Tamaño de la fuente de preguntas y respuestas:', min_value=8, max_value=100, value=10)

st.header("Generar los exámenes", divider="grey")
def generararchivo(df, CantPreguntas, num_examen,titulo):
    pregunta_column = df.columns[0]
    Random = df.sample(CantPreguntas)
    Elementos = []
    numpregunta = 1
    
    _, temp_file_path = tempfile.mkstemp(suffix='.pdf')

    doc = SimpleDocTemplate(temp_file_path,pagesize=OpcionesPagina[TamañoPagina])

    
    estilo_encabezado = ParagraphStyle(name='Encabezado', fontSize=TamañoTitulo,leading=TamañoTitulo+1)
    estilo_texto = ParagraphStyle(name='Texto', fontSize=TamañoPreguntas, leading=TamañoPreguntas+1)
    
    Elementos.append(Paragraph(f"<strong>{titulo}</strong> ", estilo_encabezado))
    
    Elementos.append(Spacer(1, TamañoTitulo))
    
    for index, row in Random.iterrows():
        Pregunta = row[pregunta_column]
        respuestas = row.iloc[1:]
        respuestas_aleatorias = respuestas.dropna().sample(frac=1) 
        
        Formato_Pregunta = f"<strong>{numpregunta}.{Pregunta}</strong><br/>"
        Formato_Respuesta = []
        for i, rta in enumerate(respuestas_aleatorias):
            if pd.notna(rta):
                Formato_Respuesta.append(f"{chr(97 + i)}. {rta}")

        Elementos.append(Paragraph(Formato_Pregunta, estilo_texto))
        for rta in Formato_Respuesta:
            Elementos.append(Paragraph(rta, estilo_texto))

        Elementos.append(Spacer(1, 6))
        numpregunta += 1

    Nombre_archivo = f"Examen_{num_examen}.pdf"
    doc = SimpleDocTemplate(Nombre_archivo,pagesize=OpcionesPagina[TamañoPagina])
    doc.build(Elementos)
    return Nombre_archivo

def zip_files(files):
    with zipfile.ZipFile("Examenes.zip","w") as zipf:
        for file in files:
            zipf.write(file)

if st.button('Generar archivos'):
    if ArchivoPreguntas is not None:
        exam_files = []
        df = pd.read_excel(ArchivoPreguntas)
        for i in range(Examenes):
            exam_files.append(generararchivo(df, PreguntasPorExamen, i+1,Encabezado))
        zip_files(exam_files)
        st.markdown("Descargue los exámenes:")
        download_button_str = download_button(open("Examenes.zip", "rb").read(), "Examenes.zip", "Descargar todos los exámenes")
        st.markdown(download_button_str, unsafe_allow_html=True)
    else:
        st.warning("Por favor, suba un archivo de preguntas antes de generar los exámenes.")
        
    st.markdown("**Suerte con las correcciones** :balloon:	:clinking_glasses: ")
    
    st.markdown("*- Sugerencias de mejora: camilumani@gmail.com -*")





