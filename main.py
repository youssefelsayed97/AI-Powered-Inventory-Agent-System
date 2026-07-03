from flask import Flask, request, redirect, render_template
from werkzeug.utils import secure_filename
import os
import uuid
from dotenv import load_dotenv
from ai.qdrant import create_collection, is_collection_empty, COLLECTION_NAME, reload_data_to_qdrant
import ai.pipeline
from tools.stock_tools import add_stock, get_all_stock

load_dotenv()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__, static_folder="static")

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "static/UPLOADS")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

create_collection(COLLECTION_NAME)

if is_collection_empty(COLLECTION_NAME):
    reload_data_to_qdrant()


@app.route('/')
def home():
    return render_template("Home.html")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def js_alert(message, redirect_location):
    return f'''
                <script>
                            alert("{message}");
                            window.location = "/{redirect_location}";
                </script>
            '''


@app.route('/Add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':

        for i in request.form:
            if str(request.form[i]).strip() == '':
                return js_alert('please fill all fields', 'Add')
                # return '''
                #     <script>
                #         alert("Please fill all fields.");
                #         window.location = '/Add';
                #     </script>
                # '''

        new_data = {i: request.form[i] for i in request.form}

        try:
            new_data['Code'] = int(new_data['Code'])
            new_data["LowPrice"] = float(new_data["LowPrice"])
            new_data["HighPrice"] = float(new_data["HighPrice"])
        except ValueError:
            return js_alert("Invalid number", "Add")
            # return """
            #         <script>
            #             alert("Invalid number.");
            #             window.location='/Add';
            #         </script>
            # """

        if 'file' not in request.files:
            # return "No file part"
            return js_alert("No file part", "Add")

        file = request.files['file']

        if file.filename == '':
            # return "No selected file"
            return js_alert("No selected file", "Add")
        if not allowed_file(file.filename):
            # return "Invalid file type"
            return js_alert("Invalid file type", "Add")

        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1].lower()

        renamed_image = f"{uuid.uuid4().hex}.{ext}"

        save_path = os.path.join(app.config['UPLOAD_FOLDER'], renamed_image)
        file.save(save_path)

        new_data["Image"] = renamed_image

        result = add_stock(new_data)

        if not result['success']:
            os.remove(save_path)


        return js_alert(f"{result['message']}", "Add")

            # return f'''
            #     <script>
            #         alert("{result["message"]}");
            #         window.location = '/Add';
            #     </script>
            # '''

        # return redirect("/")

    # return render_template("Home.html")



@app.route("/Stock")
def stock():
    stocks = get_all_stock()
    return render_template("stock.html", stocks=stocks)


@app.route("/AI", methods=["POST"])
def ai_action():
    query = request.form["query"]

    result = ai.pipeline.ai_action_decide(query)
    print("-----------------------------")
    print(result)
    print("-----------------------------")
    if result['tool']:
        if result['tool'] == "search_stock" and result['success']:
            return render_template("stock.html", stocks=result['result'])
        elif result['tool'] == "delete_stock":
            if result['success']:
                return js_alert(f"{result['message'], result['deleted_item']}", "Stock")
                # return f"""
                #             <script>
                #                 alert("{result['message'], result['deleted_item']}");
                #                 window.location = '/Stock';
                #             </script>
                #         """
            else:
                return js_alert(f"{result['message']}", "Stock")
                # return f"""
                #             <script>
                #                 alert("{result['message']}");
                #                 window.location = '/Stock';
                #             </script>
                #         """
    else:
        return js_alert(f"{result['message']}", "Stock")
        # return f"""
        #              <script>
        #                     alert("{result['message']}");
        #                     window.location = '/Stock';
        #                 </script>
        #             """


    # if result['tool'] == "delete_stock" and result['args']['Code']:
    #     print("ai action delete")
    #
    # try:
    #     return render_template("stock.html", stocks=result['result'])
    # except:



if __name__ == "__main__":
    app.run(debug=True)
