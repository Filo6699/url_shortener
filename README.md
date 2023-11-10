# URL Shortener

A simple URL shortener implemented in Python with a touch of JS.

## Demo

See the URL shortener in action: [urlshort.xyz](https://urlshort.xyz)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Filo6699/url_shortener
   ```

2. (Optional) Create a virtual environment:

   ```bash
   python -m venv venv
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   Note: For psycopg2, you can follow [this guide](https://www.psycopg.org/docs/install.html). Consider using pre-compiled binaries if you are exploring for fun.

4. Create a `.env` file based on `.env.example`.

5. [Set-up your database](database.md).

6. Run the application:

   ```bash
   python main.py
   ```