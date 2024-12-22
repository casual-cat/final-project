from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, ssl_context=('/etc/letsencrypt/live/gabi-final-project-devops.online/fullchain.pem', '/etc/letsencrypt/live/gabi-final-project-devops.online/privkey.pem'))

