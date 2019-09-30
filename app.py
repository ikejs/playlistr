from flask import Flask, render_template

app = Flask(__name__)

playlists = [
    {
    'title': 'Cat Videos',
    'description': 'Cats acting weird',
    'videos': [
        {
        'name': 'Cat Holds a Hotdog',
        'url': 'https://www.youtube.com/watch?v=j8rrCHWM-W8'
        },
        {
        'name': 'Cats React to Fake Cats',
        'url': 'https://www.youtube.com/watch?v=SAjs3SdwTAk'
        }
    ]
    },
    { 'title': '80\'s Music',
    'description': 'Don\'t stop believing!',
    'videos': [
        {
        'name': 'a-Ha - Take on Me',
        'url': 'https://www.youtube.com/watch?v=djV11Xbc914'
        },
        {
        'name': "Bon Jovi - Livin' on a Prayer",
        'url': 'https://www.youtube.com/watch?v=lDK9QqIzhwk'
        }
    ]
    }
]

@app.route('/')
def playlists_index():
    """Show all playlists."""
    return render_template('playlist_index.html', playlists=playlists)

if __name__ == '__main__':
    app.run(debug=True)
