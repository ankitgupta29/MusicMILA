import web
import json

from classifySongFromTweet import *

def make_text(string):
    return string

urls = ('/', 'tutorial')
render = web.template.render('templates/')

app = web.application(urls, globals())

my_form = web.form.Form(
                web.form.Textbox('', class_='header-slider', id='textfield'),
               )

class tutorial:
    def GET(self):
        form = my_form()
        return render.tutorial(form, "Your text goes here.")
        #return render.tutorial("your text ")
        
    def POST(self):
        form = my_form()
        form.validates()
        tweet = form.value['textfield']
        print tweet
        classifySong(tweet)
        
        return make_text(tweet)
        #return render.index(greeting = greeting)
       #
      

if __name__ == '__main__':
    app.run()

