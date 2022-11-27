from fastapi import (FastAPI, Response, status) # Router Dependency
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

@router.get("/queue", status_code=200)
async def listQueue(response: Response):

    if not queue:
        response.status_code = status.HTTP_204_NO_CONTENT
        return {
            "message": "/queue - GET",
            "code": 204,
            "queue": queue
        }
    else:
        response.status_code = status.HTTP_200_OK
        return {
            "message": "/queue - GET",
            "code": 200,
            "queue": queue
        }

@router.get("/queue/{id}", status_code=200)
async def getInfo(id: int, response: Response):

    if not queue:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "message": "/queue/:id - GET - NOT FOUND",
            "code": 404,
        }
    else:
        try:
            response.status_code = status.HTTP_200_OK
            return {
            "message": "/queue/:id - GET",
            "code": 200,
            "person": queue[id]
            }
        except IndexError:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {
                "message": "/queue/:id - GET - NOT FOUND",
                "code": 404
            }
    

@router.post("/queue", status_code=201)
async def queuePerson(person: Person):
    person.pos = len(queue)
    queue.append(person)

    return {
        "message": "/queue - POST",
        "code": 201,
        "person": person
    }

@router.put("/queue", status_code=200)
async def updateQueue(response: Response):

    if not queue:
        response.status_code = status.HTTP_204_NO_CONTENT
        return {
            "message": "/queue - PUT - EMPTY QUEUE",
            "code": 204,
        }
    else:
        treats.append(queue.pop(0))

        for person in queue:
            person.pos = person.pos - 1

        response.status_code = status.HTTP_200_OK
        return {
            "message": "/queue - PUT",
            "code": 200,
            "queue": queue
        }

@router.delete("/queue/{id}", status_code=200)
async def deleteQueue(id: int, response: Response):
    
    if not queue:
        response.status_code = status.HTTP_204_NO_CONTENT
        return {
            "message": "/queue/:id - DELETE - EMPTY QUEUE",
            "code": 204,
        }
    else:
        index = 0
        
        try:
            treats.append(queue.pop(id))
        except IndexError:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {
                "message": "/queue/:id - DELETE - NOT FOUND",
                "code": 404,
            }


        for person in queue:
            person.pos = index
            index+=1

        response.status_code = status.HTTP_200_OK
        return {
            "message": "/queue/:id - DELETE",
            "code": 200,
            "queue": queue
        }


@router.put("/priority", status_code=200)
async def updateQueuePriority(response: Response):

    if not queue:
        response.status_code = status.HTTP_204_NO_CONTENT
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
                response.status_code = status.HTTP_404_NOT_FOUND
                return {
                    "message": "/priority - PUT - NOT FOUND",
                    "code": 404
                }
        
        response.status_code = status.HTTP_200_OK
        return {
            "message": "/priority - PUT",
            "code": 200,
            "queue": queue
        }

@router.get("/treats", status_code=200)
async def treatsPersons(response: Response):

    if not treats:
        response.status_code = status.HTTP_204_NO_CONTENT
        return {
            "message": "/treats - GET - EMPTY CONTENT",
            "code": 204,
            "atendidos": treats
        }
    else:
        for person in treats:
            person.treat = True

        response.status_code = status.HTTP_200_OK
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
