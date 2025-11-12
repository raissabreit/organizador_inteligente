import streamlit as st
import os
from database import criar_banco, obter_historico
from monitor import iniciar_monitoramento
from config import EXTENSOES, PASTA_ORGANIZADA

st.set_page_config(page_title="Organizador Inteligente", page_icon="📁", layout="wide")
criar_banco()

st.title("📁 Organizador Inteligente de Arquivos")
st.markdown("---")

# Botão para iniciar monitoramento
if st.button("🔄 Iniciar Monitoramento", type="primary"):
    try:
        observer = iniciar_monitoramento()
        st.success("Monitoramento iniciado! Os arquivos serão organizados automaticamente.")
        st.info("Coloque arquivos na pasta 'Downloads' para testar.")
    except Exception as e:
        st.error(f"Erro: {e}")

# Estatísticas
st.subheader("📊 Estatísticas")
col1, col2, col3 = st.columns(3)

def contar_arquivos():
    contagens = {}
    for categoria in EXTENSOES.keys():
        pasta_categoria = os.path.join(PASTA_ORGANIZADA, categoria)
        if os.path.exists(pasta_categoria):
            contagens[categoria] = len([f for f in os.listdir(pasta_categoria) 
                                      if os.path.isfile(os.path.join(pasta_categoria, f))])
        else:
            contagens[categoria] = 0
    return contagens

contagens = contar_arquivos()

with col1:
    st.metric("Imagens", contagens["Imagens"])
with col2:
    st.metric("Vídeos", contagens["Vídeos"])
with col3:
    st.metric("Documentos", contagens["Documentos"])

# Histórico
st.markdown("---")
st.subheader("📋 Histórico de Movimentações")

df_historico = obter_historico()
if not df_historico.empty:
    st.dataframe(df_historico[['nome_arquivo', 'tipo', 'data_hora']], 
                use_container_width=True, hide_index=True)
else:
    st.info("Nenhuma movimentação registrada ainda.")
