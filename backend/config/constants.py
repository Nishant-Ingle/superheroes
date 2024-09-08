import os
curr_dir_abs_path = os.path.abspath(os.path.dirname(__file__))
props_file_abs_path = os.path.join(curr_dir_abs_path, "..", "resources", "app.properties")
db_file_abs_path = os.path.join(curr_dir_abs_path, "..", "..", "db", "superhero_app.sqlite3")
