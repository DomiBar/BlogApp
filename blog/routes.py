from blog import app
from flask import render_template, request, flash, redirect, url_for
from blog.models import Entry, db
from blog.forms import EntryForm

@app.route('/')
def homepage():
    all_posts=Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template("homepage.html", all_posts=all_posts)


def create_and_edit_entry(entry_id=None):
    if entry_id != None:
        entry = Entry.query.filter_by(id=entry_id).first_or_404()
        form = EntryForm(obj=entry)
    else:
        form=EntryForm()
    error = None
    if request.method == 'POST':
        if form.validate_on_submit():
            if entry_id != None:
                form.populate_obj(entry)
            else:
                entry = Entry(
                    title=form.title.data,
                    body=form.body.data,
                    is_published=form.is_published.data
                    )
                db.session.add(entry)
            db.session.commit()
            if entry.is_published==True:
                flash("Dodano nowy wpis do blogu")
            return redirect(url_for('homepage'))
        else:
           error = form.errors
    return render_template('entry_form.html', form=form, error=error)



@app.route("/new-post/", methods=["GET", "POST"])
def create_entry():
    return create_and_edit_entry()

@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
   return create_and_edit_entry(entry_id=entry_id)