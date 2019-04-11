#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''作者图书项目'''

from flask import Flask, render_template, request, redirect,jsonify,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)


class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/author_book'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY='asdasdasdasdasfafa'


app.config.from_object(Config)

db = SQLAlchemy(app)  # 先设置app的config 再传app


class Author(db.Model):
    __tablename__ = 'tbl_anthors'

    id = db.Column(db.Integer, primary_key=True, unique=True)

    name = db.Column(db.String(64), unique=True)

    books = db.relationship('Book', backref='author')


class Book(db.Model):
    __tablename__ = 'tbl_books'

    id = db.Column(db.Integer, primary_key=True, unique=True)

    name = db.Column(db.String(64), unique=True)

    author_id = db.Column(db.Integer, db.ForeignKey('tbl_anthors.id'))


# 创建表单模型类
class AuthorBookForm(FlaskForm):
    author_name = StringField('用户名',validators=[DataRequired('用户名必填')])
    book_name = StringField(label='书籍', validators=[DataRequired(message=u'书籍必填')])
    submit = SubmitField(label='保存')




@app.route('/',methods=['POST','GET'])
def index():
    # 查询数据

    form = AuthorBookForm()
    print('--------------------------------------------------')

    if form.validate_on_submit():
        author_name = form.author_name.data
        book_name = form.book_name.data
        print(book_name)
        author = Author(name=author_name)
        db.session.add(author)

        db.session.commit()

        book = Book(name=book_name, author_id=author.id)

        db.session.add(book)
        db.session.commit()
    author_li = Author.query.all()
    return render_template('index.html', authors=author_li, form=form)

'''POST'''
# @app.route('/delete_book',methods=['POST'])
# def delete_book():
#     req_dict=request.get_json()
#     print(req_dict)
#
#     book_id=req_dict.get('book_id')
#
#     book=Book.query.get(book_id)
#
#     db.session.delete(book)
#     db.session.commit()
#
#     return jsonify(code=0,message='OK')


'''GET'''
@app.route('/delete_book',methods=['GET'])
def delete_book():

    book_id=request.args.get('book_id')

    book=Book.query.get(book_id)


    db.session.delete(book)
    db.session.commit()

    return redirect(url_for('index'))





if __name__ == '__main__':
    # db.drop_all()
    # db.create_all()
    #
    # OneAuthor=Author(name='樋口一叶')
    # TwoAuthor=Author(name='夏目漱石')
    # ThreeAuthor = Author(name='大宰治')
    # FourAuthor = Author(name='芥川龙之介')
    # FiveAuthor = Author(name='村上春树')
    #
    # db.session.add_all([OneAuthor,TwoAuthor,ThreeAuthor,FourAuthor,FiveAuthor])
    # db.session.commit()
    #
    #
    # OneBook = Book(name='青梅竹马',author_id=OneAuthor.id)  #ForeignKey=tbl_authors.id  => author_id=OneAuthor.id
    # TwoBook = Book(name='心',author_id=TwoAuthor.id)
    # ThreeBook = Book(name='人间失格',author_id=ThreeAuthor.id)
    # FourBook = Book(name='罗生门',author_id=FourAuthor.id)
    # FiveBook = Book(name='挪威森林',author_id=FiveAuthor.id)
    #
    # db.session.add_all([OneBook, TwoBook,  ThreeBook, FourBook, FiveBook])
    # db.session.commit()

    app.run(debug=True)

#Warning: (1366, "Incorrect string value: '\\xD6\\xD0\\xB9\\xFA\\xB1\\xEA...' for column 'VARIABLE_VALUE' at row 481")
#result = self._query(query)
'''此处是mysql中文问题，案例还有一个BUG => validators警告信息没有出来'''

