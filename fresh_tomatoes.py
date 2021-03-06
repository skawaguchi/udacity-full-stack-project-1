'''Creates the web page for Fresh Tomatoes. It depends on the Actor and Movie
modules.'''

import webbrowser
import os
import re
import json

# Styles and scripting for the page
MAIN_PAGE_HEAD = '''
<head>
    <meta charset="utf-8">
    <title>Fresh Tomatoes!</title>
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <link rel="stylesheet" href="styles/main.css">
</head>
'''

# The main page layout and title bar
MAIN_PAGE_CONTENT = '''
<!DOCTYPE html>
<html lang="en">
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container"></div>
        </div>
      </div>
    </div>

    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">Fresh Tomatoes Movie Trailers</a>
          </div>
        </div>
      </div>
    </div>
    <div id="screenshot"></div>
    <ul class="movie-list">
      {movie_tiles}
    </ul>

    <!-- Movie Details -->
    <div id="movie-detail-container"></div>

    <script src="src/polyfills.js"></script>
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <script src="dist/app.js"></script>
  </body>
</html>
'''

# A single movie entry html template
MOVIE_TILE_CONTENT = '''
<li class="movie-tile col-md-4">
    <a class="text-center" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="popover" data-target="#trailer" data-movie-id="{movie_id}" title="{movie_title}" data-content="<span><strong>Year:</strong></span> {year}<br><span><strong>Starring:</strong></span> {actors}<br>{synopsis}" data-trigger="hover" data-html="true" data-placement="bottom">
        <img src="{poster_image_url}" width="220" height="342">
        <h2 class="movie-title">{movie_title}</h2>
    </a>
</li>
'''

def create_actor_list_content(actors):
    '''Returns a comma-separated string of Actor names for display'''
    actor_list = []
    for actor in actors:
        actor_list.append(actor.get_name())
    return ', '.join(actor_list)

def create_movie_tiles_content(movies):
    '''Generates a string with the movie tile markup.'''
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(
            r'(?<=v=)[^&#]+',
            movie.trailer_youtube_url
        )
        youtube_id_match = youtube_id_match or re.search(
            r'(?<=be/)[^&#]+',
            movie.trailer_youtube_url
        )
        trailer_youtube_id = youtube_id_match.group(0) if youtube_id_match else None

        # Append the tile for the movie with its content filled in
        content += MOVIE_TILE_CONTENT.format(
            movie_id=movie.movie_id,
            movie_title=movie.title,
            poster_image_url=movie.poster_image_url,
            trailer_youtube_id=trailer_youtube_id,
            actors=create_actor_list_content(movie.actors),
            year=movie.year,
            synopsis=movie.synopsis
        )

    return content

def open_movies_page(movies):
    '''Launch the Fresh Tomatoes page.'''
    # Create or overwrite the output file
    output_file = open('fresh_tomatoes.html', 'w')

    # Replace the placeholder for the movie tiles with the actual dynamically generated content
    rendered_content = MAIN_PAGE_CONTENT.format(
        movie_tiles=create_movie_tiles_content(movies),
        movie_list=json.dumps(movies, default=lambda o: o.__dict__)
    )

    # Output the file
    output_file.write(MAIN_PAGE_HEAD + rendered_content)
    output_file.close()

    # open the output file in the browser
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2) # open in a new tab, if possible
