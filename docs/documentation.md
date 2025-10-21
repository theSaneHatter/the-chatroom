# the-chatroom documentation
The grand, offical documentation of the-chatroom 
## structure--how this thing is setup : 
### frontend : 
#### sending messages : 
- website gets message from user
- sends message via post request
#### receving messages : 
- website connects to server via websocket asap
- when there are new messages, websocket sends 'em and website displays 'em
### backend : 
- flask for managing web coms 
- when receve message via post request, flask (using flask socketio) broadcasts the message to all connected clients via sockets
> - *note: the client who is the sender gets the message also, and uses this feture to varaify that their message was sent*
> - *note: there is stuff added to the message oc eg uid*

## todo : 
### web-ui : 
- as we all know, the ui sucks, especally with the new lines and moble. 
> so you could make the input box expand vertically
- perhaps a markdown system 
- perhaps make message filtering 
- perhaps make encryption using asymmetric keys and signatures, could also allow smaler chat rooms if combined with filtering
### backend : 
- windows compatability 
>> might be some stuff on other compu that was never published for this, but big prob is with system calling for logs and stuff
>>shutil!
- nodeability from config file and embedded in messages/packets


 
