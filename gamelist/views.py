# gamelist/views.py

from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from PIL import Image, ImageDraw, ImageFont
import os

def draw_table(image, draw, games, rows, cols, canvas_size, margins, border_width, font):
    inner_width = canvas_size[0] - margins['left'] - margins['right']
    inner_height = canvas_size[1] - margins['top'] - margins['bottom']
    cell_width = inner_width / cols
    cell_height = inner_height / rows

    draw.rectangle(
        [margins['left'], margins['top'], canvas_size[0] - margins['right'], canvas_size[1] - margins['bottom']],
        outline="black",
        width=border_width
    )

    for row in range(rows):
        for col in range(cols):
            x0 = margins['left'] + col * cell_width
            y0 = margins['top'] + row * cell_height
            x1 = x0 + cell_width
            y1 = y0 + cell_height
            draw.rectangle([x0, y0, x1, y1], outline="black", width=1)

            game_index = row * cols + col
            if game_index < len(games):
                text = games[game_index]
                text_bbox = draw.textbbox((0, 0), text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                text_x = x0 + (cell_width - text_width) / 2
                text_y = y0 + (cell_height - text_height) / 2
                draw.text((text_x, text_y), text, fill="black", font=font)

def gamelist(request):
    if request.method == 'POST' and request.FILES['textFile']:
        text_file = request.FILES['textFile']
        canvas_width = int(request.POST['canvasWidth'])
        canvas_height = int(request.POST['canvasHeight'])
        rows = int(request.POST['numRows'])
        cols = int(request.POST['numCols'])
        margin_top = int(request.POST['marginTop'])
        margin_left = int(request.POST['marginLeft'])
        margin_right = int(request.POST['marginRight'])
        margin_bottom = int(request.POST['marginBottom'])
        border_width = int(request.POST['borderWidth'])
        font_size = int(request.POST['fontSize'])

        fs = FileSystemStorage()
        filename = fs.save(text_file.name, text_file)
        file_path = fs.path(filename)

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            games = [line.strip() for line in file.readlines()]

        try:
            font = ImageFont.truetype(r"C:\Users\mugha\OneDrive\Desktop\Daraz Code\Fonts\Roboto\Roboto-Black.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        total_games = len(games)
        rows_per_canvas = rows
        cols_per_canvas = cols
        num_canvases = (total_games + (rows_per_canvas * cols_per_canvas) - 1) // (rows_per_canvas * cols_per_canvas)

        generated_images = []
        for canvas_index in range(num_canvases):
            canvas_size = (canvas_width, canvas_height)
            image = Image.new('RGB', canvas_size, 'white')
            draw = ImageDraw.Draw(image)

            start_game_index = canvas_index * rows_per_canvas * cols_per_canvas
            end_game_index = min((canvas_index + 1) * rows_per_canvas * cols_per_canvas, total_games)
            games_for_canvas = games[start_game_index:end_game_index]

            draw_table(image, draw, games_for_canvas, rows_per_canvas, cols_per_canvas, canvas_size, 
                       {'top': margin_top, 'left': margin_left, 'right': margin_right, 'bottom': margin_bottom}, 
                       border_width, font)

            image_filename = f"canvas_{canvas_index + 1}.png"
            image_path = os.path.join(fs.location, image_filename)
            image.save(image_path)
            generated_images.append(fs.url(image_filename))

        return render(request, 'result.html', {'images': generated_images})

    return render(request, 'gamelist.html')
