Navigate to where you want the project
cd Desktop

Clone the project
git clone https://github.com/hafeezabdul8/travel-tanzania-hub.git

Enter project folder
cd travel-tanzania-hub

Create virtual environment
python -m venv venv

Activate virtual environment
venv\Scripts\activate

You should see (venv) at the beginning of your command line
First upgrade pip
python -m pip install --upgrade pip

Install all dependencies
pip install -r requirements.txt

If requirements.txt fails, install manually:
pip install Django==4.2.0 pip install google-genai==0.3.0 pip install pandas==2.1.0 pip install psycopg2-binary==2.9.7 pip install django-cors-headers==4.0.0 pip install python-dotenv==1.0.0

Copy environment template
copy .env.example .env

Edit the .env file with Notepad:
notepad .env

#on the file edit this DEBUG=True SECRET_KEY=django-insecure-your-secret-key-here-change-this DATABASE_URL=sqlite:///db.sqlite3

For Gemini AI (Optional - Get free API key from Google AI Studio)
GEMINI_API_KEY=your-gemini-api-key-here

Or disable AI for now
AI_SERVICE=fallback

#run the project

Start the server
python manage.py runserver

You should see
Starting development server at http://127.0.0.1:8000/ Quit the server with CTRL-BREAK.

#FOR WINDOW USER AND USE CMD TO RUN COMMANDS
