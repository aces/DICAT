#dcmdump -ml +P StudyDate +P PatientName +P PatientID +P InstitutionName +P StudyInstanceUID +P SeriesInstanceUID -q $1 > /data/dataReceived/dump.txt
#dcmdump -ml -q $1 > /data/dataReceived/dump.txt
#cat /data/dataReceived/dump.txt | while read line; do
dcmdump -ml +P StudyDate +P PatientName +P PatientID +P InstitutionName +P StudyInstanceUID +P SeriesInstanceUID -q $1 > /data/dataReceived/dump_sort_by_study.txt
#dcmdump -ml -q $1 > /data/dataReceived/dump.txt
#cat /data/dataReceived/dump.txt | while read line; do
 var=$(awk -F ' ' '{print $3}' /data/dataReceived/dump_sort_by_study.txt)
#done
var_1=($var);
#echo ${var_1[5]};
    StudyDate=${var_1[0]};
    Server_file_id=${var_1[1]};
    InstitutionName=${var_1[3]};
    StudyInstanceUID=${var_1[4]};
    SeriesInstanceUID=${var_1[5]};
      
  #echo ${#StudyDate};${a:12:}
    StudyDate=${StudyDate:1:(${#StudyDate}-2)};
    Server_file_id=${Server_file_id:1:(${#Server_file_id}-2)};
    InstitutionName=${InstitutionName:1:(${#InstitutionName}-2)};
    StudyInstanceUID=${StudyInstanceUID:1:(${#StudyInstanceUID}-2)};
    SeriesInstanceUID=${SeriesInstanceUID:1:(${#SeriesInstanceUID}-2)};

   # echo $Server_file_id;
    clear;
    cd /data
    
    if [ ! -d dataTemp ]; then
	mkdir dataTemp;
	echo "Creating Temporary Data Pool";
      fi
      cd dataTemp
   
    
	if [ ! -d $StudyInstanceUID ]; then
	mkdir $StudyInstanceUID;
	echo "New Study...Creating dedicated study directory..";
      fi
    

    
      

      cp -v $1 /data/dataTemp/$StudyInstanceUID
      echo "Moving the data file to Corresponding study category";
      
      
      
      
      cd /data/dataLogged
   
   
	if [ ! -d $StudyInstanceUID ]; then
	mkdir $StudyInstanceUID;
	echo "New Study...Creating dedicated study directory for data logging..";
      fi
   
      cp -v $1 /data/dataLogged/$StudyInstanceUID
      echo "Moving the data file to Corresponding study category for data logging";
      
      cd /data
   

#      php update_transfer_log_tables.php $Server_file_id $StudyDate $InstitutionName $StudyInstanceUID $SeriesInstanceUID
      
      
      