import streamlit as st
from datetime import date
import tempfile
import re
import sqlite3
from streamlit_mic_recorder import mic_recorder
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from src.transcriber import transcrever_audio
from src.clinical_ai import analisar_consulta
from src.image_analysis import analisar_imagem
from src.lesion_detection import detectar_lesao
from src.pathology_interpreter import interpretar_laudo
from src.melanoma_abcd import analisar_abcd
from src.biopsy_request import gerar_pedido_biopsia
from src.patient_report import gerar_laudo_paciente


# ----------------------------
# BANCO
# ----------------------------

def conectar_db():
    return sqlite3.connect("derm_ai.db", check_same_thread=False)

def criar_tabelas():

    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS consultas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        data_consulta TEXT,
        transcricao TEXT,
        analise TEXT
    )
    """)

    conn.commit()
    conn.close()

criar_tabelas()


# ----------------------------
# SALVAR CONSULTA
# ----------------------------

def salvar_consulta(nome, transcricao, analise):

    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO consultas (patient_name, data_consulta, transcricao, analise)
    VALUES (?, ?, ?, ?)
    """, (
        nome,
        date.today().strftime("%Y-%m-%d"),
        transcricao,
        analise
    ))

    conn.commit()
    conn.close()


# ----------------------------
# APP
# ----------------------------

st.set_page_config(page_title="Derm AI Copilot", layout="wide")

st.title("Derm AI Copilot")
st.write("Assistente dermatológico com IA")


# ----------------------------
# SESSION STATE
# ----------------------------

if "patient_started" not in st.session_state:
    st.session_state.patient_started = False

if "patient_name" not in st.session_state:
    st.session_state.patient_name = ""

if "patient_sex" not in st.session_state:
    st.session_state.patient_sex = ""

if "patient_age" not in st.session_state:
    st.session_state.patient_age = ""

if "transcricao_total" not in st.session_state:
    st.session_state.transcricao_total = ""

if "analise_total" not in st.session_state:
    st.session_state.analise_total = ""

if "camera_ativa" not in st.session_state:
    st.session_state.camera_ativa = False


# ----------------------------
# CALCULAR IDADE
# ----------------------------

def calcular_idade(data_nascimento):

    hoje = date.today()

    idade = hoje.year - data_nascimento.year - (
        (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day)
    )

    return idade


# ----------------------------
# PDF
# ----------------------------

def gerar_pdf():

    arquivo = "consulta_medica.pdf"

    c = canvas.Canvas(arquivo, pagesize=A4)

    largura, altura = A4
    y = altura - 50

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, "RELATÓRIO MÉDICO")

    y -= 40
    c.setFont("Helvetica", 12)

    c.drawString(50, y, f"Paciente: {st.session_state.patient_name}")
    y -= 20

    c.drawString(50, y, f"Sexo: {st.session_state.patient_sex}")
    y -= 20

    c.drawString(50, y, f"Idade: {st.session_state.patient_age}")
    y -= 20

    for linha in st.session_state.analise_total.split("\n"):

        c.drawString(50, y, linha[:95])
        y -= 15

        if y < 120:
            c.showPage()
            y = altura - 50

    c.save()

    return arquivo


# ----------------------------
# NOVO PACIENTE
# ----------------------------

if not st.session_state.patient_started:

    st.header("Novo paciente")

    nome = st.text_input("Paciente")

    sexo = st.selectbox(
        "Sexo",
        ["Masculino", "Feminino", "Outro"]
    )

    if "patient_dob" not in st.session_state:
        st.session_state.patient_dob = None

    dob = st.date_input(
        "Data de nascimento",
        value=st.session_state.patient_dob,
        min_value=date(1900,1,1),
        max_value=date.today()
    )

    st.session_state.patient_dob = dob

    idade = None

    if dob:
        idade = calcular_idade(dob)
        st.write(f"Idade: {idade} anos")

    if st.button("Iniciar consulta"):

        st.session_state.patient_name = nome
        st.session_state.patient_sex = sexo
        st.session_state.patient_age = idade
        st.session_state.patient_started = True

        st.rerun()

    st.stop()


