from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"\n========================================================")
    print(f" 🚀 Virtual Study Group Platform Running!")
    print(f" 👉 Access in Browser: http://localhost:{port}")
    print(f"========================================================\n")
    app.run(debug=True, host="127.0.0.1", port=port)