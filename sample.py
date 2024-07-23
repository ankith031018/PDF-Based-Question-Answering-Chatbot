import streamlit as st
import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist

# Ensure necessary NLTK data packages are downloaded
nltk.download('punkt')
nltk.download('stopwords')

def extract_text_pypdf2(pdf_path):
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        return text
    except FileNotFoundError:
        return "The specified PDF file was not found."

def summarize_text(text, num_sentences=3):
    # Tokenize the text
    tokens = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words and word.isalnum()]

    # Calculate word frequencies
    freq = FreqDist(filtered_tokens)

    # Rank sentences based on word frequencies
    sentences = sent_tokenize(text)
    ranking = {}
    for i, sentence in enumerate(sentences):
        sentence_tokens = word_tokenize(sentence)
        sentence_score = sum(freq[word] for word in sentence_tokens)
        ranking[i] = sentence_score

    # Get the top-ranked sentences
    sorted_ranking = sorted(ranking, key=ranking.get, reverse=True)[:num_sentences]
    summary = ' '.join(sentences[i] for i in sorted(sorted_ranking))

    return summary

def answer_question(question, text):
    question_tokens = nltk.word_tokenize(question)
    text_tokens = nltk.word_tokenize(text)

    question_tokens = [token.lower() for token in question_tokens if token.isalnum()]
    text_tokens = [token.lower() for token in text_tokens if token.isalnum()]

    common_tokens = set(question_tokens) & set(text_tokens)

    sentences = nltk.sent_tokenize(text)
    candidate_answers = [sentence for sentence in sentences if any(word in nltk.word_tokenize(sentence.lower()) for word in common_tokens)]

    if not candidate_answers:
        return "Sorry, I couldn't find an answer to that question."

    return candidate_answers[0]

# Streamlit application
def main():
    st.title("PDF Text Extractor and Analyzer")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        pdf_path = uploaded_file.name
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.write("Extracting text from PDF...")
        extracted_text_pypdf2 = extract_text_pypdf2(pdf_path)

        if extracted_text_pypdf2 == "The specified PDF file was not found.":
            st.error(extracted_text_pypdf2)
            return

        st.success("Text extraction complete.")

        option = st.selectbox(
            'Choose an option',
            ('Ask a question', 'Summarize the text', 'Print the entire PDF text', 'Exit')
        )

        if option == 'Ask a question':
            question = st.text_input("Enter your question")
            if question:
                answer = answer_question(question, extracted_text_pypdf2)
                st.write(f"Answer: {answer}")
        
        elif option == 'Summarize the text':
            num_sentences = st.slider("Number of sentences in summary", 1, 10, 3)
            summary = summarize_text(extracted_text_pypdf2, num_sentences)
            st.write(f"Summary:\n{summary}")
        
        elif option == 'Print the entire PDF text':
            st.text_area("Full PDF Text", extracted_text_pypdf2, height=300)
        
        elif option == 'Exit':
            st.write("Exiting...")

if __name__ == "__main__":
    main()
