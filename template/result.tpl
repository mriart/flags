<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<style>
body {
    font-family: "Arial";
	font-size: 120%;
}
</style>
</head>

<body>
Score: {{score}} / {{num_questions}} <br>
Review: <br>
% for review in reviews:
    <img src="{{review[0]}}"> {{review[1]}} {{review[2]}}<br>
% end 
<br>
<a href="/q">Start again</a>
</body>
</html>
