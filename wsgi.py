from app import create_app

app = create_app('test')

if __name__ == "__main__":
    app.run()