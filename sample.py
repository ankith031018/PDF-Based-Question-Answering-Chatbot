import PyPDF2
import nltk

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

def main():
    pdf_path = 'C:\\MARCUS AURELIUS\\bot\\Meditations.pdf'
    print("Extracting text from PDF with PyPDF2...")
    extracted_text_pypdf2 = extract_text_pypdf2(pdf_path)

    if extracted_text_pypdf2 == "The specified PDF file was not found.":
        print(extracted_text_pypdf2)
        return

    print("Text extraction complete. You can now ask questions.")

    while True:
        question = input("Enter your question (or type 'exit' to quit): ")
        if question.lower() == 'exit':
            break
        answer = answer_question(question, extracted_text_pypdf2)
        print(f"Answer: {answer}\n")

if __name__ == "__main__":
    main()


#C:\\MARCUS AURELIUS\\bot\\Meditations.pdf