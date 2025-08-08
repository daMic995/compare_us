from api.app import app

if __name__ == "__main__":
    # The host='0.0.0.0' makes the server accessible from your local network.
    # The port and debug settings can be configured here or moved to the config file.
    app.run(host='0.0.0.0', port=5000, debug=True)
