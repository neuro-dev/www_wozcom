from PIL import Image

def remove_metadata(input_path, output_path):
    # Открываем изображение
    img = Image.open(input_path)
    
    # Создаем новую копию без метаданных (без info)
    # JPEG сохраняет метаданные только если передать exif=...
    img.save(output_path, "JPEG", quality=95)
    print(f"Метаданные удалены. Файл сохранен: {output_path}")

# Пример использования
remove_metadata("avatar.jpg", "avatar_no_meta.jpg")
