import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import urllib.parse as urlparse
from datetime import datetime

app = Flask(__name__)

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Playlister')
client = MongoClient(host=host)
db = client.get_default_database()
playlists = db.playlists
comments = db.comments


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
    videoURLs = request.form.get('videos').split() # List of inputted YouTube URLs
    videos = [] # Collection of YouTube video IDs
    for url in videoURLs: # https://stackoverflow.com/questions/4356538/how-can-i-extract-video-id-from-youtubes-link-in-python
        url_data = urlparse.urlparse(url)
        query = urlparse.parse_qs(url_data.query)
        video = query["v"][0]
        videos.append(video)

    playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': videos,
        'rating': request.form.get('rating'),
        'created_at': datetime.now()
    }
    playlist_id = playlists.insert_one(playlist).inserted_id
    print(playlist_id)
    return redirect(url_for('playlists_show', playlist_id=playlist_id))



@app.route('/playlists/<playlist_id>')
def playlists_show(playlist_id):
    """Show a single playlist."""
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    playlist_comments = comments.find({'playlist_id': ObjectId(playlist_id)})
    return render_template('playlists_show.html', playlist=playlist, comments=playlist_comments)



@app.route('/playlists/<playlist_id>/edit')
def playlists_edit(playlist_id):
    """Show the edit form for a playlist."""
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlists_edit.html', playlist=playlist, title='Edit Playlist')



@app.route('/playlists/<playlist_id>', methods=['POST'])
def playlists_update(playlist_id):
    """Submit an edited playlist."""
    videoURLs = request.form.get('videos').split() # List of inputted YouTube URLs
    videos = [] # Collection of YouTube video IDs
    for url in videoURLs: # https://stackoverflow.com/questions/4356538/how-can-i-extract-video-id-from-youtubes-link-in-python
        url_data = urlparse.urlparse(url)
        query = urlparse.parse_qs(url_data.query)
        video = query["v"][0]
        videos.append(video)

    updated_playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': videos,
        'rating': request.form.get('rating')
    }
    playlists.update_one(
        {'_id': ObjectId(playlist_id)},
        {'$set': updated_playlist})
    return redirect(url_for('playlists_show', playlist_id=playlist_id))



@app.route('/playlists/<playlist_id>/delete', methods=['POST'])
def playlists_delete(playlist_id):
    """Delete one playlist."""
    playlists.delete_one({'_id': ObjectId(playlist_id)})
    return redirect(url_for('playlists_index'))



########## COMMENT ROUTES ##########

@app.route('/playlists/comments', methods=['POST'])
def comments_new():
    """Submit a new comment."""
    comment = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'playlist_id': ObjectId(request.form.get('playlist_id'))
    }
    print(comment)
    comment_id = comments.insert_one(comment).inserted_id
    return redirect(url_for('playlists_show', playlist_id=request.form.get('playlist_id')))



@app.route('/playlists/comments/<comment_id>', methods=['POST'])
def comments_delete(comment_id):
    """Action to delete a comment."""
    comment = comments.find_one({'_id': ObjectId(comment_id)})
    comments.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('playlists_show', playlist_id=comment.get('playlist_id')))





if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 80))
