"""Сборка сайта ПОGREB WINE: исходники в src/, фото и видео в media/, результат в dist/.
Запуск: python build.py"""
import os, shutil, subprocess, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get('OUT', os.path.join(ROOT, 'dist'))
if os.environ.get('CLEAN', '1') == '1' and os.path.isdir(OUT) and OUT.endswith('dist'):
    shutil.rmtree(OUT)
os.makedirs(OUT, exist_ok=True)
env = dict(os.environ, OUT=OUT)
subprocess.run([sys.executable, os.path.join(ROOT, 'src', 'build_pages.py')], check=True, env=env)
src = os.path.join(ROOT, 'src')
with open(os.path.join(OUT, 'style.css'), 'w', encoding='utf-8') as f:
    for name in ('style.css', 'extra.css'):
        f.write(open(os.path.join(src, name), encoding='utf-8').read() + '\n')
for js in ('app.js', 'konstruktor.js'):
    shutil.copy(os.path.join(src, js), os.path.join(OUT, js))
media_out = os.path.join(OUT, 'media')
if os.path.abspath(media_out) != os.path.abspath(os.path.join(ROOT, 'media')):
    shutil.copytree(os.path.join(ROOT, 'media'), media_out, dirs_exist_ok=True)

# Фото и видео, которые прислали через бота: HEIC -> JPG, крупные фото уменьшаем,
# видео без превью получают превью, тяжёлые видео сжимаем. Исходники в media/ не трогаем.
def process_media(folder):
    try:
        from PIL import Image, ImageOps
    except ImportError:
        Image = None
    try:
        import pillow_heif
        pillow_heif.register_heif_opener()
    except Exception:
        pass
    have_ffmpeg = shutil.which('ffmpeg') is not None
    for name in sorted(os.listdir(folder)):
        path = os.path.join(folder, name)
        base, ext = os.path.splitext(name)
        ext = ext.lower()
        if not name.startswith('tg-'):
            continue
        try:
            if Image and ext in ('.heic', '.heif', '.jpg', '.jpeg', '.png', '.webp'):
                im = ImageOps.exif_transpose(Image.open(path)).convert('RGB')
                if max(im.size) > 2000:
                    im.thumbnail((2000, 2000))
                target = os.path.join(folder, base + '.jpg')
                im.save(target, 'JPEG', quality=84, optimize=True, progressive=True)
                if target != path:
                    os.remove(path)
            elif ext in ('.mp4', '.mov', '.m4v') and have_ffmpeg:
                target = os.path.join(folder, base + '.mp4')
                if os.path.getsize(path) > 6 * 1024 * 1024 or ext != '.mp4':
                    tmp = os.path.join(folder, base + '.tmp.mp4')
                    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', path, '-vf', "scale='min(1080,iw)':-2", '-c:v', 'libx264', '-crf', '27', '-preset', 'veryfast', '-an', '-movflags', '+faststart', tmp], check=True)
                    os.remove(path)
                    os.replace(tmp, target)
                poster = os.path.join(folder, base + '-poster.jpg')
                if not os.path.exists(poster):
                    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '1', '-i', target, '-frames:v', '1', '-q:v', '4', poster], check=True)
        except Exception as e:
            print('media: не обработал', name, e)

if os.path.abspath(media_out) != os.path.abspath(os.path.join(ROOT, "media")):
    process_media(media_out)
open(os.path.join(OUT, '.nojekyll'), 'w').close()
print('OK', OUT)
