from gevent.pywsgi import WSGIServer


'--- SERVER RUN ---'
if __name__ == '__main__':
    WSGIServer((app.config['HOST'], app.config['PORT']), app).serve_forever()
