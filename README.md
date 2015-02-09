<h1>Olset Backend/API Engineer Coding Challenge</h1>
API written for python/flask.
<h3>Usage</h3>
* api url: `http://clemon-olset.ngrok.com/api/1.0/<route>`
* sample curl:<br>
`$ curl -i -H "Content-Type: application/json" -X POST -d '{"sentence":"heyo, I want to go to San Deigo on January 22nd for 2 days"}' http://clemon-olset.ngrok.com/api/1.0/parse`

<h3>routes</h3>
**POST: /api/1.0/parse**
<p>input: sentence structured as a JSON object</p>
*example: `{'sentence':'heyo, I want to go to San Deigo on January 22nd for 2 days'}`*
<p>output: JSON object containing "dates", "durations", and "locations"</p>
*example: `{
            'dates' : ['01/22/16'],
            'durations' : ['2 days'],
            'locations' : ['San Diego']}`*

<br><br><br><br><br><br><br>
<h2>Thanks for your time!</h2>
[![Thanks for your time](http://img.youtube.com/vi/-UvvkWd_dR4/0.jpg)](http://youtu.be/-UvvkWd_dR4?t=3m10s)
