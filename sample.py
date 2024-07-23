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

def main():
    pdf_path = "C:\\Users\\Student.DESKTOP-G81TD8G.000\\Downloads\\Meditations.pdf"
    print("Extracting text from PDF with PyPDF2...")
    extracted_text_pypdf2 = extract_text_pypdf2(pdf_path)

    if extracted_text_pypdf2 == "The specified PDF file was not found.":
        print(extracted_text_pypdf2)
        return

    print("Text extraction complete.")

    while True:
        print("\nChoose an option:")
        print("1. Ask a question")
        print("2. Summarize the text")
        print("3. Print the entire PDF text")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            question = input("Enter your question (or type 'exit' to quit): ")
            if question.lower() == 'exit':
                break
            answer = answer_question(question, extracted_text_pypdf2)
            print(f"Answer: {answer}\n")
       
        elif choice == '2':
            summary = summarize_text(extracted_text_pypdf2)
            print(f"Summary:\n{summary}\n")

        elif choice == '3':
            print(f"Full PDF Text:\n{extracted_text_pypdf2}\n")

        elif choice == '4':
            break
       
        else:
            print("Invalid choice. Please choose again.")

    print("Exiting...")

if __name__ == "__main__":
    main()
