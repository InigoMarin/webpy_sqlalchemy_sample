import web
from web import form
from handler import *
from models import *
import hashlib

urls = (
  "/list","list",
  "/(.*)", "index"
)

render = web.template.render('templates/', base='layout')

vpass = form.regexp(r".{3,20}$", 'must be between 3 and 20 characters')
vemail = form.regexp(r".*@.*", "must be a valid email address")

register_form = form.Form(
    form.Textbox("username", description="Username"),
    form.Textbox("email", vemail, description="E-Mail"),
    form.Password("password", vpass, description="Password"),
    form.Password("password2", description="Repeat password"),
    form.Button("submit", type="submit", description="Register"),
    validators = [
        form.Validator("Passwords did't match", lambda i: i.password == i.password2)]
)
class index:
    def GET(self,path):
        f = register_form()
        return render.index(f)

    def POST(self,path):
        f = register_form()
        if not f.validates():
            return render.index(f)
        else:
            createSha1 = hashlib.sha1(f.password.value)
            password = createSha1.hexdigest();
            u = User(username=f['username'].value,email=f['email'].value,password=password)
            web.ctx.orm.add(u)
            raise web.seeother('/list')
class list:
    def GET(self):
        return render.list(web.ctx.orm.query(User).all())            

app = web.application(urls, locals())
app.add_processor(load_sqla)

if __name__ == "__main__":
    app.run()

