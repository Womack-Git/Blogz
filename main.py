from flask import Flask, render_template, request
import sqlite3
app = Flask('app')

#Andrew Womack // Build-a-Blog

conn = sqlite3.connect('database.db')
c = conn.cursor()

#database creation code
#c.execute("""CREATE TABLE posts (
#  pid INTEGER PRIMARY KEY AUTOINCREMENT,
#  title text NOT NULL,
#  content text NOT NULL
#)""")

#c.execute("INSERT INTO posts (title, content) VALUES ('Test Title','This is test content')")
#print(c.fetchall())

def sql(sql_command, values):
  conn = sqlite3.connect('database.db', check_same_thread=False)
  c = conn.cursor()
  query = c.execute(sql_command, values).fetchall()
  conn.commit()
  conn.close()
  return query

def sql_two(sql_command):
  conn = sqlite3.connect('database.db', check_same_thread=False)
  c = conn.cursor()
  query = c.execute(sql_command).fetchall()
  conn.commit()
  conn.close()
  return query

#Second table creation code


@app.route('/')
def initialize_page():
  query = sql_two('SELECT * FROM posts')
  id = request.args.get('pid')
  if id != None:
    title = sql('SELECT title FROM posts WHERE pid=?',(id,))
    content = sql('SELECT content FROM posts WHERE pid=?',(id,))
    #guinness world record book of dumbest solutions to a problem ever because I haven't done sqlite in 8 months+
    format_string_title = str(title)
    format_string_title = format_string_title.replace("[('", "")
    format_string_title = format_string_title.replace("',)]", "")
    format_string_content = str(content)
    format_string_content = format_string_content.replace("[('", "")
    format_string_content = format_string_content.replace("',)]", "")
    return render_template('individual.html', title = format_string_title, content = format_string_content)
  return render_template('home.html', query = query)


@app.route('/postpage')
def post_link():
  return render_template("postpage.html")

@app.route('/postpage', methods=["POST"])
def post_add():
  error = "Blog post must have title and content"
  title = str(request.form.get("Title"))
  content = str(request.form.get("Content"))
  if title != "" and content != "":
    sql('INSERT INTO posts (title, content) VALUES (?,?)', (title, content))
    return render_template('postadded.html', title = title, content = content)
  else: return render_template('postpage.html', message = error)


app.run(host='0.0.0.0', port=8080)