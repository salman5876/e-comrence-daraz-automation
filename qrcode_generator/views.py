# qrcode_generator/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import QRCodeForm
from qrcodes.models import Game
import qrcode
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import base64

def create_qr_code(link, file_name):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    qr_img = qr.make_image(fill='black', back_color='white')

    font_path = "arial.ttf"  # Update this path to your desired font file
    font = ImageFont.truetype(font_path, 54)

    img_width, img_height = qr_img.size
    new_height = img_height + 70
    result_img = Image.new('RGB', (img_width, new_height), 'white')
    result_img.paste(qr_img, (0, 0))

    draw = ImageDraw.Draw(result_img)
    line_y = img_height - 15
    draw.line((40, line_y, img_width - 40, line_y), fill='black', width=8)

    text_bbox = draw.textbbox((0, 0), file_name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_position = ((img_width - text_width) // 2, img_height + 1)
    draw.text(text_position, file_name, fill='black', font=font)

    border_width = 10
    margin_width = 10
    rounded_radius = 20
    bordered_img_width = img_width + 2 * (border_width + margin_width)
    bordered_img_height = new_height + 2 * (border_width + margin_width)
    
    bordered_img = Image.new('RGB', (bordered_img_width, bordered_img_height), 'white')
    border_draw = ImageDraw.Draw(bordered_img)
    border_draw.rounded_rectangle(
        [(margin_width, margin_width), (bordered_img_width - margin_width, bordered_img_height - margin_width)],
        radius=rounded_radius,
        outline='black',
        width=border_width
    )
    bordered_img.paste(result_img, (border_width + margin_width, border_width + margin_width))

    return bordered_img

def generate_qr(request):
    qr_image_url = None
    file_name = None
    qr_saved_success = request.session.pop('qr_saved_success', False)

    if request.method == 'POST':
        form = QRCodeForm(request.POST)
        if form.is_valid():
            file_link = form.cleaned_data['file_link']
            file_name = form.cleaned_data['file_name']
            qr_image = create_qr_code(file_link, file_name)

            resized_qr_image = qr_image.resize((186, 230))

            buffer = BytesIO()
            resized_qr_image.save(buffer, format="PNG")
            buffer.seek(0)

            qr_image_base64 = base64.b64encode(buffer.getvalue()).decode()
            qr_image_url = f"data:image/png;base64,{qr_image_base64}"

            request.session['qr_image_data'] = qr_image_base64
            request.session['qr_image_name'] = file_name

    else:
        form = QRCodeForm(initial={
            'file_link': request.POST.get('file_link', ''),
            'file_name': request.POST.get('file_name', '')
        })

    return render(request, 'qrcode_generator/generate_qr.html', {
        'form': form,
        'qr_image_url': qr_image_url,
        'file_name': file_name,
        'qr_saved_success': qr_saved_success,
    })


def download_qr(request):
    image_data_base64 = request.session.get('qr_image_data')
    file_name = request.session.get('qr_image_name')

    if not image_data_base64 or not file_name:
        return redirect('qrcode_generator:generate_qr')

    image_data = base64.b64decode(image_data_base64)
    response = HttpResponse(image_data, content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename="{file_name}.png"'
    return response

# qrcode_generator/views.py

def save_qr_to_db(request):
    if request.method == 'POST':
        file_name = request.session.get('qr_image_name')
        image_data_base64 = request.session.get('qr_image_data')

        if not image_data_base64 or not file_name:
            return redirect('qrcode_generator:generate_qr')

        image_data = base64.b64decode(image_data_base64)
        image = BytesIO(image_data)
        image.seek(0)

        game = Game(name=file_name)
        game.image.save(f"{file_name}.png", image)
        game.save()

        request.session['qr_saved_success'] = True
        return redirect('qrcode_generator:generate_qr')

    return redirect('qrcode_generator:generate_qr')