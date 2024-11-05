from dotenv import load_dotenv
import os
import PyPDF2
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

        # Process each chunk for linked entity extraction
        for idx, chunk in enumerate(chunks):
            print(f'\nProcessing chunk {idx + 1} of {len(chunks)}...')
            
            # Extract linked entities from each chunk
            try:
                linked_entities = ai_client.recognize_linked_entities(documents=[chunk])[0].entities
                if len(linked_entities) > 0:
                    print("\nLinked Entities:")
                    for linked_entity in linked_entities:
                        print(f'\t{linked_entity.name} ({linked_entity.url}) - Data Source: {linked_entity.data_source}')
            except Exception as ex:
                print(f"Error processing chunk {idx + 1}: {ex}")

    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()
