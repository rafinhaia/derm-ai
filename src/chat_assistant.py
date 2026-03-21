import streamlit as st
from src.clinical_ai import analisar_consulta


def render_chat():

    st.divider()
    st.header("Assistente clínico (IA)")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    pergunta = st.text_input("Pergunte sobre o caso atual")

    if st.button("Enviar pergunta"):

        if not st.session_state.transcricao_total:
            st.warning("Nenhuma consulta ainda.")
            return

        contexto = st.session_state.transcricao_total

        prompt = f"""
Você é um dermatologista especialista atuando como CONSULTOR CLÍNICO.

IMPORTANTE:
- NÃO repita o prontuário
- NÃO reescreva o caso
- NÃO liste tudo novamente

Responda APENAS a pergunta do médico de forma direta e prática.

CASO CLÍNICO:
{contexto}

PERGUNTA:
{pergunta}

Responda em no máximo 5 linhas, de forma objetiva e prática.
"""

        resposta = analisar_consulta(prompt)

        st.session_state.chat_history.append(("Você", pergunta))
        st.session_state.chat_history.append(("IA", resposta))

    for autor, msg in st.session_state.chat_history:
        st.write(f"**{autor}:** {msg}")