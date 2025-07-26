from django.shortcuts import render, redirect
from .models import PDFUpload
from .utils.pdf_extractor import extract_text_from_pdf
from .utils.heading_extractor import extract_chapter_headings
from .utils.summarizer import summarize_text

def upload_pdf(request):
    if request.method == 'POST':
        pdf = request.FILES['pdf']
        obj = PDFUpload.objects.create(file=pdf)

        # Step 1: Extract full text from PDF
        full_text = extract_text_from_pdf(obj.file.path)
        print("✅ PDF Extracted Pages:", len(full_text))

        if len(full_text) > 5:
            print("📄 Sample from Page 6:\n", full_text[5][:1000])
        else:
            print("⚠️ Not enough pages to show sample.")

        # Step 2: Extract chapter headings
        headings = extract_chapter_headings(full_text)
        print("🧠 Total Headings Detected:", len(headings))

        # Step 3: Summarize first 3 chapters only (for speed)
        chapters = []
        for i, (title, idx) in enumerate(headings[:3]):
            print(f"\n📚 Chapter {i+1}: {title}")
            raw_text = full_text[idx]

            print("⏳ Summarizing...")
            summary = summarize_text(raw_text)
            print(f"✅ Done summarizing: {title}")

            chapters.append({
                'title': title,
                'page': idx + 1,
                'summary': summary,
            })

        return render(request, 'processor/view_pdf.html', {
            'chapters': chapters,
            'pdf_url': obj.file.url
        })

    return render(request, 'processor/upload.html')
