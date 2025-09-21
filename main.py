from flask import Flask, render_template, send_from_directory
import os
import requests

# Serve templates from repo root (where your .html files live)
app = Flask(__name__, template_folder='.', static_folder='static')

# --- Weather helper (local dev only) ---
def get_weather(city='Sudbury'):
    """Return (temp_c, description) or (None, None) on failure."""
    api_key = os.getenv('OPENWEATHER_API_KEY')  # don't hardcode secrets
    if not api_key:
        return None, None
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        resp = requests.get(url, params={"q": city, "appid": api_key, "units": "metric"}, timeout=6)
        resp.raise_for_status()
        data = resp.json()
        temp_c = round(data['main']['temp'], 1)
        desc = data['weather'][0]['description']
        return temp_c, desc
    except Exception:
        return None, None

# ---- Routes for both "/" and "/index.html" ----
@app.route("/")
@app.route("/index.html")
def index():
    temp_c, temp_description = get_weather('Sudbury')
    return render_template("index.html", temp_c=temp_c, temp_description=temp_description)

# ---- Match your file-based links (project.html, edu.html, etc.) ----
@app.route("/project.html")
def project_html():
    return render_template("project.html")

@app.route("/edu.html")
def edu_html():
    return render_template("edu.html")

@app.route("/cert.html")
def cert_html():
    return render_template("cert.html")

@app.route("/exp.html")
def exp_html():
    return render_template("exp.html")

@app.route("/skills.html")
def skills_html():
    return render_template("skills.html")

@app.route("/publish.html")
def publish_html():
    return render_template("publish.html")

@app.route("/voul.html")
def voul_html():
    return render_template("voul.html")

@app.route("/bmi.html")
def bmi_html():
    # If you create a BMI page, this will serve it
    return render_template("bmi.html")

# ---- Back-compat: also keep your old no-extension routes working ----
@app.route("/project")
def project():
    return render_template("project.html")

@app.route("/edu")
def edu():
    return render_template("edu.html")

@app.route("/cert")
def cert():
    return render_template("cert.html")

@app.route("/exp")
def exp():
    return render_template("exp.html")

@app.route("/skills")
def skills():
    return render_template("skills.html")

@app.route("/publish")
def publish():
    return render_template("publish.html")

@app.route("/voul")
def voul():
    return render_template("voul.html")

@app.route("/bmi")
def bmi():
    return render_template("bmi.html")

# Optional: serve any other top-level HTML by filename safely
@app.route("/<path:filename>")
def catch_all_html(filename):
    # Serve other .html files in the root if requested directly
    if filename.endswith(".html") and os.path.exists(filename):
        return render_template(filename)
    # Let Flask handle 404s for unknown paths / assets
    return send_from_directory('.', filename)

if __name__ == "__main__":
    # Set your key once locally:  export OPENWEATHER_API_KEY=xxxxx
    app.run(host="0.0.0.0", port=8080, debug=True)
