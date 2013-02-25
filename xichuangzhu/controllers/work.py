#-*- coding: UTF-8 -*-

from flask import render_template, request, redirect, url_for, json

from xichuangzhu import app, conn, cursor

from xichuangzhu.models.work_model import Work
from xichuangzhu.models.dynasty_model import Dynasty
from xichuangzhu.models.author_model import Author
from xichuangzhu.models.collection_model import Collection
from xichuangzhu.models.review_model import Review

import markdown2

import re

# page - single work
#--------------------------------------------------

@app.route('/work/<int:work_id>')
def single_work(work_id):
	work = Work.get_work(work_id)
	work['Content'] = re.sub(r'<([^<]+)>', r"<sup title='\1'></sup>", work['Content'])
	work['Content'] = markdown2.markdown(work['Content'])
	reviews = Review.get_reviews_by_work(work['WorkID'])
	return render_template('single_work.html', work=work, reviews=reviews)

# page - all works
#--------------------------------------------------
@app.route('/works')
def works():
	works = Work.get_works()
	for work in works:
		work['Content'] = re.sub(r'<([^<]+)>', '', work['Content'])
	return render_template('works.html', works=works)

# page - add work
#--------------------------------------------------

@app.route('/work/add', methods=['GET', 'POST'])
def add_work():
	if request.method == 'GET':
		return render_template('add_work.html')
	elif request.method == 'POST':
		title        = request.form['title']
		content      = request.form['content']
		authorID     = int(request.form['authorID'])
		dynastyID    = Dynasty.get_dynastyID_by_author(authorID)
		collectionID = int(request.form['collectionID'])
		type = request.form['type']
		newWorkID = Work.add_work(title, content, authorID, dynastyID, collectionID, type)
		return redirect(url_for('single_work', workID=newWorkID))

# page - edit work
#--------------------------------------------------

@app.route('/work/edit/<int:work_id>', methods=['GET', 'POST'])
def edit_work(work_id):
	if request.method == 'GET':
		work = Work.get_work(work_id)
		return render_template('edit_work.html', work=work)
	elif request.method == 'POST':
		title        = request.form['title']
		content      = request.form['content']
		intro        = request.form['introduction']
		authorID     = int(request.form['authorID'])
		dynastyID    = Dynasty.get_dynastyID_by_author(authorID)
		collectionID = int(request.form['collectionID'])
		type         = request.form['type']
		Work.edit_work(title, content, intro ,authorID, dynastyID, collectionID, type, work_id)
		return redirect(url_for('single_work', work_id=work_id))

# proc - delete work
#--------------------------------------------------

# @app.route('/work/delete/<int:workID>', methods=['GET'])
# def delete_work(workID):
# 	Work.delete_work(workID)
# 	return redirect(url_for('index'))

# helper - search authors and their collections in page add work
#--------------------------------------------------

@app.route('/work/search_authors', methods=['POST'])
def get_authors_by_name():
	name = request.form['author']
	authors = Author.get_authors_by_name(name)
	for author in authors:
		author['Collections'] = Collection.get_collections_by_author(author['AuthorID'])
	return json.dumps(authors)

# helper - search the author's collections in page edit work
#--------------------------------------------------
@app.route('/work/search_collections', methods=['POST'])
def get_collections_by_author():
	authorID = int(request.form['authorID'])
	collections = Collection.get_collections_by_author(authorID)
	return json.dumps(collections)
