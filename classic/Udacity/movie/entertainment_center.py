import media
import fresh_tomatoes

toy_story = media.Movie("Toy Story", "A story of a boy and his toy blah.. blah",
	"https://upload.wikimedia.org/wikipedia/en/1/13/Toy_Story.jpg", "https://www.youtube.com/watch?v=KYz2wyBy3kc")

#print(toy_story.storyline)
avatar = media.Movie("Avatar",
	"A marine on an alien planet", "https://upload.wikimedia.org/wikipedia/en/b/b0/Avatar-Teaser-Poster.jpg",
	"https://www.youtube.com/watch?v=6ziBFh3V1aM")

#print(avatar.storyline)
#avatar.show_trailer()
raazi = media.Movie("Raazi", "A thriller story of an Indian Spy",
	"https://upload.wikimedia.org/wikipedia/en/2/2f/Raazi_-_Poster.jpg",
	"https://www.youtube.com/watch?v=YjMSttRJrhA")

movies = [avatar, toy_story, raazi]

#fresh_tomatoes.open_movies_page(movies)
print(media.Movie.VALID_RATINGS)
print(media.Movie.__doc__)
print(media.Movie.__name__)
print(media.Movie.__module__)
