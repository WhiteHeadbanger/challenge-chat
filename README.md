# How to run

1. `pip install -r requirements`
2. `python -m src.app`
3. Use a Postman to send requests and receive responses

# Endpoints
* POST /register?<str:username>
* POST /login?<str:username>
* GET /logout
* DELETE /deleteaccount
* POST /friendrequest/send?<str:username>
* POST /friendrequest/handle?<str:username>&<str:accept>
* POST /pm/send?<str:username>&<str:message>
* GET /pm
* GET /room?<str:room_name>
* POST /room/create?<str:room_name>
* POST /room/invite?<str:room_name>&<str:username>
* POST /room/send?<str:room_name>&<str:message>

