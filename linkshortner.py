from flask import Flask
from flask import request, jsonify, redirect, abort, render_template, url_for
import pymongo,string,random

app = Flask(__name__, template_folder='templates')
app.config["DEBUG"] = True

myclient = pymongo.MongoClient("mongodb+srv://kanu00047:Theindian%2337@cluster0.dizvk.mongodb.net")
mydb = myclient["url"]["links"]

def get_random_string(length):
    letters = string.ascii_uppercase + string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def shorten_link(url, domain, password):
    randomid = get_random_string(4)

    search_key = "{}".format(randomid)
    myquery = {"shortid": search_key}
    mydoc = mydb.find_one(myquery)

    if mydoc == None:
        post_data = {
            'shortid': '{}'.format(randomid),
            'url': '{}'.format(url),
            'password': '{}'.format(password)
        }
        result = mydb.insert_one(post_data)
        return jsonify({"shortlink": "http://{}/{}".format(domain,randomid),
                        "originallink":"{}".format(url),
                        "owner_of_website":"https://t.me/P4R4D0XXX"})
    else:
        shorten_link(url, domain, password)

@app.route('/')
def home1():
    return redirect("http://github.com/kanishk-sachdeva")

@app.route('/<path:path>', methods=["GET", "POST"])
def home(path):

    if path== None:
        return abort(404,"Not Found")
    else:
        shortnedid = path
        search_key = "{}".format(shortnedid)

        myquery = {"shortid": search_key}
        mydoc = mydb.find_one(myquery)

        if mydoc != None:
            link2 = mydoc.get("url")
            passreq = mydoc.get("password")
            if passreq == "" or passreq == "None":
                s = link2
                if s is not None:
                    if s.find("http://") != 0 and s.find("https://") != 0:
                        s = "http://" + s
                return redirect(s)
            else:
                if request.method == "POST":
                    input1 = request.form.get("url")
                    if passreq == input1:
                        s = link2
                        if s is not None:
                            if s.find("http://") != 0 and s.find("https://") != 0:
                                s = "http://" + s
                        return redirect(s)
                    else:
                        return render_template("wrong.html")


                return render_template("form.html")

        else:
            return render_template("404.html")

@app.route('/shorten', methods=['POST'])
def shorten():
    #url = request.data["url"]
    domain = request.headers['Host']

    password = request.headers.get("password")
    url = request.form.get('url', '')
    print(url)
    if url!=None and url!="":
        return shorten_link(url, domain, password)
    else:
        return abort(401,"Invalid Scheme Provided")

if __name__ == '__main__':
    app.run(debug=True)

