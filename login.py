import streamlit as st

# estado de login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 🔒 LOGIN
if not st.session_state.logged_in:

    st.title("Derm AI Copilot")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if senha == "654321":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Senha incorreta")

    st.stop()  # 🔴 impede execução do app antes do login

# ✅ APP PRINCIPAL (SEM BUG DE IMPORT)
with open("main_app.py", "r", encoding="utf-8") as f:
    code = f.read()
    exec(code, globals())