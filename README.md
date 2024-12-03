# Sortify

<img src="https://raw.githubusercontent.com/KeremKurban/Sortify/dev/images/ui_example.png" alt="UI Example" width="400"/>

Sortify is a web application that allows users to sort their favorite Spotify album tracks based on their preferences. Users can input an album link, compare two songs at a time, and choose their preference until all songs are sorted. The application also displays album covers and provides play buttons for each song during the comparison phase.

## Features

- Sort Spotify album tracks based on user preferences
- Display album covers during comparisons
- Play buttons for each song to listen before making a choice
- User-friendly interface

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Spotify Developer Account

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/sortify.git
    cd sortify
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    Create a `.env` file in the root directory and add your Spotify API credentials:
    ```env
    SPOTIFY_CLIENT_ID=your_spotify_client_id
    SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
    SPOTIFY_REDIRECT_URI=http://localhost:5001/callback
    SECRET_KEY=your_secret_key
    ```

5. Run the application:
    ```bash
    python run.py
    ```

6. Open your browser and go to `http://localhost:5001`.

## Deployment

To deploy Sortify on Render, ensure your `render.yaml` is correctly configured and follow the deployment instructions on Render's website.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Spotipy](https://github.com/plamere/spotipy) - A lightweight Python library for the Spotify Web API
- [Flask](https://flask.palletsprojects.com/) - A lightweight WSGI web application framework