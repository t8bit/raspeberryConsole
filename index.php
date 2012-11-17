<?php
//find games
$games=array();
if ($handle = opendir('games-html')) {
    while (false !== ($entry = readdir($handle))) {
        if ($entry != "." && $entry != "..") {
           $games[]=$entry;
        }
    }
    closedir($handle);
}
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
	"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>
	<title>untitled</title>
	<meta http-equiv="content-type" content="text/html;charset=utf-8" />
	<meta name="generator" content="Geany 1.22" />
	<link rel="stylesheet" type="text/css" href="css/style.css" />
	<script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.0/jquery.min.js" type="text/javascript"></script>
	<script src="js/gears.js" type="text/javascript"></script>
	
</head>

<body onload='init();'>
	<p>Codebits 'Portable' Game Console</p>
	<?php foreach($games as $game): ?>
	<div class='game'><a href='games-html/<?php echo $game; ?>/index.html'>
		<img src='games-html/<?php echo $game; ?>/icon.png' width=100px height=100px alt='game to play'/>
		<?php echo $game; ?>
	</a></div>
	<?php endforeach;?>
	<div id='debug' ></div>
</body>

</html>
