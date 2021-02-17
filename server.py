from flask import Flask, render_template, request, redirect, url_for, flash, session
import data_manager
import util

app = Flask(__name__)
app.secret_key = b'\x8d)\xbe\x97\x0b_\xeaT\xbcV\xb5\xeb\xc7SZ\xccm\xc9O\xebD\x83\x80\xef'


@app.template_filter('convert')
def convert_from_timestamp(timestamp):
    return util.convert_timestamp(timestamp)


@app.template_filter('if_exists')
def file_exist_filter(value):
    return data_manager.check_file_exists(value)


@app.route("/")
def main_page():
    questions = data_manager.get_latest_five_questions('submission_time', 'DESC')
    tag_names = data_manager.get_tags_to_question_id()
    return render_template('main_page.html', headers=data_manager.QUESTION_HEADER,
                           questions=questions, title=data_manager.TITLE_HEADER,
                           tag_names=tag_names)


@app.route("/list")
def hello():
    order_by = request.args.get('sort_by', 'submission_time')
    is_reversed = 'DESC' if request.args.get('reverse') else 'ASC'
    tag_names = data_manager.get_tags_to_question_id()
    questions = data_manager.get_questions(order_by, is_reversed)
    return render_template('index.html', headers=data_manager.QUESTION_HEADER,
                           questions=questions, title=data_manager.TITLE_HEADER,
                           order_by=order_by, is_reversed=is_reversed, tag_names=tag_names)


@app.route("/registration", methods=['GET', 'POST'])
def route_registration():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = util.hash_password(request.form['password'])
        if data_manager.check_user_data('username', username) is True:
            flash('This username is already taken!')
            return redirect(request.url)
        elif data_manager.check_user_data('email_address', email) is True:
            flash('This email address is already taken!')
            return redirect(request.url)
        elif not util.verify_password(request.form['password2'], password):
            flash('The passwords are different!')
            return redirect(request.url)
        else:
            data_manager.add_user(username, email, password)
            session['id'] = data_manager.get_user_id(username)[0]['id']
            session['username'] = username
            return redirect(url_for('main_page'))
    else:
        return render_template("registration.html")


@app.route("/login", methods=['GET', 'POST'])
def route_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            if not util.verify_password(password, data_manager.get_password(username)[0]['password']):
                flash("Incorrect password or username!")
                return redirect(request.url)
            else:
                session['id'] = data_manager.get_user_id(username)[0]['id']
                session['username'] = username
                return redirect(url_for('main_page'))
        except IndexError:
            flash("Incorrect password or username!")
            return redirect(request.url)
    else:
        return render_template("login.html")


@app.route("/logout")
def route_logout():
    session.clear()
    return redirect(url_for("main_page"))


@app.route("/users")
def users_list():
    if 'username' not in session:
        return redirect(url_for("main_page"))
    else:
        users = data_manager.get_all_users()
        return render_template("list_users.html", users=users)


@app.route("/user/<user_id>")
def user_details(user_id):
    if 'username' not in session:
        return redirect(url_for("main_page"))
    else:
        user = data_manager.get_a_user(user_id)[0]
        answers = data_manager.get_data_from_user('answer', user_id)
        comments = data_manager.get_data_from_user('comment', user_id)
        questions = data_manager.get_data_from_user('question', user_id)
        return render_template("user_details.html", user=user, answers=answers,
                               comments=comments, questions=questions)


@app.route("/answer/comment/<int:answer_id>/")
def route_to_question_from_answer(answer_id):
    question = data_manager.get_question_by_a_id(answer_id)[0]
    print(question)
    return redirect(url_for("display_question", question_id=question['id']))


@app.route("/question/<int:question_id>")
def display_question(question_id):
    if '/question' not in request.referrer:
        data_manager.increase_display_count(question_id)
    tag_names = data_manager.get_tag_name_by_question_id(question_id)
    question = data_manager.get_question_by_id(question_id)
    answers = data_manager.get_answers_by_question_id(question_id)
    qcomments_list = data_manager.get_question_comments_with_username(question_id)
    acomments_list = data_manager.get_answers_comments_with_username(question_id)
    return render_template('question.html', headers=data_manager.ANSWER_HEADER,
                           question=question[0], answers=answers,
                           qcomments=qcomments_list,
                           acomments=acomments_list,
                           tag_names=tag_names)


