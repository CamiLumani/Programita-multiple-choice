import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
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

st.header("Generar los archivos", divider="grey")
def generararchivo(df, CantPreguntas, num_examen,titulo):
    Random = df.sample(CantPreguntas)
    Elementos = []
    numpregunta = 1
    
    _, temp_file_path = tempfile.mkstemp(suffix='.pdf')

    doc = SimpleDocTemplate(temp_file_path, pagesize=letter)

    
    estilo_encabezado = ParagraphStyle(name='Encabezado', fontSize=20)
    
    Elementos.append(Paragraph(f"<strong>{titulo}</strong> ", estilo_encabezado))
    
    Elementos.append(Spacer(1, 12))
    Elementos.append(Spacer(1, 12))

    for index, row in Random.iterrows():
        Pregunta = row['Pregunta']
        respuestas = row.iloc[1:]

        Formato_Pregunta = f"<strong>{numpregunta}.{Pregunta}</strong><br/>"
        Formato_Respuesta = []
        for i, rta in enumerate(respuestas):
            if pd.notna(rta):
                Formato_Respuesta.append(f"{chr(97 + i)}. {rta}")

        Elementos.append(Paragraph(Formato_Pregunta, getSampleStyleSheet()["BodyText"]))
        for rta in Formato_Respuesta:
            Elementos.append(Paragraph(rta, getSampleStyleSheet()["BodyText"]))

        Elementos.append(Spacer(1, 12))
        numpregunta += 1

    Nombre_archivo = f"Examen_{num_examen}.pdf"
    doc = SimpleDocTemplate(Nombre_archivo, pagesize=letter)
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


