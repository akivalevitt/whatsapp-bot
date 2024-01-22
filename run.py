import logging

from app import create_app


app = create_app()

if __name__ == "__main__":
    logging.info("Flask app started")
    app.run(host="https://flask-on-koyeb-ai-automate.koyeb.app/", port=8000)




# remember to delete at circleci, koyeb