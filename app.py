import streamlit as st
import requests
import os

# Pega a URL da API (Flask) que configuraremos no Kubernetes
API_URL = os.getenv("API_URL", "http://localhost:5000")

st.set_page_config(page_title="CyberFrame AI", page_icon="⚡", layout="centered")

# ==========================================
# CSS CUSTOMIZADO (NEON E FUTURISTA)
# ==========================================
st.markdown("""
    <style>
    /* Brilho nos títulos */
    h1, h2, h3 {
        text-shadow: 0 0 10px #00f3ff, 0 0 20px #00f3ff;
        color: #ffffff;
    }
    
    /* Efeito na barra lateral */
    [data-testid="stSidebar"] {
        border-right: 2px solid #00f3ff;
        box-shadow: 2px 0 15px rgba(0, 243, 255, 0.2);
    }
    
    /* Botões Futuristas */
    .stButton > button {
        background: transparent;
        border: 1px solid #00f3ff;
        color: #00f3ff;
        transition: all 0.3s ease;
        box-shadow: 0 0 10px rgba(0, 243, 255, 0.1);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton > button:hover {
        background: #00f3ff;
        color: #000000;
        box-shadow: 0 0 20px rgba(0, 243, 255, 0.6);
        border-color: #00f3ff;
    }
    
    /* Mensagens de sucesso com borda neon verde */
    [data-testid="stNotification"] {
        border: 1px solid #00ff66;
        background-color: rgba(0, 255, 102, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# LOGO SVG E TÍTULO
# ==========================================
logo_svg = """
<div style="display: flex; justify-content: center; margin-bottom: 20px;">
    <svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="neonGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#00f3ff" />
                <stop offset="100%" stop-color="#bf00ff" />
            </linearGradient>
            <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="5" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
        </defs>
        <path d="M50 10 L90 30 L90 70 L50 90 L10 70 L10 30 Z" fill="none" stroke="url(#neonGradient)" stroke-width="4" filter="url(#glow)"/>
        <circle cx="50" cy="50" r="15" fill="none" stroke="#00f3ff" stroke-width="3" filter="url(#glow)"/>
        <circle cx="50" cy="50" r="5" fill="#00f3ff" filter="url(#glow)"/>
        <path d="M35 50 L65 50 M50 35 L50 65" stroke="url(#neonGradient)" stroke-width="2" opacity="0.5"/>
    </svg>
</div>
<h1 style='text-align: center;'>CYBERFRAME AI</h1>
<p style='text-align: center; color: #a0a0a0; font-family: monospace;'>v2.0 // Powered by FIAP X</p>
"""
st.markdown(logo_svg, unsafe_allow_html=True)

# Inicializa o estado para guardar o Token do usuário logado
if 'token' not in st.session_state:
    st.session_state['token'] = None

# ==========================================
# BARRA LATERAL (LOGIN / REGISTRO)
# ==========================================
with st.sidebar:
    if st.session_state['token'] is None:
        st.header("⎋ SYSTEM LOGIN")
        tab1, tab2 = st.tabs(["Acesso", "Novo Registro"])
        
        with tab1:
            l_user = st.text_input("ID Usuário", key="l_user")
            l_pass = st.text_input("Senha", type="password", key="l_pass")
            if st.button(">> Entrar"):
                try:
                    res = requests.post(f"{API_URL}/login", json={"username": l_user, "password": l_pass})
                    if res.status_code == 200:
                        st.session_state['token'] = res.json().get('access_token')
                        st.success("Acesso Liberado.")
                        st.rerun()
                    else:
                        st.error("Acesso Negado.")
                except Exception as e:
                    st.error("Offline: API inalcançável.")
                    
        with tab2:
            r_user = st.text_input("Novo ID", key="r_user")
            r_pass = st.text_input("Nova Senha", type="password", key="r_pass")
            if st.button(">> Registrar"):
                try:
                    res = requests.post(f"{API_URL}/register", json={"username": r_user, "password": r_pass})
                    if res.status_code == 201:
                        st.success("Identidade registrada! Faça o login.")
                    else:
                        st.error("Erro no registro.")
                except Exception:
                    st.error("Offline: API inalcançável.")
    else:
        st.success("🟢 Conexão Estabelecida")
        if st.button("<< Disconnect"):
            st.session_state['token'] = None
            st.rerun()

# ==========================================
# TELA PRINCIPAL (LOGADO)
# ==========================================
if st.session_state['token']:
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    
    st.subheader("⚡ INGESTÃO DE DADOS (UPLOAD)")
    uploaded_file = st.file_uploader("SELECIONE O ARQUIVO DE VÍDEO (.MP4)", type=["mp4", "avi", "mov"])
    
    if st.button("INICIALIZAR EXTRAÇÃO"):
        if uploaded_file is not None:
            with st.spinner("Transmitindo pacote de dados..."):
                try:
                    files = {'video': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    res = requests.post(f"{API_URL}/upload", headers=headers, files=files)
                    if res.status_code == 202:
                        st.success("✅ Pacote injetado na Fila de Processamento Neural (SQS)!")
                    else:
                        st.error("❌ Falha na injeção de dados.")
                except Exception:
                    st.error("Erro de comunicação com os servidores centrais.")
        else:
            st.warning("Nenhum arquivo detectado no scanner.")
            
    st.divider()
    
    st.subheader("📡 STATUS DE PROCESSAMENTO")
    col1, col2 = st.columns([0.8, 0.2])
    with col2:
        if st.button("SYNC ⟳"):
            pass 
            
    try:
        res_videos = requests.get(f"{API_URL}/videos", headers=headers)
        if res_videos.status_code == 200:
            videos = res_videos.json()
            if not videos:
                st.info("Nenhum dado no histórico.")
            else:
                for v in videos:
                    status = v['status']
                    # Cores neon baseadas no status
                    cor = "🟡" if status == "NA_FILA" else "🔵" if status == "PROCESSANDO" else "🟢" if status == "CONCLUIDO" else "🔴"
                    
                    with st.expander(f"{cor} {v['filename']} | STATUS: {status}"):
                        st.write(f"**Timestamp:** {v['data_upload']}")
                        
                        if status == "CONCLUIDO" and v.get('download_url'):
                            st.markdown(f"### [🔗 DOWNLOAD PACOTE COMPRESSO (.ZIP)]({v['download_url']})")
                        elif status == "ERRO":
                            st.error("Falha crítica no Worker. Arquivo corrompido.")
                        else:
                            st.info("Engrenagens trabalhando... Arquivo na fila SQS ou em extração.")
    except Exception as e:
        st.error("Conexão perdida com o banco de dados.")
else:
    st.info("⚠️ REQUIRES AUTHENTICATION: Conecte-se pelo terminal lateral para liberar as ferramentas.")