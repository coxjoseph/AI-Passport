from src.app import app

if __name__ == '__main__':
    app.run_server(debug=True, port=8050, host='0.0.0.0')
