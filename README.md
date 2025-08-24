# the-chatroom
## tf this is
- this is a chatroom u can host from ur compu so people can chat using its web ui
- you shouldnt use this rn because its hella beta

## how do i use?
> its not really done yet, but...
### useage : 
- py main.py, then you can go to ur local network ip as should by hostname -I at port 5000, and chat. Others can chat too, and everyone will see the messages
- Would reccomend using from the stable branch, but everythings krazy rn

## structure--how this thing is setup : 
### frontend : 
#### sending : 
- website gets message from user
- sends message via post request
#### receving : 
- website connects to server via websocket asap
- when there are new messages, websocket sends 'em and website displays 'em
### backend : 
- flask for managing web coms 
- when receve message via post request, broadcasts the message to all connected clients via sockets
- *note: the client who is the sender gets the message also, and uses this feture to varaify that their message was sent*
- *note: there is stuff added to the message oc eg uid*

## todo : 
### web-ui : 
- as we all know, the ui sucks, especally with the new lines and moble. 
> so you could make the input box expand vertically
- perhaps a markdown system 
- perhaps make message filtering 
- perhaps make encryption using asymmetric keys and signatures, could also allow smaler chat rooms if combined with filtering
### backend : 
- jajaja we all know the prob with importing flask and breaking system packages and stuff for linux users. 
>> so make ts more like a flask app. 
- windows compatability 
>> might be some stuff on other compu that was never published for this, but big prob is with system calling for logs and stuff


