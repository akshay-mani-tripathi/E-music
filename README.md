Emusic Using AI

Project Overview

Emusic is an music platform designed to revolutionize the way users discover and interact with music. By integrating voice recognition, and Spotify functionality, Emusic offers a seamless and personalized music experience for users.

Features

Song Search Functionality: Search for songs using Spotify’s vast library.

Voice Recognition: Premium users can search for songs using voice commands for a hands-free experience.

User Accounts: Secure user authentication and subscription-based plans.

Technologies Used

Programming Language: Python

Web Framework: Django

Frontend: HTML, CSS, JavaScript

Voice Recognition: SpeechRecognition library

API Integration: Spotify API

Installation

Create a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Set up environment variables:

Create a .env file in the root directory.

Add the following:

SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SECRET_KEY=your_django_secret_key

Run migrations:

python manage.py makemigrations
python manage.py migrate

Start the server:

python manage.py runserver

Usage

Open your browser and navigate to http://127.0.0.1:8000/.

Create an account or log in.

Search for songs via the search bar or use voice commands (for premium users).

View personalized song recommendations.

Project Structure

myproject1
├── accounts            # User authentication and subscription

├── myproject1

├── templates           # HTML templates

├── static              # Static files (CSS, JS, images)

├── requirements.txt    # Python dependencies

├── README.md           # Project documentation

├── manage.py           # Django project manager


Future Enhancements

Implement AI-generated playlists based on user mood.

Add support for multiple languages in voice recognition.

Enable real-time music streaming.

Integrate with other music platforms like Apple Music and YouTube Music.

Contributing

We welcome contributions! To contribute:

Fork the repository.

Create a feature branch:

git checkout -b feature-name

Commit your changes:

git commit -m "Add feature-name"

Push the branch:

git push origin feature-name

Open a Pull Request.

License

This project is licensed under the MIT License. See the LICENSE file for details.

Contact

For queries or feedback, contact:

Email: 2k22.cse.2213249@gmail.com

GitHub: akshay-mani-tripathi

