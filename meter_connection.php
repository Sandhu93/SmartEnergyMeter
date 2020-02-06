<?php
 define ('hostname','192.168.1.100');
 define ('username','root');
 define ('password','root');
 define ('databasename','meter');
 
 $connect = mysqli_connect(hostname,username,password,databasename);
 
 ?>