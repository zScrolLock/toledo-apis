from fastapi import FastAPI # Router Dependency
from pydantic import (BaseModel, constr) # Base Model to Person Class
from enum import Enum
import datetime

router = FastAPI() # Route Loader
queue = []
treats = []

class Priority(str, Enum):
    P = 'P'
    N = 'N'

class Person(BaseModel):          
    name: constr(max_length=20)
    priority: Priority
    date: str = datetime.datetime.now().strftime("%x")
    treat: bool = False
    pos: int = None

@router.get("/queue")
async def listQueue():
    return {
        "message": "/queue - GET",
        "code": 200,
        "queue": queue
    }

@router.get("/queue/{id}")
async def getInfo(id: int):

    if not queue:
        return {
            "message": "/queue - GET - NOT FOUND",
            "code": 404,
        }
    else:
        try:
            return {
            "message": "/queue - GET",
            "code": 200,
            "person": queue[id]
            }
        except IndexError:
            return {
                "message": "/queue - GET - NOT FOUND",
                "code": 404
            }
    

@router.post("/queue")
async def queuePerson(person: Person):
    person.pos = len(queue)
    queue.append(person)

    return {
        "message": "queue - POST",
        "code": 200,
        "person": person
    }

@router.put("/queue")
async def updateQueue():

    if not queue:
        return {
            "message": "/queue - PUT - EMPTY QUEUE",
            "code": 204,
        }
    else:
        treats.append(queue.pop(0))

        for person in queue:
            person.pos = person.pos - 1

        return {
            "message": "/queue - PUT",
            "code": 200,
            "queue": queue
        }

@router.delete("/queue/{id}")
async def deleteQueue(id: int):
    
    if not queue:
        return {
            "message": "/queue - PUT - EMPTY QUEUE",
            "code": 204,
        }
    else:
        index = 0
        
        try:
            treats.append(queue.pop(id))
        except IndexError:
            return {
                "message": "/queue - PUT - NOT FOUND",
                "code": 404,
            }


        for person in queue:
            person.pos = index
            index+=1

        return {
            "message": "/queue - PUT",
            "code": 200,
            "queue": queue
        }


@router.put("/priority")
async def updateQueuePriority():

    if not queue:
        return {
            "message": "/priority - PUT - EMPTY QUEUE",
            "code": 204,
        }
    else:
        result = findPriority()
        print(result)
        if  result == -1:
            treats.append(queue.pop(0))
        else:
            for person in queue:
                if person.priority == "P":
                    person.pos = person.pos - 1

            try:
                treats.append(queue.pop(result))
            except IndexError:
                return {
                    "message": "/queue - PUT - NOT FOUND",
                    "code": 404
                }
                
        return {
            "message": "/queue - PUT",
            "code": 200,
            "queue": queue
        }

@router.get("/treats")
async def treatsPersons():

    for person in treats:
        person.treat = True

    return {
        "message": "/treats - GET",
        "code": 200,
        "atendidos": treats
    }

def findPriority():        
    for person in queue:
        if person.priority == "P":
            return person.pos


    return -1
