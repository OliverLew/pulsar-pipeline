<title>Python is awesome!</title>
<style>
h1 { font-size: 64px; }
</style>
<h1>Afternerd</h1>
<p>Congratulations! The HTTP Server is working!</p>

<?php
    echo "test";
    exec("ls -lart", $out, $ret);
    echo "<pre>return: $ret";
    echo PHP_EOL . 'output: ' . PHP_EOL;
    foreach ($out as $line) {
        echo $line . PHP_EOL;
    }
    echo "</pre>";
?>
