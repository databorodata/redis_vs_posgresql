from py2neo.ogm import GraphObject, Property
from py2neo import Graph
from pydantic import BaseModel

from app.config import NEO4J_PASS

graph = Graph("bolt://localhost:7687", auth=("neo4j", NEO4J_PASS))




class UserProfileResponse(BaseModel):
    my_coef: int
    his_coef: int


class UserProfile(GraphObject):
    __primarykey__ = "id"

    id = Property()
    my_coef = Property()
    his_coef = Property()


def create_user_profile(id: int, my_coef: int, his_coef: int):
    user_profile = UserProfile()
    user_profile.id = id
    user_profile.my_coef = my_coef
    user_profile.his_coef = his_coef
    graph.create(user_profile)



