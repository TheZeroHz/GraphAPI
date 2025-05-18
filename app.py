from flask import Flask, request, send_file, jsonify
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

app = Flask(__name__)

def draw_gauge(value: float, color: str):
    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw={'projection': 'polar'})
    ax.set_theta_direction(-1)
    ax.set_theta_offset(np.pi / 2.0)
    ax.set_ylim(0, 100)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines.clear()
    ax.grid(False)

    # Background arc
    full_circle = np.linspace(0, 2 * np.pi, 100)
    ax.plot(full_circle, np.full_like(full_circle, 100), lw=20, color='lightgray', alpha=0.5)

    # Value arc
    end_angle = 2 * np.pi * (value / 100.0)
    ax.plot(np.linspace(0, end_angle, 100), np.full(100, 100), lw=20, color=color)

    # Center text
    ax.text(0, 0, f"{int(value)}%", fontsize=20, ha='center', va='center', color=color)

    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1, transparent=True)
    buf.seek(0)
    plt.close(fig)
    return buf

@app.route('/gauge', methods=['GET'])
def gauge():
    try:
        value = float(request.args.get("value", 0))
        color = request.args.get("color", "blue")
        value = max(0, min(100, value))  # Clamp between 0–100

        image = draw_gauge(value, color)
        return send_file(image, mimetype='image/png')
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
