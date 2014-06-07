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

    $con->query("INSERT INTO dataReceived (StudyDate, PatientName, PatientID, InstitutionName, StudyInstanceUID, SeriesInstanceUID) 
    VALUES ('$argv[1]','$argv[2]','$argv[3]','$argv[4]','$argv[5]','$argv[6]')");

 

    $result = $con->query("SHOW TABLE STATUS WHERE `name`=\"dataReceived\"");

    $row=$result->fetch_array(MYSQLI_ASSOC);

    $last_entered_ID=$row["Auto_increment"]-1;
    $Server_file_id='NBRC'.'_'.rand(1,9999).'_'.$last_entered_ID;
   
 
    $con->query("INSERT INTO dataTransferred (Server_file_id, StudyDate, InstitutionName, StudyInstanceUID, SeriesInstanceUID) 
    VALUES ('$Server_file_id','$argv[1]','$argv[4]','$argv[5]','$argv[6]')");
    
    
    $con->query("INSERT INTO dataLogged (Center_file_id, StudyDate,PatientName, PatientID, InstitutionName, StudyInstanceUID, SeriesInstanceUID, Server_file_id) 
    VALUES ('$last_entered_ID','$argv[1]','$argv[2]','$argv[3]','$argv[4]','$argv[5]','$argv[6]','$Server_file_id')"); 
    
 
  echo $Server_file_id;
mysqli_close($con);  
?>
