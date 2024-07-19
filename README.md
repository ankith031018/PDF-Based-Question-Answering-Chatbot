# PDF-Based-Question-Answering-Chatbot
The PDF-Based Question Answering Chatbot is an interactive bot designed to answer questions based on the content of a given PDF document. Utilizing the PyPDF2 library for text extraction and the nltk library for natural language processing, this chatbot extracts text from a specified PDF file and processes user queries to provide relevant answers.
Text Extraction from PDF:

Uses PyPDF2 to read and extract text from PDF files.
Supports multi-page PDFs, consolidating text into a single string for processing.
Natural Language Processing:

Employs nltk for tokenizing and processing text.
Identifies common tokens between user questions and the extracted text to find relevant sentences.
Provides the first matching sentence as the answer to user queries.
Interactive Question-Answering:

Operates in an interactive loop, allowing users to ask questions continuously.
Responds to each question based on the extracted knowledge from the PDF.
Users can exit the loop by typing 'exit'.
Usage:

Setup:

Ensure the required libraries (PyPDF2 and nltk) are installed.
Place the PDF file (e.g., Meditations.pdf) in the same directory as the script.
Running the Bot:

Execute the script.
The bot will extract text from the specified PDF file.
Once text extraction is complete, users can start asking questions.
Interacting with the Bot:

Type a question and press Enter to receive an answer.
The bot will display the answer based on the extracted text.
Type 'exit' to quit the interactive session.
