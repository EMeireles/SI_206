import unittest
import proj1_w18 as proj1
import json
import requests

with open('sample_json.json') as json_data:
    d= json.load(json_data)

    

class TestClasses(unittest.TestCase):

    def testMedia(self):
        m1 = proj1.Media()
        m2 = proj1.Media("1999", "Prince")
        m3=proj1.Media("1999","Prince","1999")
        m4 = proj1.Media(json=d[0])
              
        self.assertEqual(m1.title, "No Title")
        self.assertEqual(m1.author, "No Author")
        self.assertEqual(m1.release_year,"0000")
        self.assertEqual(m1.url,"")

        self.assertEqual(m2.title, "1999")
        self.assertEqual(m2.author, "Prince")
        self.assertEqual(m2.url,"")
        self.assertEqual(m2.__str__(),"1999 by Prince (0000)")

        self.assertEqual(m3.title, "1999")
        self.assertEqual(m3.author, "Prince")
        self.assertEqual(m3.release_year,"1999")
        self.assertEqual(m3.url,"")
        self.assertEqual(m3.__str__(),"1999 by Prince (1999)")


        self.assertEqual(m4.title,"Jaws")
        self.assertEqual(m4.author,"Steven Spielberg")
        self.assertEqual(m4.release_year,"1975")
        self.assertEqual(m4.url,"http://video.itunes.apple.com/apple-assets-us-std-000001/Video127/v4/a5/4c/6d/a54c6d2c-7003-1ae7-f002-84b4444bc05b/mzvf_5104399247891878253.640x266.h264lc.U.p.m4v")
        self.assertEqual(m4.__str__(),"Jaws by Steven Spielberg (1975)")

    def testSong(self):
        s1=proj1.Song()
        s2=proj1.Song("Oveture","AJR","2017","Living Room",180,"Alternative")
        s3=proj1.Song(json=d[1])

        self.assertEqual(s1.title,"No Title")
        self.assertEqual(s1.author,"No Author")
        self.assertEqual(s1.release_year,"0000")
        self.assertEqual(s1.album,"Generic Title")
        self.assertEqual(s1.track_length,0)
        self.assertEqual(s1.genre,"Rock")
        self.assertEqual(s1.url,"")
        self.assertEqual(s1.__str__(),"No Title by No Author (0000) [Rock]")

        self.assertEqual(s2.title,"Oveture")
        self.assertEqual(s2.author,"AJR")
        self.assertEqual(s2.release_year,"2017")
        self.assertEqual(s2.album,"Living Room")
        self.assertEqual(s2.track_length,180)
        self.assertEqual(s2.genre,"Alternative")
        self.assertEqual(s2.url,"")
        self.assertEqual(s2.__str__(),"Oveture by AJR (2017) [Alternative]")


        self.assertEqual(s3.title,"Hey Jude")
        self.assertEqual(s3.author,"The Beatles")
        self.assertEqual(s3.release_year,"1968")
        self.assertEqual(s3.album,"The Beatles 1967-1970 (The Blue Album)")
        self.assertEqual(s3.track_length,431333)
        self.assertEqual(s3.genre,"Rock")
        self.assertEqual(s3.url,"https://audio-ssl.itunes.apple.com/apple-assets-us-std-000001/Music/v4/d5/c8/10/d5c81035-a242-c354-45cf-f634e4127f43/mzaf_1171292596660883824.plus.aac.p.m4a")
        self.assertEqual(s3.__str__(),"Hey Jude by The Beatles (1968) [Rock]")

    def testMovie(self):
        m1=proj1.Movie()
        m2=proj1.Movie("The Prestige","Christopher Nolan","2006","PG-13",120)
        m3=proj1.Movie(json=d[0])

        self.assertEqual(m1.title,"No Title")
        self.assertEqual(m1.author,"No Author")
        self.assertEqual(m1.release_year,"0000")
        self.assertEqual(m1.rating,"PG")
        self.assertEqual(m1.movie_length,0)
        self.assertEqual(m1.url,"")
        self.assertEqual(m1.__str__(),"No Title by No Author (0000) [PG]")

        self.assertEqual(m2.title, "The Prestige")
        self.assertEqual(m2.author,"Christopher Nolan")
        self.assertEqual(m2.release_year,"2006")
        self.assertEqual(m2.rating,"PG-13")
        self.assertEqual(m2.movie_length,120)
        self.assertEqual(m2.url,"")
        self.assertEqual(m2.__str__(),"The Prestige by Christopher Nolan (2006) [PG-13]")

        self.assertEqual(m3.title, "Jaws")
        self.assertEqual(m3.author,"Steven Spielberg")
        self.assertEqual(m3.release_year,"1975")
        self.assertEqual(m3.rating,"PG")
        self.assertEqual(m3.movie_length,7451455)
        self.assertEqual(m3.url,"http://video.itunes.apple.com/apple-assets-us-std-000001/Video127/v4/a5/4c/6d/a54c6d2c-7003-1ae7-f002-84b4444bc05b/mzvf_5104399247891878253.640x266.h264lc.U.p.m4v")
        self.assertEqual(m3.__str__(),"Jaws by Steven Spielberg (1975) [PG]")

    def test_search(self):
        self.assertEqual(len(proj1.fetch("moana")),50)
        self.assertEqual(proj1.fetch("!@#@$@#$@#$%@#%@#$#@$"),"Sorry that query doesn't work! Please try again!")
        self.assertEqual(len(proj1.fetch("helter skelter")),50)

    def test_len(self):
        m1=proj1.Media()
        s1=proj1.Song(track_length=1000)
        s2=proj1.Song(json=d[1])
        mov1=proj1.Movie(movie_length=2300)
        mov2=proj1.Movie(json=d[0])

        self.assertEqual(m1.__len__(),0)
        self.assertEqual(s2.__len__(),431333/1000)
        self.assertEqual(s1.__len__(),1)
        self.assertEqual(mov1.__len__(),round((2300/1000)/60))
        self.assertEqual(mov2.__len__(),round((7451455/1000)/60))



unittest.main()


