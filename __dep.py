# NOTE: EMA route deprecated
# @app.route("/EMA", methods=["GET", "POST"])
# def ema():
#     if request.method == "POST":
#         from utils.base.scp_ema_parser import EMA_Parser

#         # -- Read in and save JSON file
#         file = request.files["file"]
#         safe_name = secure_filename(file.filename)

#         output_dir = datetime.now().strftime("%b_%d_%Y_%H_%M_%S")
#         output_path = os.path.join(
#             app.root_path, app.config["UPLOAD_FOLDER"], output_dir
#         )

#         if not os.path.exists(output_path):
#             pathlib.Path(output_path).mkdir(exist_ok=True, parents=True)

#         file.save(os.path.join(output_path, safe_name))

#         # -- Instantiate EMA_Parser object
#         try:
#             parser = EMA_Parser(filename=safe_name, output_path=output_path)
#             parser.big_dogs_only()

#         except Exception as e:
#             message = f"Error @ EMA Parser\n\n{e}"
#             post_webhook(message=message)

#             return redirect(url_for("index"))

#         # -- Download resulting files
#         target = os.path.join(output_path, "SCP_EMA_Responses.tar.gz")
#         return download(target)

#     return render_template("utils/ema.html")
