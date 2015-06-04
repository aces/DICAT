#!/usr/bin/env python
# -*- coding: utf-8 -*-

# read language preference from appdata file
#from utilities import readappdata  #TODO replace and remove
#language = readappdata()[0]

language = "en"

if language == "fr":  #TODO make dynamic

    ######################  TOP LEVEL MENU BAR  ######################
    apptitle = u"Outils LORIS"
    #APPLICATION menu
    menuapplication = u"Application"
    settingapplication = u"Préferences"
    quitapplication = u"Quitter"
    #PROJECT menu
    #menuproject = u"Projet"    #TODO remove?
    #openproject = u"Ouvrir un projet"
    #modifyproject = u"Modifier le projet ouvert"
    #newproject = u"Créer un nouveau projet"
    #CANDIDATE menu
    menucandidate = "Candidat"
    addcandidate = u"Nouveau candidat"
    findcandidate = u"Trouver candidat"
    updatecandidate = u"Mettre à jour"
    excludecandidate = u"Exclure un candidat"
    getcandidateid = u"Obtenir l'identifiant d'un candidat"
    clearallfield = u"Effacer"
    #ANONYMIZER menu
    menuanonymizer = u"DICOM"
    #CALENDAR menu
    menucalendar = u"Calendrier"
    newappointment = u"Nouveau Rendez-vous"
    #HELP menu
    menuhelp = u"Aide"
    gethelp = u"Obtenir de l'aide"
    aboutwindow = u"A propos de ..."       
    ######################  PROJECT INFO PANE  #######################
    project_infopane = u"Informations"
    project_detailpane = u"Détails du Projet"
    visit_detailpane = u"Détails des Visites"
    projectname = u"Projet"
    projectstart = u"Début"
    projectend = u"Fin"
    targetrecruitment = u"Cible de recrutement"
    currentrecruitment = u"Recrutement actuel"
    totalvisit = u"Nombre de Visites"    
    ####################  MULTI-TAB DATA SECTION  #####################
    calendar_pane = u"Calendrier"
    candidate_pane = u"Candidats"
    
    
    labelcandidatetable = u"Faites un double-clic sur l'une des lignes pour remplir les champs ci-dessus"
    datatable_id = u"ID"
    datatable_firstname = u"Prénom"
    datatable_lastname = "Nom"
    datatable_dob = u"Date de Naissance"
    datatable_phone = u"Téléphone"
    datatable_address = u"Adresse"
    datatable_city = u"Ville"
    datatable_province = u"Province"
    datatable_country = u"Pays"
    datatable_postalcode = u"Code Postal"
    
    
    calendar_monday = u"Lundi"
    calendar_tuesday = u"Mardi"
    calendar_wednesday = u"Mercredi"
    calendar_thursday = u"Jeudi"
    calendar_friday = u"Vendredi"
    calendar_saturday = u"Samedi"
    calendar_sunday = u"Dimanche"
    calendar_january = u"Janvier"
    calendar_february = u"Février"
    calendar_march = u"Mars"
    calendar_april = u"Avril"
    calendar_may = u"Mai"
    calendar_june = u"Juin"
    calendar_jully = u"Juillet"
    calendar_august = u"Août"
    calendar_september = u"Septembre"
    calendar_october = u"Octobre"
    calendar_november = u"Novembre"
    calendar_december = u"Décembre"
    ################  COLUMN HEADER  ##################
    col_candidate = u"Candidat"
    col_visitlabel = u"Visite"
    col_when = u"Date/Heure"
    col_where = u"Endroit"
    col_status = u"Statut"
    
    ####################  STATUS  #####################
    status_active = "actif"
    status_tentative = "provisoire"
    
    #################  DATA WINDOWS  ##################
    schedulewindow_title ="Calendrier"
    candidatewindow_title = "Information du candidat"
    
    
    ##################  DIALOGBOX  ####################
    dialog_yes = "Oui"
    dialog_no = "Non"
    dialogtitle_confirm = "Veuillez confirmer!"
    dialogclose = "Vous êtes sur le point de fermer cette fenêtre sans sauvegarder!  Voulez-vous continuer?"
    
    candidate_firstname = "prénom"
        
elif language == "en":
    apptitle = "LORIS tools"
    #APPLICATION menu
    menuapplication = u"Application"
    settingapplication = u"Preferences"
    quitapplication = u"Quit"
    #PROJECT menu
    #menuproject = u"Project"   #TODO remove?
    #openproject = u"Open project"
    #modifyproject = u"Modify open project"
    #newproject = u"New project"    
    #CANDIDATE menu
    menucandidate = u"Candidate"
    addcandidate = u"New candidate"
    findcandidate = u"Find a candidate"
    updatecandidate = u"Update"
    excludecandidate = u"Exclude a candidate"
    getcandidateid = u"Get a canditate ID"
    clearallfield = u"Clear"
    #CALENDAR menu
    menucalendar = u"Calendar"
    newappointment = u"New appointment"
    #ANONYMIZER menu
    menuanonymizer = u"DICOM"
    #HELP menu
    menuhelp = u"Help"
    gethelp = u"Get some help"
    aboutwindow = u"About this..."
    ######################  PROJECT INFO PANE  #######################
    project_infopane = u"Informations"
    project_detailpane = u"Project Details"
    visit_detailpane = u"Visit Details"
    projectname = u"Project"
    projectstart = u"Start"
    projectend = u"End"
    targetrecruitment = u"Recruitment target"
    currentrecruitment = u"Current recruitment"
    totalvisit = u"Total number of Visits"    
    ####################  MULTI-TAB DATA SECTION  #####################
    calendar_pane = u"Calendar"
    candidate_pane = u"Candidates"
    labelcandidatetable = u"Double click on row to populate fields above"
    datatable_id = u"ID"
    datatable_firstname = u"First Name"
    datatable_lastname = "Last Name"
    datatable_dob = u"Date of Birth"
    datatable_phone = u"Phone"
    datatable_address = u"Address"
    datatable_city = u"City"
    datatable_province = u"Province"
    datatable_country = u"Country"
    datatable_postalcode = u"Postal Code"
    
    
    calendar_monday = u"Monday"
    calendar_tuesday = u"Tuesday"
    calendar_wednesday = u"Wednesday"
    calendar_thursday = u"Thursday"
    calendar_friday = u"Friday"
    calendar_saturday = u"Saturday"
    calendar_sunday = u"Sunday"
    calendar_january = u"January"
    calendar_february = u"February"
    calendar_march = u"Marc"
    calendar_april = u"April"
    calendar_may = u"May"
    calendar_june = u"June"
    calendar_jully = u"Jully"
    calendar_august = u"August"
    calendar_september = u"September"
    calendar_october = u"October"
    calendar_november = u"November"
    calendar_december = u"December"
    
    ################  COLUMN HEADER  ##################
    col_candidate = u"Candidate"
    col_visitlabel = u"Visit"
    col_when = u"Date/Time"
    col_where = u"Place"
    col_status = u"Status"  
    ####################  STATUS  #####################
    status_active = "active" 
    status_tentative = "tentative"
    
    #################  DATA WINDOWS  ##################
    schedulewindow_title ="Scheduler"
    candidatewindow_title = "Candidate information"
    
    
    ##################  DIALOGBOX  ####################
    dialog_yes = "Yes"
    dialog_no = "No"
    dialogtitle_confirm = "Please confirm!"
    dialogclose = "You are about to close this window without saving! \n\nDo you want to continue?"
