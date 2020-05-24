from app.modules.common.controller import Controller


class QuestionTopicController(Controller):
    def create(self, data):
        pass

    def get(self):
        pass

    def update(self, object_id, data):
        pass

    def delete(self, object_id):
        pass

    def _parse_question_topic(self, data, question_topic=None):
        if question_topic is None:
            question_topic = QuestionTopic()
        if 'question_id' in data:
            try:
                question_topic.question_id = int(data['question_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'topic_id' in data:
            try:
                question_topic.topic_id = int(data['topic_id'])
            except Exception as e:
                print(e.__str__())
                pass
        return question_topic
