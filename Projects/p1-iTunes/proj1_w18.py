##Emil Merieles

import requests
import json
import webbrowser

class Media(object):
	def __init__(self, title="No Title", author="No Author",release_year="0000",url="",json=None):
		if json==None:
			self.title = title
			self.author = author
			self.release_year=release_year
			self.url=url
		else:
			try:
				self.title = json['trackName']
			except:
				self.title=json['collectionName']
			self.author = json['artistName']
			self.release_year=json['releaseDate'][0:4]
			try:
				self.url=json['previewUrl']
			except:
				self.url=json['trackViewUrl']
				
	def __str__(self):
		return "{} by {} ({})".format(self.title,self.author,self.release_year)
	def __len__(self):
		return 0


class Song(Media):
	def __init__(self, title="No Title", author="No Author",release_year="0000", album="Generic Title", track_length=0,genre="Rock",url="",json=None,):
		if json == None:
			super().__init__(title,author,release_year,url)
			self.album=album
			self.track_length=track_length
			self.genre=genre
		else:
			super().__init__(title,author,release_year,url,json = json)
			self.album = json['collectionName']
			self.track_length=json['trackTimeMillis']
			self.genre=json['primaryGenreName']

	def __str__(self):
		return "{} by {} ({}) [{}]".format(self.title,self.author,self.release_year,self.genre)
	def __len__(self):
		second_time=self.track_length/1000
		return second_time

class Movie(Media):
	def __init__(self, title="No Title", author="No Author",release_year="0000", rating="PG",movie_length=0,url="",json=None):
		if json == None:
			super().__init__(title,author,release_year,url)
			self.rating=rating
			self.movie_length=movie_length
		else:
			super().__init__(title,author,release_year,url,json= json)
			self.rating=json['contentAdvisoryRating']
			self.movie_length=json['trackTimeMillis']

	def __str__(self):
		return "{} by {} ({}) [{}]".format(self.title,self.author,self.release_year,self.rating)

	def __len__(self):
		minute_time= round((self.movie_length/1000)/60)
		return minute_time


def fetch(query):
	try:
		data=requests.get('https://itunes.apple.com/search?term={}'.format(query))
		parse=json.loads(data.text)
		return parse['results']
	except:
		return "Sorry that query doesn't work! Please try again!"

		 
def main(last_impt=None):
	last_impt=input("Enter a search term, or 'exit' to quit: ")
	while(last_impt!='exit'):
		songs=[]
		movies=[]
		other=[]

		data=fetch(last_impt)
		if data!="Sorry that query doesn't work! Please try again!":
			for dic in data:
				try:
					if dic['kind']=='song':
						ins=Song(json=dic)
						songs.append((ins.__str__(),ins.url))

					elif dic['kind']=='feature-movie':
						mov_ins=Movie(json=dic)
						movies.append((mov_ins.__str__(),mov_ins.url))
					else:
						om_ins=Media(json=dic)
						other.append((om_ins.__str__(),om_ins.url))
				except:
					if dic['wrapperType']=='audiobook':
						book=Media(json=dic)
						other.append((book.__str__(),book.url))

					elif dic['kind']=='podcast':
						pod=Media(json=dic)
						other.append(pod.__str__(),pod.url)

			agg_list=[]


			for sng in songs:
				agg_list.append(sng)

			for mov in movies:
				agg_list.append(mov)

			for ot in other:
				agg_list.append(ot)

			num=1

			if len(songs)==0:
				print("SONGS:")
				print("No songs!")
			else:
				print("SONGS:")
				for sng in songs:
					print(str(num)+"."+sng[0])
					num+=1

			if len(movies)==0:
				print("MOVIES:")
				print("No movies!")

			else:
				print("MOVIES:")
				for mov in movies:
					print(str(num)+"."+mov[0])
					num+=1

			if len(other)==0:
				print("OTHER MEDIA:")
				print("No other media!")

			else:
				print("OTHER MEDIA:")
				for om in other:
					print(str(num)+"."+om[0])
					num+=1

			impt=input("Enter a number to listen or view a preview of an item, or entanother search term, or exit:")

			try:
				webbrowser.open(str(agg_list[int(impt)-1][1]))
			except:
				last_impt=impt

		else:
			last_impt=input("Sorry,that didn't work! Please try again or enter 'exit' to quit:")


if __name__ == '__main__':
	main()
	print("Bye!")







































