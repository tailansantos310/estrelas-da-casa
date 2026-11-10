import streamlit as st
import random
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Estrelas da Casa", page_icon="⭐", layout="wide")

# Inicialização do banco de dados simulado no estado da sessão
if "jogadores" not in st.session_state:
    st.session_state.jogadores = {
        "TAILAN": {"estrelas": 0, "historico_dados": [], "cartas": []},
        "CAIO": {"estrelas": 0, "historico_dados": [], "cartas": []},
        "CAROL": {"estrelas": 0, "historico_dados": [], "cartas": []},
        "KARINE": {"estrelas": 0, "historico_dados": [], "cartas": []}
    }

if "tarefas_dia" not in st.session_state:
    st.session_state.tarefas_dia = {
        j: {t: False for t in [
            "🍳 Café da manhã", "🍳 Café da tarde", "🍳 Almoço", "🍳 Janta", "🍳 Fogão janta",
            "🧹 Varrer", "🧹 Pano", "🧹 Organizar", "🧹 Garrafas", "🚽 Banheiro", "👕 Roupa"
        ]} for j in st.session_state.jogadores
    }

st.title("⭐ ESTRELAS DA CASA - CADA UM POR SI ⭐")
st.write("---")

# Abas principais
aba_painel, aba_tarefas, aba_dados, aba_regras = st.tabs([
    "🏆 Painel Geral", "📝 Tarefas Diárias", "🎲 Dado do Dia", "📜 Regras & Prêmios"
])

# --- ABA 1: PAINEL GERAL ---
with aba_painel:
    st.header("🏆 Ranking Atual")
    
    # Criar DataFrame para exibição do ranking
    dados_ranking = []
    for j, dados in st.session_state.jogadores.items():
        # Verificação de liberações por estrelas
        cartas_liberadas = []
        if dados["estrelas"] >= 35: cartas_liberadas.append("👻 FANTASMA")
        if dados["estrelas"] >= 45: cartas_liberadas.append("🛡️ ESCUDO")
        if dados["estrelas"] >= 55: cartas_liberadas.append("👑 CHEFE")
        if dados["estrelas"] >= 65: cartas_liberadas.append("🃏 CORINGA")
        
        dados_ranking.append({
            "Jogador": j,
            "Estrelas ⭐": dados["estrelas"],
            "Cartas Liberadas 🃏": ", ".join(cartas_liberadas) if cartas_liberadas else "Nenhuma"
        })
    
    df_ranking = pd.DataFrame(dados_ranking).sort_values(by="Estrelas ⭐", ascending=False)
    st.table(df_ranking)
    
    st.subheader("⚠️ Situação da Punição (Fim de Semana)")
    ultimo_lugar = df_ranking.iloc[-1]["Jogador"]
    st.error(f"Se a semana terminasse agora, **{ultimo_lugar}** pagaria a punição!")

# --- ABA 2: TAREFAS DIÁRIAS ---
with aba_tarefas:
    st.header("📝 Marcar Tarefas do Dia")
    st.caption("Aviso: Mentir que fez o item custará 5 ⭐!")
    
    jogador_selecionado = st.selectbox("Quem está registrando?", list(st.session_state.jogadores.keys()))
    
    st.subheader(f"Tarefas de {jogador_selecionado}")
    
    for tarefa in st.session_state.tarefas_dia[jogador_selecionado].keys():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(tarefa)
        with col2:
            # Se já marcou hoje, fica salvo
            concluido = st.checkbox("Feito", key=f"{jogador_selecionado}_{tarefa}", 
                                    value=st.session_state.tarefas_dia[jogador_selecionado][tarefa])
            if concluído != st.session_state.tarefas_dia[jogador_selecionado][tarefa]:
                st.session_state.tarefas_dia[jogador_selecionado][tarefa] = concluído
                if concluído:
                    st.session_state.jogadores[jogador_selecionado]["estrelas"] += 1
                else:
                    st.session_state.jogadores[jogador_selecionado]["estrelas"] -= 1
                    
    st.success(f"Estrelas acumuladas de {jogador_selecionado}: {st.session_state.jogadores[jogador_selecionado]['estrelas']} ⭐")

# --- ABA 3: DADO DO DIA ---
with aba_dados:
    st.header("🎲 Rolar o Dado Diário")
    
    jogador_dado = st.selectbox("Escolha o jogador para rolar o dado:", list(st.session_state.jogadores.keys()), key="dado_jog")
    
    if st.button(f"Jogar Dado para {jogador_dado}"):
        resultado = random.randint(1, 6)
        st.subheader(f"Resultado do Dado: {resultado}")
        
        # Regras do dado
        if resultado == 1:
            st.session_state.jogadores[jogador_dado]["estrelas"] -= 1
            st.error("Perdeu 1 estrela! 😢")
        elif resultado == 2:
            st.info("Nada aconteceu. 🧘")
        elif resultado == 3:
            st.session_state.jogadores[jogador_dado]["estrelas"] += 1
            st.success("+1 estrela ganha! 📈")
        elif resultado == 4:
            st.warning("Ganhou 🛡️ ESCUDO!")
        elif resultado == 5:
            st.warning("Ganhou 👻 FANTASMA!")
        elif resultado == 6:
            st.warning("Ganhou 👑 CHEFE!")

# --- ABA 4: REGRAS & PRÊMIOS ---
with aba_regras:
    st.header("📜 Regras Oficiais do Jogo")
    st.markdown("""
    * **Funcionamento:** De Segunda a Domingo, todos os participantes realizam as mesmas 11 tarefas.
    * **Pontuação:** Cada tarefa feita garante **1 ⭐**. Deixar de fazer remove a estrela e acumula a obrigação para o dia seguinte.
    * **Penalidade:** Mentir que fez uma tarefa resulta na perda imediata de **5 ⭐**.
    * **Cartas de Poder (Liberações):**
        * **35 Estrelas:** 👻 FANTASMA (Faz 1 tarefa sumir)
        * **45 Estrelas:** 🛡️ ESCUDO (Não perde estrela por 1 tarefa não feita)
        * **55 Estrelas:** 👑 CHEFE (Manda outra pessoa fazer 1 tarefa sua)
        * **65 Estrelas:** 🃏 CORINGA (Vira Fantasma, Escudo ou Chefe)
    
    ### ⚠️ PUNIÇÃO (Último lugar no Domingo à noite)
    * Lavar a louça da semana toda sozinho.
    * Limpar o banheiro sozinho por 4 dias.
    * Fazer a janta sozinho por 3 dias.
    * Encher as garrafas a semana toda.

    ### 💰 PRÊMIO
    * No fim do ano, quem tiver acumulado mais estrelas ganha **R$ 150,00**!
    """)
