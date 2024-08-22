# uploadgamefiles/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import GameForm
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.graphics.shapes import Drawing, Line
from reportlab.lib.colors import red
from io import BytesIO
import tempfile
import os
from reportlab.lib.enums import TA_CENTER

# Google Drive API imports
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'service_account.json'
PARENT_FOLDER_ID = "1ikmp1_wgrqjkL7h0PNzsFYsHJBDaa9_I"

def authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def set_file_permissions(service, file_id):
    permission = {
        'type': 'anyone',
        'role': 'reader'
    }
    service.permissions().create(
        fileId=file_id,
        body=permission
    ).execute()

def upload_file_to_drive(file_path):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)
    
    file_name = os.path.basename(file_path)

    file_metadata = {
        'name': file_name,
        'parents': [PARENT_FOLDER_ID]
    }

    media = MediaFileUpload(file_path, resumable=True)
    request = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%.")

    file_id = response.get('id')
    print(f"File ID: {file_id}")

    set_file_permissions(service, file_id)

    file = service.files().get(fileId=file_id, fields='webViewLink').execute()
    webViewLink = file.get('webViewLink')
    print(f"File link: {webViewLink}")
    return webViewLink

def add_page_border(canvas, doc):
    width, height = letter
    margin = 30
    border_width = 3

    canvas.setStrokeColor('black')
    canvas.setLineWidth(border_width)
    canvas.rect(
        margin - border_width, 
        margin - border_width, 
        width - 2 * margin + 2 * border_width, 
        height - 2 * margin + 2 * border_width
    )

def generate_pdf(game_name, game_size, game_links):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    elements = []
        # Add the header in red color
    header_style = ParagraphStyle(
        name='HeaderStyle',
        fontSize=14,
        textColor=red,
        alignment=TA_CENTER,
        spaceAfter=20
    )
    elements.append(Paragraph("PLEASE DON'T SHARE QR CODE IMAGE IN REVIEW", header_style))
    elements.append(Spacer(1, 12))


    title_style = styles['Title']
    title_style.fontSize = 14
    title_style.alignment = 0
    
    link_style = ParagraphStyle(
        name='LinkStyle',
        fontSize=12,
        textColor=(0, 0, 1),
        underline=True,
        fontName='Helvetica-Bold',
        alignment=0
    )
    
    bold_red_style = ParagraphStyle(
        name='BoldRedStyle',
        fontSize=12,
        textColor=red,
        fontName='Helvetica-Bold',
        alignment=0
    )
    
    elements.append(Paragraph(f"Product Name: {game_name.upper()}", title_style))
    elements.append(Spacer(1, 3))

    drawing = Drawing(400, 2)
    drawing.add(Line(0, 0, 450, 0, strokeColor='black', strokeWidth=2))
    elements.append(drawing)
    elements.append(Spacer(1, 12))
    
    elements.append(Paragraph(f"File Size: {game_size}", title_style))
    elements.append(Spacer(1, 3))

    drawing = Drawing(400, 2)
    drawing.add(Line(0, 0, 450, 0, strokeColor='black', strokeWidth=2))
    elements.append(drawing)
    elements.append(Spacer(1, 12))
    
    elements.append(Paragraph(
        "Note: Password is written on guide given inside parcel", 
        bold_red_style
    ))
    elements.append(Spacer(1, 12))
    
    drawing = Drawing(400, 2)
    drawing.add(Line(0, 0, 450, 0, strokeColor='black', strokeWidth=2))
    elements.append(drawing)
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Links:", styles['Heading2']))
    elements.append(Spacer(1, 8))
    
    for link in game_links.splitlines():
        if link:
            link_text = f'<a href="{link}">{link}</a>'
            elements.append(Paragraph(link_text, link_style))
            elements.append(Spacer(1, 12))


    

    elements.append(Paragraph(
        "NOTE: IF LINKS ARE EXPIRED OR NOT WORKING CONTACT TO SELLER", 
        bold_red_style
    ))
    elements.append(Spacer(1, 12))
    
    drawing = Drawing(400, 2)
    drawing.add(Line(0, 0, 450, 0, strokeColor='black', strokeWidth=2))
    elements.append(drawing)
    elements.append(Spacer(1, 12))


    elements.append(Paragraph(
        "Tutorial Video Link:", 
        styles['Heading2']
    ))
    elements.append(Spacer(1, 6))
    tutorial_video_link = "https://drive.google.com/file/d/1aIdIViznlep6ZORwhR631nf0KMoiyPMT/view?usp=drive_link"
    elements.append(Paragraph(
        tutorial_video_link, 
        link_style
    ))
    elements.append(Spacer(1, 12))
    
    drawing = Drawing(400, 2)
    drawing.add(Line(0, 0, 450, 0, strokeColor='black', strokeWidth=2))
    elements.append(drawing)
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(
        "Guide File Link", 
        styles['Heading2']
    ))
    elements.append(Spacer(1, 6))
    guide_file_link = "https://drive.google.com/file/d/1pxtpnNABQWr9izLygu6uznqJlrWkl0_r/view?usp=drive_link"
    elements.append(Paragraph(
        guide_file_link, 
        link_style
    ))
    elements.append(Spacer(1, 12))

    doc.build(elements, onFirstPage=add_page_border, onLaterPages=add_page_border)
    buffer.seek(0)
    return buffer

def uploadgamefiles(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            game_name = form.cleaned_data['game_name']
            game_size = form.cleaned_data['game_size']
            game_links = form.cleaned_data['game_links']
            
            pdf_buffer = generate_pdf(game_name, game_size, game_links)
            
            temp_dir = tempfile.gettempdir()
            pdf_path = os.path.join(temp_dir, f"{game_name.upper()}.pdf")
            with open(pdf_path, 'wb') as f:
                f.write(pdf_buffer.read())
            
            if 'upload_pdf' in request.POST:
                with open(pdf_path, 'rb') as f:
                    response = HttpResponse(f.read(), content_type='application/pdf')
                    response['Content-Disposition'] = f'attachment; filename="{game_name}.pdf"'
                    messages.success(request, 'PDF generated successfully!')
                return response

            elif 'upload_drive' in request.POST:
                file_link = upload_file_to_drive(pdf_path)
                messages.success(request, f'File uploaded to Google Drive with Link: {file_link}')
                
                # Save the link and name in the session
                request.session['uploaded_file_link'] = file_link
                request.session['uploaded_file_name'] = game_name
                
                # Return the response to render the new button
                return render(request, 'uploadgamefiles.html', {
                    'form': form,
                    'generate_qrcode_button': True,
                    'file_link': file_link,
                    'file_name': game_name
                })

            os.remove(pdf_path)
    else:
        form = GameForm()
    
    return render(request, 'uploadgamefiles.html', {'form': form})
