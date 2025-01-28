from app import app , db

@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('DataBase Created Successfuly')

if __name__=='__main__':
    app.run(debug=True)
