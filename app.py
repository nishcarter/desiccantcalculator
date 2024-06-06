from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        U = float(request.form['U'])
        D = float(request.form['D'])
        WVTR_in = request.form.get('WVTR_in')
        WVTR_m2 = request.form.get('WVTR_m2')
        L_in = request.form.get('L_in')
        W_in = request.form.get('W_in')
        L_mm = request.form.get('L_mm')
        W_mm = request.form.get('W_mm')

        if WVTR_in:
            WVTR = float(WVTR_in)
        elif WVTR_m2:
            WVTR = float(WVTR_m2) / 15.50031
        else:
            return jsonify({"error": "Please enter a value for WVTR."}), 400

        if not L_in:
            L_in = float(L_mm) / 25.4
        else:
            L_in = float(L_in)

        if not W_in:
            W_in = float(W_mm) / 25.4
        else:
            W_in = float(W_in)

        A = (L_in * W_in) * 2

        calculated_shelf_life = (U * D) / (0.304 * WVTR * A)
        result_color = "green" if calculated_shelf_life > 24 else "red"

        return jsonify({
            "shelf_life": f"{calculated_shelf_life:.2f} months",
            "color": result_color
        })

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