@app.route("/question/<int:question_id>/new-tag", methods=['GET', 'POST'])
def add_tag_to_question(question_id):
    if 'username' not in session:
        return redirect(url_for("main_page"))
    else:
        tag_list = data_manager.get_tag_that_not_in_question(question_id)
        if request.method == 'GET':
            question = data_manager.get_question_by_id(question_id)[0]
            tag_names = data_manager.get_tag_name_by_question_id(question_id)
            return render_template('tag.html', tag_list=tag_list, question=question, tag_names=tag_names)
        else:
            checked_tags = request.form.getlist('tags')
            new_tag = request.form.get('new_tag', None).split()
            tags = checked_tags + new_tag
            for tag in tags:
                data_manager.modify_tag(question_id, tag)
            return redirect(f"/question/{question_id}")


@app.route("/question/<int:question_id>/new-comment", methods=['GET', 'POST'])
def add_comment_to_question(question_id):
    if 'username' not in session:
        return redirect(url_for("main_page"))
    else:
        if request.method == "GET":
            question = data_manager.get_question_by_id(question_id)[0]
            return render_template('qcomment.html', question=question)
        else:
            user_id = session['id']
            data_manager.add_comment_to_question(request.form['message'], question_id, user_id)
            return redirect(f"/question/{question_id}")


@app.route("/answer/<int:answer_id>/new-comment", methods=['GET', 'POST'])
def add_comment_to_answer(answer_id):
    if 'id' not in session:
        return redirect(url_for("main_page"))
    else:
        if request.method == "GET":
            answer = data_manager.get_an_answer(answer_id)[0]
            question = data_manager.get_question_by_a_id(answer_id)
            return render_template('acomment.html', answer=answer,
                                   question=question[0])
        else:
            user_id = session['id']
            question_id = data_manager.get_question_id_by_answer_id(answer_id)
            data_manager.add_comment_to_answer(request.form['message'], answer_id, user_id)
            return redirect(f"/question/{question_id}")


@app.route("/add-question", methods=['GET', 'POST'])
def add_question():
    if 'id' not in session:
        return redirect(url_for("main_page"))
    else:
        if request.method == "GET":
            return render_template("form_question.html")
        elif request.method == "POST":
            file_name = "default.png"
            uploaded_image = request.files['image']
            if uploaded_image.filename != '':
                uploaded_image.save(data_manager.path_to_image(uploaded_image.filename))
                file_name = uploaded_image.filename
            user_id = session['id']
            data_manager.add_question(request.form['title'], request.form['message'], file_name, user_id)
            return redirect("/")


@app.route("/question/<int:question_id>/new-answer", methods=['GET', 'POST'])
def add_answer(question_id):
    if 'username' not in session:
        return redirect(url_for("main_page"))
    else:
        if request.method == "GET":
            question = data_manager.get_question_by_id(question_id)[0]
            tag_names = data_manager.get_tag_name_by_question_id(question_id)
            return render_template('form_answer.html', question=question, tag_names=tag_names)
        elif request.method == "POST":
            file_name = "default.png"
            uploaded_image = request.files['image']
            user_id = session['id']
            if uploaded_image.filename != '':
                uploaded_image.save(data_manager.path_to_image(uploaded_image.filename))
                file_name = uploaded_image.filename
                # !!!!! answer id
            data_manager.add_answer(request.form['message'], question_id, file_name, user_id)
            return redirect(url_for("display_question", question_id=question_id))


@app.route("/search")
def search_phrase():
    phrase = request.args.get('q')
    question_list = data_manager.search_in_questions(phrase)
    answers_list = data_manager.search_in_answers(phrase)
    tag_names = data_manager.get_tags_to_question_id()
    # need filter question_owner!!!
    question_owner = data_manager.get_question_owners()
    return render_template("searchresults.html", questions=question_list, phrase=phrase,
                           answers=answers_list, tag_names=tag_names, question_owner=question_owner)


@app.route("/question/<int:question_id>/delete")
def delete_question(question_id):
    # data_manager.delete_all_comments_by_que_id(question_id)
    # data_manager.delete_answer_by_question_id(question_id)
    # data_manager.delete_all_tag_by_q_id(question_id)
    data_manager.delete_question_by_id(question_id)
    return redirect("/")


@app.route("/question/<int:question_id>/edit", methods=["GET", "POST"])
def edit_question(question_id):
    if 'username' not in session:
        return redirect(url_for("main_page"))
    else:
        question = data_manager.get_question_by_id(question_id)
        if request.method == "GET":
            return render_template("form_question.html", question=question[0])
        elif request.method == "POST":
            uploaded_image = request.files['image']
            file_name = data_manager.get_question_by_id(question_id)[0]['image']
            if uploaded_image.filename != '':
                uploaded_image.save(data_manager.path_to_image(uploaded_image.filename))
                data_manager.delete_unused_image(file_name)
                file_name = uploaded_image.filename
            data_manager.update_question(request.form['title'], request.form['message'], file_name, question_id)
            return redirect(url_for("display_question", question_id=question_id))


