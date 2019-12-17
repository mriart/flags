<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<style>
body {
    font-family: "Arial";
	font-size: 150%;
}
</style>
</head>

<body>
Question {{i}}
<br>
<!--Cheat double_bracket cheat double_bracket-->
<br>
<img src="/img/{{flag}}">
<br><br>
<form action="/q" method="POST">
	<input type="hidden" name="quest" value={{q}}>
	<input type="radio" name="answer" value={{p0}} style="height:20px; width:20px"> {{p0_text}}
	<br><br>
	<input type="radio" name="answer" value={{p1}} style="height:20px; width:20px"> {{p1_text}}
	<br><br>
	<input type="radio" name="answer" value={{p2}} style="height:20px; width:20px"> {{p2_text}}
	<br><br>
	<input type="submit" value="Next" style="height:50px; width:150px">
</form> 
</body>
</html>
