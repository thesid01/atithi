# -*- coding: utf-8 -*-

from .root import app


@app.handle(intent='generic')
def generic(request, responder):
    responder.reply("Sure, what do you want to know?")
    responder.params.target_dialogue_state = 'india'
    responder.listen()


@app.handle(intent='india')
def india(request, responder):
    query = request.text
    answers = app.question_answerer.get(index='faq', query_type='text', question=query,answer=query)
    if answers:
        reply = ['Here is the top result:', answers[0]['question'], answers[0]['answer']]
        responder.reply('\n'.join(reply))
    else:
        responder.reply("Sorry😕, I couldn't find an answer to your question")
