# TODO:
'''
    - Remove/edit entries
    - back to index page
'''

from flask import Flask, session, render_template, request, g
from db_handler import DatabaseHandler
from config_handler import ConfigHandler

app = Flask(__name__)
db_hand = DatabaseHandler()
config_hand = ConfigHandler()

@app.route("/", methods=['get', 'post'])
def index():
    '''Main page'''
    table_select = request.form.get('table_select')
    if table_select and table_select not in ['Flashcards', 'Guess game']:
        db_hand.set_current_table(table_select)
        config_hand.set_last_opened_table(table_select)

    cats = db_hand.get_all_categories()
    tables = db_hand.get_tables()
    last_table = config_hand.get_last_opened_table()
    return render_template("index.html", categories=cats, tables=tables, last_table=last_table)

@app.route("/add_data")
def add_data():
    '''TODO: Under development'''
    return render_template('add_data.html')

@app.route("/play_all")
def play_all():
    text_dict = db_hand.get_all_texts()
    return render_template('flashcards.html', data=text_dict)


@app.route("/play_category", methods=['post'])
def play_category():

    selected_categories = [v for v in request.form if v != 'table_select']
    if not selected_categories:     # Empty selection
        return index()
    
    text_dict = db_hand.get_categorcal_texts(selected_categories)
    game_type = request.form.get('table_select')
    
    if game_type == 'Guess game':
        return render_template('guess_game.html', data=text_dict)
    elif game_type == 'Flashcards':
        return render_template('flashcards.html', data=text_dict)
    else:
        return index()


@app.route('/add_element', methods=['post'])
def add_element():
    db_hand.add_data({request.form['text1']: request.form['text2']})
    print('Data added to database')
    return render_template("add_data.html")

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:   
        db.close()

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=1900, debug=True)
