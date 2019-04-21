from flask import Flask, render_template, request, redirect
import base64
from urllib.parse import quote

app = Flask(__name__)


@app.route('/')
def hello_world():

    return render_template("index.html")

@app.route('/deleteportion')
def deleteportion():

    portiontodelete = request.args.get("title")

    curportions = []

    with open("/Users/Hunter/PycharmProjects/onesite/onesite.txt", "r") as file:
        temp = file.read()

        portions = temp.split("$END$")
        portions = portions[:-1]

        for item in portions:
            itemarr = item.split("$$$")
            title = itemarr[0]
            image = itemarr[1]
            editor = itemarr[2]
            if title != portiontodelete:
                curportions.append("{}$$${}$$${}$END$".format(title, image, editor))

    with open("/Users/Hunter/PycharmProjects/onesite/onesite.txt", "w") as file:

        endstr = ""

        for item in curportions:
            endstr += item
        file.write(endstr)


    return redirect("/edit")

@app.route('/edit')
def edit():

    formitemstr = ""

    with open("/Users/Hunter/PycharmProjects/onesite/onesite.txt", "r") as file:
        temp = file.read()

        portions = temp.split("$END$")
        endstr = ""
        navstr = ""
        portions = portions[:-1]
        counter = 0
        print(portions)
        for item in portions:
            print("CURITEM")
            print(item)
            itemarr = item.split("$$$")
            print(itemarr)
            title = itemarr[0]
            image = itemarr[1]
            editor = itemarr[2]

            formitemstr += """
            <a href="/deleteportion?title={}" class='btn btn-danger'>Delete This Portion</a>
            <br>
            <p>Title {}</p>
            <input name="title{}" value="{}">
            <p>Background Image {}</p>
            <input name="image{}" type="file" value="{}">
            <textarea id="summernote{}" name="editor{}">{}</textarea>

            <script>
                $("#summernote{}").summernote();
            </script>


            """.format(title, counter, counter, title, counter, counter, image, counter, counter, editor, counter)
            counter += 1



    return render_template("editbuild.html", edited=formitemstr)


@app.route('/demo', methods=["GET", "POST"])
def demo():

    with open("/Users/Hunter/PycharmProjects/onesite/onesite.txt", "r") as file:
        temp = file.read()

        portions = temp.split("$END$")
        endstr = ""
        navstr = ""
        portions = portions[:-1]
        print(portions)
        for item in portions:
            print("CURITEM")
            print(item)
            itemarr = item.split("$$$")
            print(itemarr)
            title = itemarr[0]
            image = itemarr[1]
            editor = itemarr[2]


            basestr = base64.b64encode(open("/Users/Hunter/PycharmProjects/onesite/{}".format(image), "rb").read())

            navstr += """<li class="nav-item">
                            <a class="nav-link" href="#{}">{}</a>
                          </li>""".format(title, title)

            tempadd = """
                <div class="col-12" style="min-height: 100vh; background: url(data:image/jpg;base64,{}) no-repeat center center fixed; background-size: cover;">

                    <div class="row">

                        <div class="col-12" style="height: 10vh;"></div>

                        <div class="col-2"></div>

                        <div class="col-8 card" id="{}">

                            <div class="card-body">

                                <div style="text-align: center">
                                    <h2>{}</h2>
                                </div>

                                <hr>
                                {}

                            </div>

                        </div>


                        <div class="col-2"></div>

                        <div class="col-12" style="height: 10vh;"></div>

                    </div>

                </div>


            """.format(quote(basestr), title, title, editor)
            endstr += tempadd

        sitetitle = "Onesite"

        with open("/Users/Hunter/PycharmProjects/onesite/site-title.txt", "r") as file:
            sitetitle = file.read()

        return render_template("demo.html", data=endstr, navbar=navstr, sitetitle=sitetitle)



@app.route('/build', methods=["GET", "POST"])
def builder():

    uploads = "/Users/Hunter/PycharmProjects/onesite"

    print(len(request.form))
    print(type(request.form))

    images = {}

    tempcounter = 0

    for item in request.files:
        print(item)
        print(type(item))
        images["image{}".format(tempcounter)] = item
        tempcounter += 1
        file = request.files[item]
        file.save("/Users/Hunter/PycharmProjects/onesite/{}".format(item))


    numinputs = (len(request.form) - 1) / 2
    counter = 0

    with open("/Users/Hunter/PycharmProjects/onesite/onesite.txt", "w") as file:
        endstr = ""

        while numinputs > counter:
            print("NUMINPUTS {}".format(numinputs))
            print("COUNTER {}".format(counter))

            print(request.form.get("title{}".format(counter)))
            endstr += request.form.get("title{}".format(counter)) + "$$$"
            curimage = images["image{}".format(counter)]
            with open("/Users/Hunter/PycharmProjects/onesite/{}".format(curimage), "rb") as file1:

                #endstr += str(base64.b64encode(file1.read())) + "$$$"
                #endstr += str(file1.read()) + "$$$"
                endstr += "{}$$$".format(curimage)

            endstr += request.form.get("editor{}".format(counter)) + "$END$"
            print(request.form.get("editor{}".format(counter)))

            counter += 1

        print("----")
        print(endstr)

        file.write(endstr)



    return redirect("/demo")

@app.route('/editbuild', methods=["GET", "POST"])
def editbuild():

    uploads = "/Users/Hunter/PycharmProjects/onesite"

    print(request.form)
    print(len(request.form))
    print(type(request.form))

    images = {}

    tempcounter = 0

    for item in request.files:
        print(item)
        print(type(item))
        images["image{}".format(tempcounter)] = item
        tempcounter += 1
        file = request.files[item]
        file.save("/Users/Hunter/PycharmProjects/onesite/{}".format(item))



    tempdict = dict(request.form)
    curmax = 0
    for item in list(tempdict.keys()):
        if "title" in item:
            tempmax = int(item[5:])

            if tempmax > curmax:
                curmax = tempmax

    numinputs = curmax + 1
    counter = 0

    with open("/Users/Hunter/PycharmProjects/onesite/onesite.txt", "w") as file:
        endstr = ""

        while numinputs > counter:
            print("NUMINPUTS {}".format(numinputs))
            print("COUNTER {}".format(counter))

            print(request.form.get("title{}".format(counter)))
            endstr += request.form.get("title{}".format(counter)) + "$$$"
            curimage = "image{}".format(counter)
            with open("/Users/Hunter/PycharmProjects/onesite/{}".format(curimage), "rb") as file1:

                #endstr += str(base64.b64encode(file1.read())) + "$$$"
                #endstr += str(file1.read()) + "$$$"
                endstr += "{}$$$".format(curimage)

            endstr += request.form.get("editor{}".format(counter)) + "$END$"
            print(request.form.get("editor{}".format(counter)))

            counter += 1

        print("----")
        print(endstr)

        file.write(endstr)



    return redirect("/demo")


if __name__ == '__main__':
    
    app.run(port=80)
