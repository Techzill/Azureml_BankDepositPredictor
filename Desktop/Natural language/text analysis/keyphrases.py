from dotenv import load_dotenv
import os
import PyPDF2

# Import namespaces
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

def main():
    try:
        # Load environment variables
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')

        # Create client using endpoint and key
        credential = AzureKeyCredential(ai_key)
        ai_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)

        # Analyze the PDF file
        books_folder = 'books'
        pdf_file_path = os.path.join(books_folder, 'Atomic Habits.pdf')

        # Open the PDF file and extract text
        with open(pdf_file_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page_num in range(len(reader.pages)):
                page_text = reader.pages[page_num].extract_text()
                text += page_text

        # Split the text into chunks of less than 5120 characters
        max_chunk_size = 5120
        chunks = [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]

        # Initialize a set to store unique key phrases
        all_key_phrases = set()

        # Process each chunk for key phrases
        for idx, chunk in enumerate(chunks):
            print(f'\nProcessing chunk {idx + 1} of {len(chunks)}...')

            try:
                # Extract key phrases for the chunk
                key_phrases_result = ai_client.extract_key_phrases(documents=[chunk])[0]
                print(f"Key Phrases for Chunk {idx + 1}:")
                for phrase in key_phrases_result.key_phrases:
                    print(f"\t{phrase}")
                    all_key_phrases.add(phrase)

            except Exception as ex:
                print(f"Error processing chunk {idx + 1}: {ex}")

        # Print all the unique key phrases across all chunks
        print("\nAll Key Phrases from the Document:")
        for phrase in all_key_phrases:
            print(f"\t{phrase}")

    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()