@app.route("/answer/<int:answer_id>/edit", methods=["GET", "POST"])
def edit_answer(answer_id):
    if 'username' not in session:
        return redirect(url_for("main_page"))
    else:
        answer = data_manager.get_an_answer(answer_id)
        if request.method == "GET":
            question = data_manager.get_question_by_a_id(answer_id)[0]
            return render_template("form_answer.html", question=question,
                                   answer=answer[0])
        else:
            uploaded_image = request.files['image']
            file_name = answer[0]['image']
            if uploaded_image.filename != '':
                uploaded_image.save(data_manager.path_to_image(uploaded_image.filename))
                data_manager.delete_unused_image(file_name)
                file_name = uploaded_image.filename
            data_manager.update_answer(request.form['message'], file_name, answer_id)
            return redirect(url_for("display_question", question_id=answer[0]['question_id']))


@app.route("/comments/<comment_id>/edit", methods=['GET', 'POST'])
def edit_comment(comment_id):
    if 'username' not in session:
        return redirect(url_for("main_page"))
    else:
        comment = data_manager.get_comments_by_id(comment_id)[0]
        if request.method == 'GET':
            if comment['question_id'] is None:
                answer = data_manager.get_an_answer(comment['answer_id'])[0]
                question = data_manager.get_question_by_a_id(answer['id'])[0]
                return render_template("acomment.html", answer=answer,
                                       comment=comment, question=question)
            else:
                question = data_manager.get_question_by_id(comment['question_id'])[0]
                return render_template("qcomment.html", question=question, comment=comment)
        else:
            message = request.form['message']
            data_manager.update_comment(message, comment_id)
            if comment['question_id'] is None:
                answer = data_manager.get_an_answer(comment['answer_id'])[0]
                comment = answer
            return redirect(f"/question/{comment['question_id']}")


@app.route("/answer/<int:answer_id>/delete", methods=['GET'])
def delete_answer(answer_id):
    question = data_manager.get_question_by_a_id(answer_id)[0]
    # data_manager.delete_all_comments_by_ans_id(answer_id)
    data_manager.delete_answer_by_answer_id(answer_id)
    return redirect(url_for("display_question", question_id=question['id']))


@app.route("/comments/<comment_id>/delete")
def delete_comment(comment_id):
    comment = data_manager.get_comments_by_id(comment_id)[0]
    if comment['question_id'] is None:
        answer = data_manager.get_an_answer(comment['answer_id'])[0]
        comment = answer
    data_manager.delete_comment_by_c_id(comment_id)
    return redirect(f"/question/{comment['question_id']}")


@app.route("/question/<int:question_id>/vote_up")
def question_vote_up(question_id):
    owner_id = data_manager.get_question_by_id(question_id)[0]['user_id']
    if 'id' in session and session['id'] != owner_id:
        if not data_manager.check_vote_updown('question_id', question_id, session['id']):
            # vote up blue->green
            data_manager.update_vote_to_question(question_id, 1)
            data_manager.update_reputation(owner_id, 5)
            data_manager.create_vote('question_id', question_id, session['id'], True)
        elif data_manager.check_vote_updown('question_id', question_id, session['id'])[0]['updown']:
            # vote up green->blue
            data_manager.update_vote_to_question(question_id, -1)
            data_manager.update_reputation(owner_id, -5)
            data_manager.delete_vote('question_id', question_id, session['id'])
        elif not data_manager.check_vote_updown('question_id', question_id, session['id'])[0]['updown']:
            # vote down red->blue vote up blue->green
            data_manager.update_vote_to_question(question_id, 2)
            data_manager.update_reputation(owner_id, 7)
            data_manager.delete_vote('question_id', question_id, session['id'])
            data_manager.create_vote('question_id', question_id, session['id'], True)

    return redirect(request.referrer)


