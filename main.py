import streamlit as st
import os
import shutil
import speech_recognition as sr
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
import base64

def transcribe_audio(audio_file_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file_path) as audio_file:
        audio_data = recognizer.record(audio_file)

        try:
            transcribed_text = recognizer.recognize_google(audio_data)
            return transcribed_text
        except sr.UnknownValueError:
            return "Error: Could not understand the audio."
        except sr.RequestError as e:
            return f"Error: {e}"

def save_to_pdf(transcribed_text, output_file_path):
    doc = SimpleDocTemplate(output_file_path, pagesize=letter)
    styles = getSampleStyleSheet()
    content = [Paragraph(text, styles["Normal"]) for text in transcribed_text.split("\n") if text.strip()]
    doc.build(content)

def get_pdf_download_link(file_path):
    with open(file_path, "rb") as file:
        pdf_bytes = file.read()
        b64 = base64.b64encode(pdf_bytes).decode()
        href = f"<a href='data:application/octet-stream;base64,{b64}' download='transcription.pdf'>Download PDF</a>"
        return href

def main():
    st.title("Audio Transcription and PDF Generation")

    uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])

    if uploaded_file:
        # Create a temporary directory to save the uploaded audio file
        temp_directory = "temp_audio"
        os.makedirs(temp_directory, exist_ok=True)

        # Save the uploaded audio file to the temporary directory
        audio_file_path = os.path.join(temp_directory, uploaded_file.name)
        with open(audio_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.audio(uploaded_file)

        if st.button("Generate PDF"):
            # Transcribe the audio
            result = transcribe_audio(audio_file_path)

            # Create a directory to save the generated PDF
            pdf_directory = "output_pdf"
            os.makedirs(pdf_directory, exist_ok=True)

            # Generate the PDF file
            output_file_path = os.path.join(pdf_directory, "transcription.pdf")
            save_to_pdf(result, output_file_path)

            st.success("Transcription and PDF generation completed successfully!")
            st.markdown(get_pdf_download_link(output_file_path), unsafe_allow_html=True)

            # Remove the temporary audio directory after processing
            shutil.rmtree(temp_directory)

if __name__ == "__main__":
    main()