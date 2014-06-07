 
#!/bin/bash
clear;
if [ "$(ls -A /data/dataReceived/incoming)" ]; then
      
      FILES=/data/dataReceived/incoming/*
      for f in $FILES
      do
	    if [[ $f != *.txt ]]||[[ $f != *.sh ]]
	    then
		  echo "Processing $f file..."
	      # dcmodify -m "(0010,0010)=Test" $f
		# source anonymize.sh $f
		#  source sortbystudy.sh $f
	    #fi
	
 		
		      if [[ $f != *.dcm ]]
		      then
			  rename=${f}.dcm
			  #echo $rename
			  mv $f $rename
			  
			  source sortbystudy.sh $rename
			  
		     else
			  source sortbystudy.sh $f
		      fi

	fi

      done

     rsync -vrtu /data/dataTemp/ /data/dataLogged/
      
      clear;
       
    action=$(yad --width 300 --entry --title "Anonymizer Choice" \
    --image=gnome-standby \
    --button="gtk-ok:0" \
    --text "Choose action:" \
    --entry-text \
    "Automatic Anonymizer" "Select Fields to Anonymize")
    
    
    #echo $action

    if [[ $action == *"Automatic Anonymizer"* ]]; then
          
      find /data/dataTemp/*/* -type d -print | while read d; do
	
	declare -i count_files=0;
	find $d -type f -print | while read f; do
	    
	    count_files=$(($count_files+1));
	    source anonymize.sh $f $count_files
	    echo "$f is found...anonymizing"
	    #$remove_file=${f}.bak
	   # echo "delete $f backup file..."
	   # rm $remove_file
	done
      done
      
      
       find /data/dataTemp/*/* -type d -print | while read d; do
	find $d -type f -print | while read f; do

	   if [[ $f == *.bak ]]
		      then
			    echo "delete $f backup file..."
			      rm $f
	    fi
	   
	done
      done
      
    
    else
	  declare -i count_study=0;
	  ls /data/dataTemp/| while read d; do
	 
	    count_study=$(($count_study+1));
	    action1=$(yad --width 500 --title="Anonymize Study $count_study : $d" --form --field="(0008,0080) InstitutionName:CHK" --field="(0008,0090) ReferringPhysicianName:CHK"  --field="Patient Name" --text="Please select the fields you want to remove from DICOM Header"  FALSE TRUE "Enter the Anonymizing ID for the Patient Name Field" --button="gtk-ok:0")

	    echo $action1;
	    
	#	    find /data/dataTemp/$d -type f -print | while read f; do
	#		source manual_anonymize.sh $f $action1
	#	    done
	    

		arr=$(echo $action1 | tr "|" "\n")
		
	       arr_val=($arr);
 	#       echo ${arr_val[0]};

		if [[ ${arr_val[0]} == *"TRUE"* ]]; then
			dcmodify -v -e "(0008,0080)" /data/dataTemp/$d/*/*.dcm
		fi

		
		if [[ ${arr_val[1]} == *"TRUE"* ]]; then
			dcmodify -v -e "(0008,0090)" /data/dataTemp/$d/*/*.dcm
		fi
		
		dcmodify -v -m "(0010,0010)=${arr_val[2]} " *.dcm
		
 		find /data/dataTemp/$d -type f -print | while read f; do
			dcmodify -v -m "(0010,0010)=${arr_val[2]} " $f
	        done	

	done	

       find /data/dataTemp/*/* -type d -print | while read d; do
	find $d -type f -print | while read f; do

	   if [[ $f == *.bak ]]
		      then
			    echo "delete $f backup file..."
			      rm $f
	    fi
	   
	done
      done
      

  
    fi
    
      
      rsync -vrtu /data/dataTemp/ /data/dataTransferred/
     rm -rf /data/dataTemp
      
      
      
#      for f in $FILES
#      do
#	    if [[ $f != *.txt ]]||[[ $f != *.sh ]]
#	    then
#		  echo "Processing $f file..."
#	      # dcmodify -m "(0010,0010)=Rajiv_Ayan" $f
#		# source anonymize.sh $f
#		 # source sortbystudy.sh $f
#	    fi
#	
 #     done
      
      
      
 #     for f in $FILES
  #    do
#	    if [[ $f == *.bak ]]
#	    then
#		  echo "delete $f backup file..."
#		  rm $f
#	    fi
#	
#     done

    #  rsync -vrtu /data/dataTemp/ /data/dataLogged/
else
    echo "No new study data received"
fi

