DROP TABLE IF EXISTS dataReceived;

DROP TABLE IF EXISTS dataLogged;     

       
DROP TABLE IF EXISTS dataTransferred;

       
       
       CREATE TABLE dataReceived(
         Center_file_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
         StudyDate VARCHAR(10),
	 PatientName VARCHAR(100),
	 PatientID VARCHAR(100),
	 InstitutionName VARCHAR(100),
	 StudyInstanceUID VARCHAR(100),
	 SeriesInstanceUID VARCHAR(100)
       );

       
       CREATE TABLE dataTransferred (
         Server_file_id VARCHAR(50) NOT NULL PRIMARY KEY,
         StudyDate VARCHAR(10),
	 InstitutionName VARCHAR(100),
	 StudyInstanceUID VARCHAR(100),
	 SeriesInstanceUID VARCHAR(100)
       );
  
  
  CREATE TABLE dataLogged (
         Center_file_id INT NOT NULL PRIMARY KEY,
         StudyDate VARCHAR(10),
	 PatientName VARCHAR(100),
	 PatientID VARCHAR(100),
	 InstitutionName VARCHAR(100),
	 StudyInstanceUID VARCHAR(100),
	 SeriesInstanceUID VARCHAR(100),  
	 Server_file_id VARCHAR(50) NOT NULL,	 
	 CONSTRAINT `FK_Server_file_id` FOREIGN KEY (`Server_file_id`) REFERENCES `dataTransferred` (`Server_file_id`)
       );