from flask import Flask, request, redirect, render_template, url_for
from datetime import datetime
import requests, json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/asmaulhusna")
def asma():
    file = open("data/asmaul-husna.json", "rb").read()

    isi = []
    for hasil in json.loads(file):
        isi.append(hasil)

    return render_template("asma.html",jeson = isi)

@app.route("/ayatkursi")
def ayatkursi():
    url = "https://islamic-api-zhirrr.vercel.app/api/ayatkursi"
    req = requests.get(url)
    jeson = json.loads(req.text)

    tafsir = jeson["data"]["tafsir"]
    arab = jeson["data"]["arabic"]
    latin = jeson["data"]["latin"]

    return render_template("ayatkursi.html",tafsir = tafsir, arab = arab, latin = latin)

@app.route("/carinabi",methods=["POST", "GET"])
def cari_nabi():
    nnabi = request.args.get("namanabi")
    if not nnabi:
        return render_template("carinabi.html")

    return redirect(url_for("sukses",data = nnabi))

@app.route("/kisahnabi/<data>") #must add variabel
def sukses(data):
    url = f"https://kisahnabi-api-zhirrr.vercel.app/api/searchnabi?q={data}"
    req = requests.get(url)
    jeson = json.loads(req.text)

    nama = jeson["nabi"]["nama"]
    lahir = jeson["nabi"]["lahir"]
    umur = jeson["nabi"]["umur"]
    ttl = jeson["nabi"]["tempat"]
    gambar = jeson["nabi"]["image"]
    kisah = jeson["nabi"]["kisah"]

    return render_template("nabi.html",nama = nama,lahir = lahir,umur = umur,ttl = ttl,gambar = gambar,kisah = kisah)

@app.route("/niat")
def niats():
    url = "https://islamic-api-zhirrr.vercel.app/api/niatshalat"
    req = requests.get(url)
    jeson = json.loads(req.text)

    isi = []
    for hasil in jeson:
        isi.append(hasil)

    return render_template("niat.html",jeson = isi)

@app.route("/cari")
def quran():
    file = open("data/quran/surat.json", "rb").read()

    isi = []
    for hasil in json.loads(file):
        isi.append(hasil)

    return render_template("qurancari.html",jeson = isi)

@app.route("/quran/<id>")
def quranA(id):
    file = open(f"data/quran/{id}.json", "rb").read()

    isi = []
    for hasil in json.loads(file):
        isi.append(hasil)

    return render_template("quran.html",jeson = isi)

@app.route("/cari/jadsho",methods=["POST", "GET"])
def cari_jadwal():
    kot = request.args.get("kota")
    if not kot:
        return render_template("cari_kota.html")

    return redirect(url_for("kota_tujuan",data = kot))

@app.route("/jadsho/<data>")
def kota_tujuan(data):
    waktu = datetime.today().strftime("%Y-%m-%d")
    url = f"https://api.pray.zone/v2/times/day.json?city={data}&date={waktu}"
    req = requests.get(url)
    jeson = json.loads(req.text)

    for hasil in jeson["results"]["datetime"]:
        dzuhur = hasil["times"]["Dhuhr"]
        ashar = hasil["times"]["Asr"]
        maghrib = hasil["times"]["Maghrib"]
        isya = hasil["times"]["Isha"]
        subuh = hasil["times"]["Imsak"]

    return render_template("jadwal.html",kota = data,Dzuhur = dzuhur,Ashar = ashar,Maghrib = maghrib,Isya = isya,Subuh = subuh)

@app.errorhandler(json.decoder.JSONDecodeError)
def error(e):
    return render_template("error.html")

@app.errorhandler(requests.exceptions.ConnectionError)
def koneksi(e):
    return "Koneksi error mohon periksa koneksi anda :)"

if __name__ == "__main__":
    app.run(debug = True)
