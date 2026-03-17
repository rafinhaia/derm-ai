import streamlit as st
from datetime import date
import tempfile
from streamlit_mic_recorder import mic_recorder
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from src.transcriber import transcrever_audio
from src.clinical_ai import analisar_consulta
from src.image_analysis import analisar_imagem
from src.lesion_detection import detectar_lesao
from src.pathology_interpreter import interpretar_laudo
from src.melanoma_abcd import analisar_abcd


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

if "patient_dob" not in st.session_state:
    st.session_state.patient_dob = None

if "patient_age" not in st.session_state:
    st.session_state.patient_age = ""

if "transcricao_total" not in st.session_state:
    st.session_state.transcricao_total = ""

if "analise_total" not in st.session_state:
    st.session_state.analise_total = ""

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
# GERAR PDF PROFISSIONAL
# ----------------------------

def gerar_pdf():

    arquivo = "consulta_medica.pdf"

    c = canvas.Canvas(arquivo, pagesize=A4)

    largura, altura = A4

    y = altura - 50

    # CABEÇALHO
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

    c.drawString(50, y, f"Data da consulta: {date.today().strftime('%d/%m/%Y')}")

    y -= 40

    # HISTÓRIA CLÍNICA
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "História clínica")

    y -= 25

    c.setFont("Helvetica", 11)

    for linha in st.session_state.transcricao_total.split("\n"):

        c.drawString(50, y, linha[:95])

        y -= 15

        if y < 120:
            c.showPage()
            y = altura - 50

    y -= 20

    # PRONTUÁRIO
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Prontuário médico")

    y -= 25

    c.setFont("Helvetica", 11)

    for linha in st.session_state.analise_total.split("\n"):

        c.drawString(50, y, linha[:95])

        y -= 15

        if y < 120:
            c.showPage()
            y = altura - 50

    # ASSINATURA
    y -= 40

    c.line(50, y, 300, y)

    y -= 15

    c.setFont("Helvetica", 10)
    c.drawString(50, y, "Assinatura do médico")

    c.save()

    return arquivo

# ----------------------------
# FORMULÁRIO PACIENTE
# ----------------------------

if not st.session_state.patient_started:

    st.header("Novo paciente")

    nome = st.text_input("Paciente")

    sexo = st.selectbox(
        "Sexo",
        ["Masculino", "Feminino", "Outro"]
    )

    dob = st.date_input(
        "Data de nascimento",
        min_value=date(1900, 1, 1),
        max_value=date.today()
    )

    idade = None

    if dob:

        idade = calcular_idade(dob)

        st.write(f"Idade: {idade} anos")

    if st.button("Iniciar consulta"):

        st.session_state.patient_name = nome
        st.session_state.patient_sex = sexo
        st.session_state.patient_dob = dob
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
# CONSULTA POR ÁUDIO
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

    st.write("Transcrevendo...")

    texto = transcrever_audio(audio_path)

    st.session_state.transcricao_total += "\n\n" + texto

    st.subheader("Nova transcrição")

    st.write(texto)

    st.subheader("Histórico da consulta")

    st.write(st.session_state.transcricao_total)

    st.write("Gerando prontuário...")

    analise = analisar_consulta(st.session_state.transcricao_total)

    st.session_state.analise_total = analise

# ----------------------------
# PRONTUÁRIO
# ----------------------------

if st.session_state.analise_total:

    st.subheader("Prontuário médico")

    st.write(st.session_state.analise_total)

    st.code(st.session_state.analise_total)

# ----------------------------
# FINALIZAR CONSULTA
# ----------------------------

st.divider()

st.header("Finalizar consulta")

if st.button("Gerar PDF médico"):

    pdf = gerar_pdf()

    with open(pdf, "rb") as file:

        st.download_button(
            label="Baixar PDF",
            data=file,
            file_name="consulta_medica.pdf",
            mime="application/pdf"
        )

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
# ANÁLISE DE IMAGEM
# ----------------------------

st.divider()

st.header("Imagem dermatológica")

modo = st.radio(
    "Enviar imagem",
    ["Câmera", "Upload"]
)

if modo == "Câmera":

    imagem = st.camera_input("Fotografar lesão")

else:

    imagem = st.file_uploader(
        "Upload da imagem",
        type=["jpg", "jpeg", "png"]
    )

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