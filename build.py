from app import app

def build():
    print("Building static site...")
    with app.test_client() as client:
        response = client.get('/')
        if response.status_code == 200:
            with open('index.html', 'w', encoding='utf-8') as f:
                f.write(response.data.decode('utf-8'))
            print("Successfully built index.html")
        else:
            print(f"Failed to build index.html. Status code: {response.status_code}")

if __name__ == "__main__":
    build()
