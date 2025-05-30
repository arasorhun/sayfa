from flask import Flask, render_template, request, redirect, session, url_for
import json
import os

app = Flask(__name__)
app.secret_key = 'gizli_kod'

def veri_yukle(dosya):
    if not os.path.exists(dosya):
        with open(dosya, 'w', encoding='utf-8') as f:
            json.dump([], f)
    with open(dosya, 'r', encoding='utf-8') as f:
        return json.load(f)

def veri_kaydet(dosya, veri):
    with open(dosya, 'w', encoding='utf-8') as f:
        json.dump(veri, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    yazilar = veri_yukle('veri/yazilar.json')
    sol = veri_yukle('veri/sol.json')
    sag = veri_yukle('veri/sag.json')
    kategoriler = veri_yukle('veri/kategoriler.json')
    return render_template('index.html', yazilar=yazilar, sol=sol, sag=sag, kategoriler=kategoriler)

@app.route('/kategori/<isim>')
def kategori_yazilari(isim):
    yazilar = veri_yukle('veri/yazilar.json')
    yazilar = [y for y in yazilar if y.get("kategori") == isim]
    sol = veri_yukle('veri/sol.json')
    sag = veri_yukle('veri/sag.json')
    kategoriler = veri_yukle('veri/kategoriler.json')
    return render_template('index.html', yazilar=yazilar, sol=sol, sag=sag, kategoriler=kategoriler)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['sifre'] == '1234':
            session['admin'] = True
            return redirect(url_for('admin'))
    return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('admin'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'yeni_yazi' in request.form:
            yazilar = veri_yukle('veri/yazilar.json')
            yeni_yazi = {
                'baslik': request.form['baslik'],
                'icerik': request.form['icerik'],
                'kategori': request.form['kategori']
            }
            ozet = request.form.get('ozet')
            if ozet:
                yeni_yazi['ozet'] = ozet
            yazilar.append(yeni_yazi)
            veri_kaydet('veri/yazilar.json', yazilar)

        elif 'sil' in request.form:
            yazilar = veri_yukle('veri/yazilar.json')
            index = int(request.form['yazi_index'])
            if 0 <= index < len(yazilar):
                yazilar.pop(index)
                veri_kaydet('veri/yazilar.json', yazilar)

        elif 'guncelle' in request.form:
            yazilar = veri_yukle('veri/yazilar.json')
            index = int(request.form['yazi_index'])
            if 0 <= index < len(yazilar):
                guncel = {
                    'baslik': request.form['baslik'],
                    'icerik': request.form['icerik'],
                    'kategori': request.form['kategori']
                }
                ozet = request.form.get('ozet')
                if ozet:
                    guncel['ozet'] = ozet
                yazilar[index] = guncel
                veri_kaydet('veri/yazilar.json', yazilar)


        elif 'sol' in request.form:
            veri_kaydet('veri/sol.json', request.form['sol'].split('\n'))

        elif 'sag' in request.form:
            veri_kaydet('veri/sag.json', request.form['sag'].split('\n'))

        elif 'kategori' in request.form:
            veri_kaydet('veri/kategoriler.json', request.form['kategori'].split('\n'))

        return redirect(url_for('admin'))

    yazilar = veri_yukle('veri/yazilar.json')
    sol = "\n".join(veri_yukle('veri/sol.json'))
    sag = "\n".join(veri_yukle('veri/sag.json'))
    kategoriler = "\n".join(veri_yukle('veri/kategoriler.json'))
    return render_template('admin.html', yazilar=yazilar, sol=sol, sag=sag, kategoriler=kategoriler)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
