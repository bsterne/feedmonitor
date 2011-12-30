<html>
<head>
<title>Mozilla - Feed Monitor</title>
<style type="text/css">
body {
	 font-family: arial;
   font-size: 70%;
}
#outer {
   width: 100%;
   margin: auto;
   text-align: center;
}
#inner {
   width: 95%;
   margin: auto;
   text-align: center;
}
td.toprow {
  background-color: #1B56B6;
  text-align:center;
  font-weight:600;
  color: #fff;
  border-bottom:2px solid #008;
  border-right:2px solid #008;
}
</style></head>
<body>
<div id="outer">
<h1 style="text-align:center;margin-top:0">Mozilla - Feed Monitor</h1>
<br/>
<div id="inner">
<?php
// set up variables for DB connection
$host = "";
$db = "";
$user = "";
$pass = "";

// establish DB connection
$link = mysql_connect($host, $user, $pass);
if (!$link) {
  die('Could not connect: ' . mysql_error());
}
$db_selected = mysql_select_db($db, $link);
if (!$db_selected) {
  die('Could not select $db: ' . mysql_error());
}

$sql = "SELECT * from alerts order by date_sent desc;";
$result = mysql_query($sql);

//alternate background color for non-special rows
$bgColor = "fff";

if ($myrow = mysql_fetch_array($result)) {
  echo "<table border=\"0\" cellpadding=\"3\" cellspacing=\"1\" width=\"100%\" style=\"border:1px solid #008;\">\n";
  echo "<tr><td class=\"toprow\">Subject</td><td class=\"toprow\">Link</td><td class=\"toprow\">Source</td><td class=\"toprow\">Date</td></tr>";
  do{
    print "<tr style=\"background-color:#".$bgColor."\">";
    $bgColor = ($bgColor == "ebebff") ? "fff" : "ebebff";
    printf("<td>%s</td><td><a href=\"%s\">%s</a></td><td>%s</td><td>%s</td>", $myrow["subject"], $myrow["link"], $myrow["link"], $myrow["source"], $myrow["date_sent"]);
    print "</tr>\n";
  }
  while ($myrow = mysql_fetch_array($result));
  echo "</table>\n";
}
?>
</div>
<body>
</html>
