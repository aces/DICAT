<?php
    //echo "Test";
//    echo $argv[1];
    $con=new mysqli("localhost","root","ibrain123","ibrain");
// Check connection
    if ($con->connect_errno)
      {
      echo "Failed to connect to MySQL: " . $con->connect_errno;
      }

   // preg_match("/\[^\]/", $argv[6],$matches);

    $con->query("INSERT INTO dataTransferred (Server_file_id, StudyDate, InstitutionName, StudyInstanceUID, SeriesInstanceUID) 
    VALUES ('$argv[1]','$argv[2]','$argv[3]','$argv[4]','$argv[5]')");

 
/*
    $result = $con->query("SHOW TABLE STATUS WHERE `name`=\"dataReceived\"");

    $row=$result->fetch_array(MYSQLI_ASSOC);

    $last_entered_ID=$row["Auto_increment"]-1;
    $Center_file_id='NBRC'.'_'.rand(1,9999).'_'.$last_entered_ID;
    echo $Center_file_id;
  */  
  
  $Server_file_id=$argv[1];
  $pieces = explode("_", $Server_file_id);
  $Center_file_id=$pieces[2];

  $result=$con->query("select * from dataReceived where Center_file_id=$Center_file_id");
  $con->query("INSERT INTO dataLogged (Center_file_id, StudyDate,PatientName, InstitutionName, StudyInstanceUID, SeriesInstanceUID) 
    VALUES ('$argv[1]','$argv[2]','$argv[3]','$argv[4]','$argv[5]')"); 
    mysqli_close($con);  
?>
 
