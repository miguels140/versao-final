# grading.py
import re
from textblob import TextBlob

def clean_text(text):
    return re.sub(r'\s+', ' ', text.strip())

def count_lines(text):
    return text.count('\n') + 1

def analyze_text(text, theme_keywords=[]):
    text = clean_text(text)
    blob = TextBlob(text)
    words = text.split()
    sentences = blob.sentences
    total_words = len(words)
    
    feedback_text = {}
    
    # 1. Adequação ao tema (0 a 3)
    if theme_keywords:
        theme_matches = sum(1 for kw in theme_keywords if kw.lower() in text.lower())
        theme_score = min(3, theme_matches)
        if theme_score == 3:
            feedback_text['tema'] = "A redação atende muito bem ao tema proposto."
        elif theme_score >= 1:
            feedback_text['tema'] = "A redação aborda parcialmente o tema, mas poderia explorar mais algumas ideias relacionadas."
        else:
            feedback_text['tema'] = "A redação não aborda adequadamente o tema proposto."
    else:
        theme_score = 3
        feedback_text['tema'] = "Tema não especificado; assumido como adequado."
    
    # 2. Organização e estrutura (0 a 3)
    paragraphs = text.split('\n')
    num_paragraphs = len(paragraphs)
    structure_score = 0
    if num_paragraphs >= 3:
        structure_score += 1
    if num_paragraphs >= 4:
        structure_score += 1
    if num_paragraphs >= 5:
        structure_score += 1
    
    if structure_score == 3:
        feedback_text['estrutura'] = "A redação apresenta boa organização com introdução, desenvolvimento e conclusão bem definidos."
    elif structure_score == 2:
        feedback_text['estrutura'] = "A redação tem estrutura razoável, mas alguns parágrafos poderiam ser melhor desenvolvidos."
    else:
        feedback_text['estrutura'] = "A redação apresenta pouca organização; é difícil identificar claramente a introdução, desenvolvimento e conclusão."
    
    # 3. Coesão e coerência (0 a 3)
    connectors = ['portanto', 'entretanto', 'além disso', 'assim', 'logo', 'porém', 'todavia', 'no entanto']
    connector_count = sum(text.lower().count(c) for c in connectors)
    coherence_score = min(3, connector_count)
    
    if coherence_score == 3:
        feedback_text['coesao'] = "O texto apresenta excelente coesão, com ideias bem conectadas e transições claras entre os parágrafos."
    elif coherence_score == 2:
        feedback_text['coesao'] = "O texto apresenta coesão moderada, mas algumas transições entre ideias poderiam ser mais claras."
    else:
        feedback_text['coesao'] = "O texto apresenta baixa coesão, com ideias pouco conectadas e transições confusas."
    
    # 4. Vocabulário e repertório (0 a 3)
    unique_words = set(words)
    vocab_score = min(3, len(unique_words)/20)
    
    if vocab_score == 3:
        feedback_text['vocabulario'] = "O vocabulário é variado e adequado ao registro formal exigido."
    elif vocab_score >= 1.5:
        feedback_text['vocabulario'] = "O vocabulário é razoável, mas poderia incluir termos mais variados ou precisos."
    else:
        feedback_text['vocabulario'] = "O vocabulário é limitado ou repetitivo; recomenda-se maior diversidade lexical."
    
    # 5. Gramática e ortografia (0 a 3)
    misspelled = sum(1 for word in words if TextBlob(word).correct() != word)
    grammar_score = max(0, 3 - misspelled/5)
    
    if grammar_score == 3:
        feedback_text['gramatica'] = "A redação apresenta ótima gramática e ortografia, sem erros significativos."
    elif grammar_score >= 1.5:
        feedback_text['gramatica'] = "A redação apresenta alguns erros gramaticais ou ortográficos que poderiam ser corrigidos."
    else:
        feedback_text['gramatica'] = "A redação apresenta vários erros gramaticais e ortográficos que comprometem a clareza do texto."
    
    # Nota final
    total_score = round(theme_score + structure_score + coherence_score + vocab_score + grammar_score)
    total_score = max(1, min(15, total_score))
    
    feedback = {
        'theme_score': round(theme_score, 2),
        'structure_score': round(structure_score, 2),
        'coherence_score': round(coherence_score, 2),
        'vocab_score': round(vocab_score, 2),
        'grammar_score': round(grammar_score, 2),
        'total_score': total_score,
        'num_paragraphs': num_paragraphs,
        'num_lines': count_lines(text),
        'total_words': total_words,
        'feedback_text': feedback_text
    }
    
    return feedback
