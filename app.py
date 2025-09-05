import nltk
from textblob import download_corpora

# Baixa corpora necessários para o TextBlob
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('brown')
download_corpora.lite()  # Baixa só os essenciais do TextBlob

st.set_page_config(page_title="Corretor de Redação UFRGS", layout="wide")

st.title("Corretor de Redação UFRGS (Simulado)")

st.markdown("""
Digite sua redação abaixo e, opcionalmente, palavras-chave do tema.
O corretor irá fornecer **feedback escrito detalhado** e **notas por critério**.
""")

essay = st.text_area("Digite sua redação:", height=300)
theme_keywords_input = st.text_input("Palavras-chave do tema (separadas por vírgula, opcional):")
theme_keywords = [kw.strip() for kw in theme_keywords_input.split(',')] if theme_keywords_input else []

if st.button("Avaliar redação"):
    if essay.strip() == "":
        st.warning("Digite uma redação antes de avaliar!")
    else:
        result = analyze_text(essay, theme_keywords)
        
        st.subheader("Feedback Escrito Detalhado")
        for key, comment in result['feedback_text'].items():
            st.markdown(f"**{key.capitalize()}:** {comment}")
        
        st.subheader("Notas por Critério")
        st.markdown(f"- Adequação ao tema: {result['theme_score']} / 3")
        st.markdown(f"- Organização e estrutura: {result['structure_score']} / 3")
        st.markdown(f"- Coesão e coerência: {result['coherence_score']} / 3")
        st.markdown(f"- Vocabulário e repertório: {result['vocab_score']} / 3")
        st.markdown(f"- Gramática e ortografia: {result['grammar_score']} / 3")
        st.markdown(f"**Nota final: {result['total_score']} / 15**")
        
        st.subheader("Informações adicionais")
        st.markdown(f"- Número de parágrafos: {result['num_paragraphs']}")
        st.markdown(f"- Número de linhas: {result['num_lines']}")
        st.markdown(f"- Número de palavras: {result['total_words']}")