# ----------------------------
# SIDEBAR
# ----------------------------

st.sidebar.header("Paciente")

st.sidebar.write(f"Paciente: {st.session_state.patient_name}")
st.sidebar.write(f"Sexo: {st.session_state.patient_sex}")
st.sidebar.write(f"Idade: {st.session_state.patient_age}")

if st.sidebar.button("Novo paciente"):

    st.session_state.patient_started = False
    st.session_state.transcricao_total = ""
    st.session_state.analise_total = ""

    st.rerun()


# ----------------------------
# CONSULTA
# ----------------------------

st.header("Consulta")

audio = mic_recorder(
    start_prompt="🎙️ Gravar consulta",
    stop_prompt="⏹️ Parar gravação",
    just_once=True
)

if audio:

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:

        temp_audio.write(audio["bytes"])
        audio_path = temp_audio.name

    texto = transcrever_audio(audio_path)

    st.session_state.transcricao_total += "\n\n" + texto

    texto_completo = st.session_state.transcricao_total

    analise = analisar_consulta(texto_completo)

    # remove asteriscos gerados pela IA
    analise = analise.replace("*", "")

    st.session_state.analise_total = analise

    salvar_consulta(
        st.session_state.patient_name,
        st.session_state.transcricao_total,
        st.session_state.analise_total
    )


# ----------------------------
# PRONTUÁRIO
# ----------------------------

if st.session_state.analise_total:

    st.subheader("Prontuário médico")

    st.markdown(st.session_state.analise_total)

    st.code(st.session_state.analise_total)


# ----------------------------
# HISTÓRICO
# ----------------------------

st.divider()
st.header("Histórico de consultas")

conn = conectar_db()
cursor = conn.cursor()

cursor.execute("""
SELECT patient_name, data_consulta
FROM consultas
ORDER BY id DESC
LIMIT 20
""")

consultas = cursor.fetchall()

for c in consultas:
    st.write(f"{c[0]} - {c[1]}")
# ----------------------------
# SOLICITAR BIÓPSIA
# ----------------------------

if st.session_state.transcricao_total:

    if st.checkbox("Solicitar biópsia"):

        pedido = gerar_pedido_biopsia(st.session_state.transcricao_total)

        st.subheader("Pedido anatomopatológico")

        st.write(pedido)


# ----------------------------
# GERAR LAUDO PARA PACIENTE
# ----------------------------

if st.session_state.transcricao_total:

    if st.checkbox("Gerar laudo para paciente"):

        laudo = gerar_laudo_paciente(
            st.session_state.transcricao_total,
            st.session_state.analise_total
        )

        st.subheader("Laudo médico para paciente")

        st.write(laudo)

        st.code(laudo)


# ----------------------------
# INTERPRETAR LAUDO
# ----------------------------

st.divider()

st.header("Interpretar anatomopatológico")

laudo = st.text_area("Cole o laudo anatomopatológico")

if laudo:

    if st.button("Interpretar laudo"):

        interpretacao = interpretar_laudo(laudo)

        st.write(interpretacao)


# ----------------------------
# IMAGEM DERMATOLÓGICA
# ----------------------------

st.divider()

st.header("Imagem dermatológica")

imagem = st.file_uploader(
    "Upload da imagem",
    type=["jpg", "jpeg", "png"]
)

if st.button("Usar câmera"):

    st.session_state.camera_ativa = True

if st.session_state.camera_ativa:

    imagem_camera = st.camera_input("Fotografar lesão")

    if imagem_camera:

        imagem = imagem_camera

if imagem:

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_img:

        temp_img.write(imagem.read())

        img_path = temp_img.name

    resultado = analisar_imagem(img_path)

    st.subheader("Análise da imagem")

    st.write(resultado)

    img_detect, _ = detectar_lesao(img_path)

    st.image(img_detect)

    if st.checkbox("Screening melanoma ABCD"):

        abcd = analisar_abcd(img_path)

        st.write("Score ABCD:", abcd["score"])