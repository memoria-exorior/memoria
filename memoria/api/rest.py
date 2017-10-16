import logging
import traceback

from flask import request
from flask_restplus import Api, Resource, reqparse, fields, abort
from mongoalchemy.exceptions import BadResultException


from memoria.config import settings
from memoria.database.model import Fact, create_fact, update_fact, delete_fact

log = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------
# rest api - initialisation


api = Api(version='1.0', title='Memoria Fact api',
          description='Manages a set of Fact resources.')

ns = api.namespace('fact/facts', description='Operations related to facts')


# -------------------------------------------------------------------------------------------------
# rest api - pagination support


pagination_arguments = reqparse.RequestParser()

pagination_arguments.add_argument('page', type=int, required=False, 
                                  default=1, help='Page number')

pagination_arguments.add_argument('per_page', type=int, required=False, 
                                  choices=[1, 10, 100, 1000], default=10,
                                  help='Results per page {error_msg}')


# -------------------------------------------------------------------------------------------------
# rest api - request/response models


fact = api.model('Fact', {
    'uuid': fields.String(readOnly=True, description='Unique identifier.'),
    'created_at': fields.DateTime(readOnly=True, description='Creation date.'),
    'modified_at': fields.DateTime(readOnly=True, description='Last modified date.'),
    'owner': fields.String(required=True, description='Owner identifier.'),
    'question': fields.String(required=True, description='Question.'),
    'answer': fields.String(required=True, description='Answer.'),
    'labels': fields.List(fields.String(
        required=False, description='Label'), required=False, description='Labels.')
})

pagination = api.model('A page of results', {
    'page': fields.Integer(description='Result page number.'),
    'pages': fields.Integer(description='Total number of result pages.'),
    'per_page': fields.Integer(description='Number of items per result page.'),
    'total': fields.Integer(description='Total number of results.'),
})

page_of_facts = api.inherit('Page of facts', pagination, {
    'items': fields.List(fields.Nested(fact))
})


# -------------------------------------------------------------------------------------------------
# rest api - routes


@ns.route('/')
class FactsCollection(Resource):
    """
    A collection of Facts.
    """

    @api.expect(pagination_arguments)
    @api.marshal_with(page_of_facts)
    def get(self):
        """
        Returns the paged list of Facts.
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)
        facts_query = Fact.query
        fact_page = facts_query.paginate(page, per_page, error_out=False)
        return fact_page

    @api.expect(fact)
    @api.marshal_with(fact)
    def post(self):
        """
        Creates a new Fact.

        NB: RESTwise the newly created Fact is also returned.
        """
        fact = create_fact(request.json)
        print("created fact: ", fact)
        return fact, 201


@ns.route('/<string:uuid>')
@api.response(404, 'Fact not found.')
class FactItem(Resource):
    """
    A single Fact.
    """

    @api.marshal_with(fact)
    def get(self, uuid):
        """
        Get the Fact.
        """
        try:
            return Fact.query.filter(Fact.uuid == uuid).one()
        except BadResultException:
            abort(404, "The fact '{}' could not be found.".format(uuid))

    @api.expect(fact)
    @api.response(204, 'Fact successfully updated.')
    def put(self, uuid):
        """
        Update the Fact.
        """
        try:
            data = request.json
            update_fact(uuid, data)
            return None, 204
        except BadResultException:
            abort(404, "The fact '{}' could not be found. Unable to update fact.".format(uuid))


    @api.response(204, 'Fact successfully deleted.')
    def delete(self, uuid):
        """
        Delete the Fact.
        """
        try:
            return delete_fact(uuid)
        except BadResultException:
            abort(404, "The fact '{}' could not be found. Unable to delete fact.".format(uuid))
        return None, 204


# -------------------------------------------------------------------------------------------------
# rest api - error handlers


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500


class NoResultFound(Exception):
    """No result was found where one was expected."""


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': 'A result was required but none was found.'}, 404

