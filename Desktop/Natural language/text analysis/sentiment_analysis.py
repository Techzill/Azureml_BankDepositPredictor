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

        # Detect sentiment for each chunk
        for idx, chunk in enumerate(chunks):
            print(f'\nProcessing chunk {idx + 1} of {len(chunks)}...')

            # Print the content of the chunk
            print(f"\nChunk {idx + 1} Content (First 500 characters):\n{chunk[:500]}...\n")

            try:
                # Perform sentiment analysis on the chunk
                sentiment_analysis = ai_client.analyze_sentiment(documents=[chunk])[0]

                # Bold formatting using ANSI escape codes
                bold_start = "\033[1m"
                bold_end = "\033[0m"

                # Print the detected sentiment in bold
                print(f"{bold_start}Detected sentiment for chunk {idx + 1}:{bold_end} {sentiment_analysis.sentiment}")
                print(f"{bold_start}Confidence scores:{bold_end} Positive: {sentiment_analysis.confidence_scores.positive}, "
                      f"Neutral: {sentiment_analysis.confidence_scores.neutral}, "
                      f"Negative: {sentiment_analysis.confidence_scores.negative}")
            except Exception as ex:
                print(f"Error processing chunk {idx + 1}: {ex}")

    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()
