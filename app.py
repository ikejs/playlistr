from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient()
db = client.Playlister
playlists = db.playlists


####### TEST PLAYLISTS ########
# playlists = [
#     {
#     'title': 'Cat Videos',
#     'description': 'Cats acting weird',
#     'videos': [
#         {
#         'name': 'Cat Holds a Hotdog',
#         'url': 'https://www.youtube.com/watch?v=j8rrCHWM-W8'
#         },
#         {
#         'name': 'Cats React to Fake Cats',
#         'url': 'https://www.youtube.com/watch?v=SAjs3SdwTAk'
#         }
#     ]
#     },
#     { 'title': '80\'s Music',
#     'description': 'Don\'t stop believing!',
#     'videos': [
#         {
#         'name': 'a-Ha - Take on Me',
#         'url': 'https://www.youtube.com/watch?v=djV11Xbc914'
#         },
#         {
#         'name': "Bon Jovi - Livin' on a Prayer",
#         'url': 'https://www.youtube.com/watch?v=lDK9QqIzhwk'
#         }
#     ]
#     }
# ]

@app.route('/')
def playlists_index():
    """Show all playlists."""
    return render_template('playlist_index.html', playlists=playlists.find())



@app.route('/playlists/new')
def playlists_new():
    """Create a new playlist."""
    return render_template('playlists_new.html', playlist={}, title='New Playlist')



@app.route('/playlists', methods=['POST'])
def playlists_submit():
    """Submit a new playlist."""
    playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split(),
        'rating': request.form.get('rating')
    }
    playlist_id = playlists.insert_one(playlist).inserted_id
    print(playlist_id)
    return redirect(url_for('playlists_show', playlist_id=playlist_id))



@app.route('/playlists/<playlist_id>')
def playlists_show(playlist_id):
    """Show a single playlist."""
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlists_show.html', playlist=playlist)



@app.route('/playlists/<playlist_id>/edit')
def playlists_edit(playlist_id):
    """Show the edit form for a playlist."""
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlists_edit.html', playlist=playlist, title='Edit Playlist')



@app.route('/playlists/<playlist_id>', methods=['POST'])
def playlists_update(playlist_id):
    """Submit an edited playlist."""
    updated_playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split()
    }
    playlists.update_one(
        {'_id': ObjectId(playlist_id)},
        {'$set': updated_playlist})
    return redirect(url_for('playlists_show', playlist_id=playlist_id))


if __name__ == '__main__':
    app.run(debug=True)
