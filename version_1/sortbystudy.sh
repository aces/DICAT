#dcmdump -ml +P StudyDate +P PatientName +P PatientID +P InstitutionName +P StudyInstanceUID +P SeriesInstanceUID -q $1 > /data/dataReceived/dump.txt
#dcmdump -ml -q $1 > /data/dataReceived/dump.txt
#cat /data/dataReceived/dump.txt | while read line; do
dcmdump -ml +P StudyDate +P PatientName +P PatientID +P InstitutionName +P StudyInstanceUID +P SeriesInstanceUID +P SeriesDescription -q $1 > /data/dataReceived/dump_sort_by_study.txt
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
    SeriesDescription=${var_1[6]};
    
  #echo ${#StudyDate};${a:12:}
    StudyDate=${StudyDate:1:(${#StudyDate}-2)};
    Server_file_id=${Server_file_id:1:(${#Server_file_id}-2)};
    InstitutionName=${InstitutionName:1:(${#InstitutionName}-2)};
    StudyInstanceUID=${StudyInstanceUID:1:(${#StudyInstanceUID}-2)};
    SeriesInstanceUID=${SeriesInstanceUID:1:(${#SeriesInstanceUID}-2)};
    SeriesDescription=${SeriesDescription:1:(${#SeriesDescription}-2)};

   # echo $Server_file_id;
   # clear;
    cd /data
    
    if [ ! -d dataTemp ]; then
	mkdir dataTemp;
	echo "Creating Temporary Data Pool";
      fi
      
      cd /data/dataTemp
   
    echo $StudyInstanceUID 
	if [ ! -d $StudyInstanceUID ]; then
	mkdir $StudyInstanceUID;
	echo "New Study...Creating dedicated study directory..";
      fi
    

      cd $StudyInstanceUID 
      
      if [ ! -d $SeriesDescription ]; then
	mkdir $SeriesDescription;
	echo "New Pulse Sequence...Creating dedicated series directory..";
      fi
           
      
      

      cp -v $1 /data/dataTemp/$StudyInstanceUID/$SeriesDescription
      echo "Moving the data file to Corresponding study and sequence category";
      
      
      
      
      cd /data/dataLogged
   
   
	if [ ! -d $StudyInstanceUID ]; then
	mkdir $StudyInstanceUID;
	echo "New Study...Creating dedicated study directory for data logging..";
      fi
   
      cd $StudyInstanceUID 
      
      if [ ! -d $SeriesDescription ]; then
	mkdir $SeriesDescription;
	echo "New Pulse Sequence...Creating dedicated series directory for data logging..";
      fi
           
      
      

      cp -v $1 /data/dataTemp/$StudyInstanceUID/$SeriesDescription
      echo "Moving the data file to Corresponding study and sequence category";
            
      cd /data
   

#      php update_transfer_log_tables.php $Server_file_id $StudyDate $InstitutionName $StudyInstanceUID $SeriesInstanceUID
      
      
      