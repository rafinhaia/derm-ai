from src.melanoma_abcd import analisar_abcd
import streamlit as st
from streamlit_mic_recorder import mic_recorder
from src.transcriber import transcrever_audio
from src.clinical_ai import analisar_consulta
from src.image_analysis import analisar_imagem
from src.lesion_detection import detectar_lesao
from src.biopsy_request import gerar_pedido_biopsia
from src.pathology_interpreter import interpretar_laudo
from src.patient_report import gerar_laudo_paciente
import tempfile

st.title("Derm AI Copilot")
st.write("Assistente dermatológico com IA")

# -----------------------------
# SESSION STATE
# -----------------------------

if "texto" not in st.session_state:
    st.session_state.texto = None

if "analise" not in st.session_state:
    st.session_state.analise = None


# -----------------------------
# GRAVAÇÃO DE CONSULTA
# -----------------------------

st.header("Consulta")

audio = mic_recorder(
    start_prompt="🎙️ Gravar consulta",
    stop_prompt="⏹️ Parar gravação",
    just_once=True
)

if audio:

    st.success("Áudio gravado")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio["bytes"])
        audio_path = temp_audio.name

    st.write("Transcrevendo consulta...")

    texto = transcrever_audio(audio_path)

    st.session_state.texto = texto

    st.subheader("Transcrição")
    st.write(texto)

    st.write("Gerando análise clínica...")

    analise = analisar_consulta(texto)

    st.session_state.analise = analise


# -----------------------------
# MOSTRAR PRONTUÁRIO
# -----------------------------

if st.session_state.analise:

    st.subheader("Prontuário médico")
    st.write(st.session_state.analise)

    st.subheader("Prontuário para copiar")
    st.code(st.session_state.analise)


# -----------------------------
# GERAR PEDIDO DE BIÓPSIA
# -----------------------------

if st.session_state.texto:

    if st.checkbox("Solicitar biópsia"):

        pedido = gerar_pedido_biopsia(st.session_state.texto)

        st.subheader("Pedido anatomopatológico")

        st.write(pedido)


# -----------------------------
# GERAR LAUDO PARA PACIENTE
# -----------------------------

if st.session_state.texto:

    if st.checkbox("Gerar laudo para o paciente"):

        laudo_paciente = gerar_laudo_paciente(
            st.session_state.texto,
            st.session_state.analise
        )

        st.subheader("Laudo médico para o paciente")

        st.write(laudo_paciente)

        st.code(laudo_paciente)


# -----------------------------
# INTERPRETAÇÃO DE LAUDO
# -----------------------------

st.header("Interpretar anatomopatológico")

laudo = st.text_area("Cole o laudo anatomopatológico")

if laudo and st.button("Interpretar laudo"):

    interpretacao = interpretar_laudo(laudo)

    st.subheader("Interpretação clínica")

    st.write(interpretacao)


# -----------------------------
# ANÁLISE DE IMAGEM
# -----------------------------

st.divider()

st.header("Imagem dermatológica")

modo_imagem = st.radio(
    "Como deseja enviar a imagem?",
    ["Usar câmera do celular", "Upload da galeria"]
)

if modo_imagem == "Usar câmera do celular":

    image_file = st.camera_input("Tirar foto da lesão")

else:

    image_file = st.file_uploader(
        "Upload da imagem da lesão",
        type=["jpg", "jpeg", "png"]
    )

if image_file is not None:

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_img:
        temp_img.write(image_file.read())
        img_path = temp_img.name

    st.write("Analisando imagem...")

    resultado_img = analisar_imagem(img_path)

    st.subheader("Análise da imagem pela IA")

    st.write(resultado_img)

    img_detect, _ = detectar_lesao(img_path)

    st.subheader("Detecção da lesão")

    st.image(img_detect)

    if st.checkbox("🔬 Fazer screening para melanoma (ABCD)"):

        abcd = analisar_abcd(img_path)

        if abcd:

            st.subheader("Screening ABCD")

            assimetria = "alta" if abcd["assimetria"] > 50 else "moderada" if abcd["assimetria"] > 20 else "baixa"

            borda = "muito irregular" if abcd["irregularidade_borda"] > 0.5 else "moderada" if abcd["irregularidade_borda"] > 0.2 else "regular"

            cor = "policromia significativa" if abcd["variacao_cor"] > 40 else "variação moderada" if abcd["variacao_cor"] > 20 else "cor homogênea"

            st.write("Assimetria:", assimetria)

            st.write("Bordas:", borda)

            st.write("Cores:", cor)

            st.write("Score ABCD:", abcd["score"])

            if abcd["risco"] == "alto":

                st.error("⚠ Risco elevado de melanoma — considerar biópsia excisional")

            elif abcd["risco"] == "moderado":

                st.warning("Risco moderado — avaliar dermatoscopia ou biópsia")

            else:

                st.success("Risco baixo")