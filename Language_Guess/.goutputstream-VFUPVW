from guess_language import guess_language
import os,sys
import json as simplejson

def main():
				cd = os.getcwd()
				
				for root,dirs,files in os.walk(cd):
								for item in dirs:
		
												if not item == 'guess':
																for root,dirs,files in os.walk('data1'):
																				print (files)
											
							
												
				'''										
				f = open('geo.2013-03-01_00-03.txt', "r")
				lines = f.readlines()
				i,no = 0,0
				txtfile = open('tweetdata.txt',mode ='wt')
				for line in lines:	
								try:
												tweet = simplejson.loads(line)
												if "text" in tweet:
																text = str(tweet["text"].encode('utf-8','ignore'))
																language = guess_language(text)
																if language == 'en':
																				txtfile.write(line)
																				
															
													
								except ValueError:
												pass
				'''


if __name__ == '__main__':
 main()