@app.route("/question/<int:question_id>/vote_down")
def question_vote_down(question_id):
    owner_id = data_manager.get_question_by_id(question_id)[0]['user_id']
    if 'id' in session and session['id'] != owner_id:
        if not data_manager.check_vote_updown('question_id', question_id, session['id']):
            # vote up blue->red
            data_manager.update_vote_to_question(question_id, -1)
            data_manager.update_reputation(owner_id, -2)
            data_manager.create_vote('question_id', question_id, session['id'], False)
        elif data_manager.check_vote_updown('question_id', question_id, session['id'])[0]['updown']:
            # vote up green->blue down blue->red
            data_manager.update_vote_to_question(question_id, -2)
            data_manager.update_reputation(owner_id, -7)
            data_manager.delete_vote('question_id', question_id, session['id'])
            data_manager.create_vote('question_id', question_id, session['id'], False)
        elif not data_manager.check_vote_updown('question_id', question_id, session['id'])[0]['updown']:
            # vote down red->blue
            data_manager.update_vote_to_question(question_id, 1)
            data_manager.update_reputation(owner_id, 2)
            data_manager.delete_vote('question_id', question_id, session['id'])

    return redirect(request.referrer)


@app.route("/answer/<int:answer_id>/vote_up")
def answer_vote_up(answer_id):
    owner_id = data_manager.get_an_answer(answer_id)[0]['user_id']
    if 'id' in session and session['id'] != owner_id:
        if not data_manager.check_vote_updown('answer_id', answer_id, session['id']):
            # vote up blue->green
            data_manager.update_vote_to_answer(answer_id, 1)
            data_manager.update_reputation(owner_id, 10)
            data_manager.create_vote('answer_id', answer_id, session['id'], True)
        elif data_manager.check_vote_updown('answer_id', answer_id, session['id'])[0]['updown']:
            # vote up green->blue
            data_manager.update_vote_to_answer(answer_id, -1)
            data_manager.update_reputation(owner_id, -10)
            data_manager.delete_vote('answer_id', answer_id, session['id'])
        elif not data_manager.check_vote_updown('answer_id', answer_id, session['id'])[0]['updown']:
            # vote down red->blue vote up blue->green
            data_manager.update_vote_to_answer(answer_id, 2)
            data_manager.update_reputation(owner_id, 12)
            data_manager.delete_vote('answer_id', answer_id, session['id'])
            data_manager.create_vote('answer_id', answer_id, session['id'], True)

    # data_manager.make_answer_vote(answer_id, 'up')
    question_id = data_manager.get_question_id_by_answer_id(answer_id)
    return redirect(url_for("display_question", question_id=question_id))
    # return redirect(url_for(request.referrer, question_id=question_id))


@app.route("/answer/<int:answer_id>/vote_down")
def answer_vote_down(answer_id):
    owner_id = data_manager.get_an_answer(answer_id)[0]['user_id']
    if 'id' in session and session['id'] != owner_id:
        if not data_manager.check_vote_updown('answer_id', answer_id, session['id']):
            # vote up blue->red
            data_manager.update_vote_to_answer(answer_id, -1)
            data_manager.update_reputation(owner_id, -2)
            data_manager.create_vote('answer_id', answer_id, session['id'], False)
        elif data_manager.check_vote_updown('answer_id', answer_id, session['id'])[0]['updown']:
            # vote up green->blue down blue->red
            data_manager.update_vote_to_answer(answer_id, -2)
            data_manager.update_reputation(owner_id, -12)
            data_manager.delete_vote('answer_id', answer_id, session['id'])
            data_manager.create_vote('answer_id', answer_id, session['id'], False)
        elif not data_manager.check_vote_updown('answer_id', answer_id, session['id'])[0]['updown']:
            # vote down red->blue
            data_manager.update_vote_to_answer(answer_id, 1)
            data_manager.update_reputation(owner_id, 2)
            data_manager.delete_vote('answer_id', answer_id, session['id'])

    # data_manager.make_answer_vote(answer_id, 'down')
    question_id = data_manager.get_question_id_by_answer_id(answer_id)
    return redirect(url_for("display_question", question_id=question_id))
    # return redirect(url_for(request.referrer))


@app.route("/answer/<answer_id>/vote/<value>")
def vote_accept(answer_id, value):
    question = data_manager.get_question_by_a_id(answer_id)[0]
    if 'id' in session and session['id'] == question['user_id']:
        rep_num = 15 if value == 'False' else -15
        answer_owner_id = data_manager.get_an_answer(answer_id)[0]['user_id']
        data_manager.update_reputation(answer_owner_id, rep_num)
        new_value = True if value == 'False' else False
        data_manager.update_answer_accepted(answer_id, new_value)

    return redirect(f"/question/{question['id']}")


@app.route("/question/<question_id>/tag/<tag_id>/delete")
def delete_tag(question_id, tag_id):
    data_manager.delete_tag_by_q_id(question_id, tag_id)
    return redirect(request.referrer)


if __name__ == "__main__":
    app.run(
        port=5000,
        debug=True
    )
