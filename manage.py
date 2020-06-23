from app import create_app

app = create_app('dev')

# now we just run command to start server, without params like other python code. It might be attended later

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
