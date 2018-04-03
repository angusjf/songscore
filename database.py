def get_db():
    if not hasattr(g, 'db'):
        g.db = sqlite3.connect(app.database)
    return g.db

@app.teardown_appcontext # makes sure if the server breaks we close. ignore the exception
def close_db(exception):
    if hasattr(g, 'db'):
        g.db.close()

def query_db(query, args=(), one=False):
    cursor = get_db().execute(query, args)
    results = cursor.fetchall()
    get_db().commit()
    cursor.close()
    if one: # one -> only expect one result, else returns a dict(?)
        if len(results) > 0:
            return results[0]
        else:
            return None
    else:
        return results
