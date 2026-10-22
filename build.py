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
open(os.path.join(OUT, '.nojekyll'), 'w').close()
print('OK', OUT)
