from django.http import FileResponse
import os
from django.shortcuts import render
from PyPDF2 import PdfMerger
from io import BytesIO
from PIL import Image

def merge(request):
    if request.method == 'POST':
        # Handling PDF files merge
        if request.FILES.getlist('pdf_files'):
            pdf_files = request.FILES.getlist('pdf_files')
            merged_pdf_name = 'merged_pdf.pdf'
            merger = PdfMerger()
            
            # Merge selected PDF files
            for pdf_file in pdf_files:
                merger.append(pdf_file)
            
            # Get the directory of the first selected PDF file for saving the merged PDF
            if pdf_files:
                destination_folder = os.path.dirname(pdf_files[0].name)
                merged_pdf_path = os.path.join(destination_folder, merged_pdf_name)
                with open(merged_pdf_path, 'wb') as merged_pdf:
                    merger.write(merged_pdf)
                
                # Serve the merged PDF for download
                return FileResponse(open(merged_pdf_path, 'rb'), as_attachment=True)
        
        # Handling Image files merge
        if request.FILES.getlist('image_files'):
            image_files = request.FILES.getlist('image_files')
            merged_image_name = 'merged_image.pdf'
            image_merger = PdfMerger()
            
            # Convert images to PDF and merge
            for image_file in image_files:
                image = Image.open(image_file)
                pdf_bytes = BytesIO()
                image.save(pdf_bytes, format='PDF')
                pdf_bytes.seek(0)
                image_merger.append(pdf_bytes)
            
            # Generate a temporary file for the merged PDF
            temp_merged_path = os.path.join(os.path.dirname(image_files[0].name), merged_image_name)
            with open(temp_merged_path, 'wb') as temp_merged_pdf:
                image_merger.write(temp_merged_pdf)
            
            # Serve the merged PDF for download
            return FileResponse(open(temp_merged_path, 'rb'), as_attachment=True)
    
    # Render the merge.html template if no files were processed
    return render(request, 'merge.html')
