import web
import json
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
        #form = web.input(greet="hell")
       # #s = "%s" % ( form.name)
        #greeting = "%s" % (form.greet)
       # print greeting
        #return render.index(greeting = greeting)
        s = form.value['textfield']
        #classifySong(s)
        return make_text(s)
        #return render.index(greeting = greeting)
       #
      

if __name__ == '__main__':
    app.run()

