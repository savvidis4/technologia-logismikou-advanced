from app import create_app

#python3.10 run.py
#npm run dev

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)