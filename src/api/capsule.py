from flask_restx import Resource, Namespace

Capsule = Namespace('Capsule')

@Capsule.route('/')
class CapsuleMainAPI(Resource):
    def get(self):
        pass # read


@Capsule.route('/create')
class CapsuleCreateAPI(Resource):
    def post(self):
        pass # create
    

@Capsule.route('/<int:id>')
class CapsuleAPI(Resource):
    def put(self):
        pass # update

    def delete(self):
        pass # delete