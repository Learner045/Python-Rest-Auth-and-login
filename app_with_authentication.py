from flask import Flask, request
from flask_restful import Resource,Api,reqparse
from flask_jwt import JWT, jwt_required

from Authentication.security import authenticate, identity

app=Flask(__name__)
app.secret_key='abcdefg'
api=Api(app)

jwt=JWT(app,authenticate,identity)
#creates a new endpoint /auth ..request sens us username,pass..which is send to authenticate()
#auth endpoint  then returns  a JWT token, this token is then used for identification purpose of user
#identity() method is used to check if userid matches


items=[]

#http status codes: 200-ohk data returned successfully  404-not found 201-data created
# 202-accepted, when creation of obj is delayed and is done after latency behind the scnees
class Item(Resource):
    parser = reqparse.RequestParser()  # get request parset and set arguments to it
    parser.add_argument('price',
                        type=float,
                        required=True,  # no req should come through without having price as attribute
                        help="This field cannot be left blank!"
                        )

    @jwt_required() #we will need to authenticate before this REQ can take place
    def get(self,name):
        item=next(filter(lambda x: x['name']==name,items),None) #filter func returns list of matching items, next gives us 1st item
        return item, 200 if item else 404
    

    def post(self,name):
        if next(filter(lambda x: x['name']==name, items),None):
            return {"message":"item with {} elready exists ".format(name)},400
        else:
            data=request.get_json(force=True) #if JSON payload is not proper/body does not have JSON then this gives an err..to avoid err..use force
            item={'name':name, 'price':data['price']}
            items.append(item)
            return item


    def delete(self,name):
        global items #we need to specify this or else python will think we are trying to
        items=list(filter(lambda x: x['name']!=name,items)) #use items in parathensis before it is being declared
        return {"message":"item deleted"}


    def put(self,name):
        #we don't want item name to get changed so we let only some arguments(price) to come through and filter using parser
        #parser belongs to class Item
        data=Item.parser.parse_args() #only arguments which we want will come through payload

        item=next(filter(lambda x: x['name']==name,items),None)
        if item is None:
            item={'name':name, 'price':data['price']}
            items.append(item)
        else:
            item.update(data)
        return item



class ItemList(Resource):
    def get(self):
        return {'items':items}

api.add_resource(Item, '/item/<string:name>') #we are receiving name directly from url into our method
api.add_resource(ItemList, '/items')


app.run(port=5000, debug=True)