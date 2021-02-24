import flask, random
from flask import render_template, request
import logic

app = flask.Flask(__name__, template_folder='templates')
app.config["DEBUG"] = True


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/', methods=['POST'])
def home_post():
    try:
        data_1 = str(request.form['fd'])
        data_2 = str(request.form['ld'])
        data_1_validity, data_2_validity = logic.data_validity(data_1, data_2)
        if not (data_1_validity and data_2_validity):
            return render_template(
                'home_post_error.html',
                value="********")
        final_data_1, final_data_2 = logic.spacing_controll(data_1, data_2)
        result = logic.friendship_calculation(final_data_1, final_data_2)
        logic.update_img_locally(final_data_1, final_data_2, result)
        direct_url = logic.upload_imgbb_server()
        return render_template('home_post.html', value=direct_url)
    except:
        try:
            result = logic.checking_whether_report_bug_clicked()

        except:
            return render_template(
                'home_post_error.html',
                value="********")


@app.route('/tnc')
def tnc():
    return render_template('tnc.html')


@app.route('/reported')
def submitted_report_bug_form():
    return render_template('successfully_reported.html')


@app.route('/500')
def internal_server_error():
    return render_template('internal_server_error.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=random.randint(2000, 9000))
