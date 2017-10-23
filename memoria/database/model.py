import uuid as uuid_gen

from memoria.database import db

# -------------------------------------------------------------------------------------------------
# fact model - operations


def create_fact(data):
    owner = data.get('owner')
    question = data.get('question')
    answer = data.get('answer')
    labels = data.get('labels')
    fact = Fact(owner, question, answer, labels)
    fact.save()
    return fact


def update_fact(fact_uuid, data):
    fact = Fact.query.filter(Fact.uuid == fact_uuid).one()
    fact.owner = data.get('owner')
    fact.question = data.get('question')
    fact.answer = data.get('answer')
    fact.labels = data.get('labels')
    fact.save()


def delete_fact(fact_uuid):
    fact = Fact.query.filter(Fact.uuid == fact_uuid).one()
    fact.remove()


# -------------------------------------------------------------------------------------------------
# fact model

class Fact(db.Document):
    """
    Fact Model
    """
    uuid = db.StringField()
    created_at = db.CreatedField()
    modified_at = db.ModifiedField()
    owner = db.StringField()
    labels = db.ListField(db.StringField())
    question = db.StringField()
    answer = db.StringField()

    def __init__(self, owner, question, answer, labels, uuid=None, *args, **kwargs):
        super(Fact, self).__init__(*args, **kwargs)
        if uuid is None:
            self.uuid = str(uuid_gen.uuid4())
        else:
            self.uuid = uuid
        self.owner = owner
        self.labels = labels
        self.question = question
        self.answer = answer

    def __repr__(self):
        return """<Fact
  uuid        : {}
  created_at  : {}
  modified_at : {}
  owner       : {}
  labels      : {}
  question    : {}
  answer      : {}
  >""".format(self.uuid, self.created_at, self.modified_at, self.owner,
              self.labels, self.question, self.answer)
