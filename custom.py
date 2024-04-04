import fitz  # PyMuPDF
from transformers import BartForConditionalGeneration, BartTokenizer
import textwrap
import torch

def get_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ''
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text += page.get_text()
    return text

def summarize_text(pdf_path):

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    text = get_text_from_pdf(pdf_path)
    model_name = "facebook/bart-large-cnn"
    model = BartForConditionalGeneration.from_pretrained(model_name)
    tokenizer = BartTokenizer.from_pretrained(model_name)

    if device.type == 'cuda':
        model.to(device)
    

    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
    if device.type == 'cuda':
        inputs = inputs.to(device)
    summary_ids = model.generate(inputs, max_length=150, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    formatted_summary = "\n".join(textwrap.wrap(summary, width=80))
    return formatted_summary

def save_summary_as_pdf(pdf_path, summary):
    doc = fitz.open()

    page = doc.new_page()
    page.insert_text((10, 100), summary, fontname="helv", fontsize=12)  # Adjust the vertical position as needed

    output_pdf_path = pdf_path.replace(".pdf", "_summary.pdf")
    doc.save(output_pdf_path)
    doc.close()

    return output_pdf_path


pdf_file_path = "intersteller_plot.pdf"
summary = summarize_text(pdf_file_path)
output_pdf_path = save_summary_as_pdf(pdf_file_path, summary)
print("Summary saved as PDF:", output_pdf_path)

pdf_file_path = "tech_paper.pdf"
summary = summarize_text(pdf_file_path)
output_pdf_path = save_summary_as_pdf(pdf_file_path, summary)
print("Summary saved as PDF:", output_pdf_path)