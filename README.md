# Conversational-Interface-Project-master
Project 3 Conservational Interface

Group 2

Members: Jerry Xu, Daniel Wang, Jonathan Katz

Github Link: https://github.com/JerryXRQ/CS337_Project3

The packages necessary to run our code are included in the file requirements.txt. We included two videos that shows our code working with Rasa and Slack.



# Extra Tasks Completed
Rasa Interface:

We got Rasa to work on the user story on Canvas using our recipe functions. A demo video was recorded and included in our submission.
Note. while in the rasa directory, run `rasa train` `rasa run actions&` `rasa shell`. Found that `rasa run actions` does not terminate, so the & is necessary and the `rasa shell` should be entered when it seems `rasa run actions&` is no longer doing anything.

Slack Chatbot:

We deployed our code using the slack platform. The user can join our slack channel and ask the bot questions.

Substitution:

We add the feature to look up available substitutions as well as browse build-in terms and descriptors.

Additional Question Format：

In addition to the required question types, we also added support for vague "what is" questions and vague ingredient substitution questions.


# Work Distribution


### Jerry Xu:
Designed the interface and finished the required tasks

Wrote the user story and question format file

Connected the deployment to Slack and recorded the demo

### Daniel Wang:
Created the flow chart

Improved the interface

Completed the substitution extra task

### Jonathan Katz:
Got Rasa to work with our functions

Recorded the Rasa demo on sample user story on Canvas


# Demo videos

Rasa: https://youtu.be/6yV8GF1JN_Q

Slack: https://youtu.be/Enmb9fn3DkU

# Notes

Because Slack will revoke our access to the bot if we post the authorization code on Git, we will not include it in our submission. Please contact us if there are any questions regarding it.
