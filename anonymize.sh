dcmdump -ml +P StudyDate +P PatientName +P PatientID +P InstitutionName +P StudyInstanceUID +P SeriesInstanceUID +P SOPInstanceUID -q $1 > /data/dataReceived/dump_anonymize.txt
#dcmdump -ml -q $1 > /data/dataReceived/dump.txt
#cat /data/dataReceived/dump.txt | while read line; do
 var=$(awk -F ' ' '{print $3}' /data/dataReceived/dump_anonymize.txt)
#done
var_1=($var);
#echo ${var_1[5]};
    StudyDate=${var_1[0]};
    PatientName=${var_1[1]};
    PatientID=${var_1[2]};
    InstitutionName=${var_1[3]};
    StudyInstanceUID=${var_1[4]};
    SeriesInstanceUID=${var_1[5]};
    SOPInstanceUID=${var_1[6]};
    
  #echo ${#StudyDate};${a:12:}
    StudyDate=${StudyDate:1:(${#StudyDate}-2)};
    PatientName=${PatientName:1:(${#PatientName}-2)};
    PatientID=${PatientID:1:(${#PatientID}-2)};
    InstitutionName=${InstitutionName:1:(${#InstitutionName}-2)};
    StudyInstanceUID=${StudyInstanceUID:1:(${#StudyInstanceUID}-2)};
    SeriesInstanceUID=${SeriesInstanceUID:1:(${#SeriesInstanceUID}-2)};
    SOPInstanceUID=${SOPInstanceUID:1:(${#SOPInstanceUID}-2)};

#Replace_Var=$(php generate_ID.php $StudyDate $PatientName $PatientID $InstitutionName $StudyInstanceUID $SeriesInstanceUID)
Replace_Var=$(php generate_ID_without_DB.php $StudyDate $PatientName $PatientID $InstitutionName $StudyInstanceUID $SeriesInstanceUID $SOPInstanceUID $2)
dcmodify -m "(0010,0010)=$Replace_Var" $1
