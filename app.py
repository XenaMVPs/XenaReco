from flask import Flask, request, render_template
import requests
import whois
import socket
from bs4 import BeautifulSoup

app = Flask(__name__)

# Función para obtener WHOIS del dominio
def get_whois(domain):
    try:
        data = whois.whois(domain)
        return str(data)
    except:
        return "No se pudo obtener WHOIS."

# Función para obtener IP de un dominio
def get_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except:
        return "No se pudo resolver la IP."

# Función para obtener encabezados HTTP
def get_headers(domain):
    try:
        response = requests.get(f"http://{domain}", timeout=5)
        headers = dict(response.headers)
        return headers
    except:
        return "No se pudieron obtener los headers."

# Función para hacer scraping más completo (Título, meta description, keywords, autor)
def get_meta(domain):
    try:
        response = requests.get(f"http://{domain}", timeout=5)
        response.encoding = response.apparent_encoding  # Corregir problemas de codificación
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string if soup.title else "No Title"
        meta_desc = soup.find("meta", attrs={"name": "description"})
        meta_desc = meta_desc["content"] if meta_desc else "No Meta Description"

        keywords = soup.find("meta", attrs={"name": "keywords"})
        keywords = keywords["content"] if keywords else "No Keywords Found"

        author = soup.find("meta", attrs={"name": "author"})
        author = author["content"] if author else "No Author Found"

        return {
            "title": title,
            "meta_desc": meta_desc,
            "keywords": keywords,
            "author": author
        }
    except Exception as e:
        return {"title": "Error", "meta_desc": "No se pudo obtener la información", "keywords": "", "author": ""}

# Ruta principal
@app.route('/')
def index():
    return render_template("index.html")

# Ruta para analizar un dominio
@app.route('/recon', methods=['POST'])
def recon():
    domain = request.form['domain']
    results = {
        "whois": get_whois(domain),
        "ip": get_ip(domain),
        "headers": get_headers(domain),
        "meta": get_meta(domain)
    }
    return render_template("result.html", domain=domain, results=results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
