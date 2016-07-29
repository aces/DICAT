#!/usr/bin/env python
# -*- coding: utf-8 -*-

#read language preference from appdata file
#from utilities import readappdata  #TODO replace and remove
#language = readappdata()[0]

language = "en" #TODO make dynamic

if language == "fr":
    ######################  TOP LEVEL MENU BAR  ######################
    app_title = u"Outils LORIS"
    #APPLICATION menu
    application_menu    = u"Application"
    application_setting = u"Préferences"
    application_quit    = u"Quitter"
    #PROJECT menu
    #menuproject   = u"Projet"    #TODO remove?
    #openproject   = u"Ouvrir un projet"
    #modifyproject = u"Modifier le projet ouvert"
    #newproject    = u"Créer un nouveau projet"
    #CANDIDATE menu
    candidate_menu   = u"Candidat"
    candidate_add    = u"Nouveau candidat"
    candidate_search = u"Trouver candidat"
    candidate_update = u"Mettre à jour"
    candidate_get_id = u"Obtenir l'identifiant d'un candidat"
    candidate_exclude_include_toggle = u"Inclure/Exclure un candidat"
    #clear_all_field = u"Effacer"
    #ANONYMIZER menu
    anonymizer_menu = u"DICOM"
    anonymizer_run  = u"Anonymizer"
    #CALENDAR menu
    calendar_menu = u"Calendrier"
    calendar_new_appointment = u"Nouveau Rendez-vous"
    #HELP menu
    help_menu     = u"Aide"
    help_get_help = u"Obtenir de l'aide"
    help_about_window = u"A propos de ..."
    ######################  PROJECT INFO PANE  #######################
    project_info_pane   = u"Projet"
    project_detail_pane = u"Détails du Projet"
    visit_detail_pane   = u"Détails des Visites"
    target_recruitment  = u"Cible de recrutement"
    current_recruitment = u"Recrutement actuel"
    project_name  = u"Projet"
    project_start = u"Début"
    project_end   = u"Fin"
    total_visit   = u"Nombre de Visites"
    ####################  MULTI-TAB DATA SECTION  #####################
    calendar_pane  = u"Calendrier"
    candidate_pane = u"Candidats"

    datatable_id    = u"ID"
    datatable_dob   = u"Date de Naissance"
    datatable_phone = u"Téléphone"
    datatable_city  = u"Ville"
    datatable_firstname   = u"Prénom"
    datatable_lastname    = u"Nom de famille"
    datatable_address     = u"Adresse"
    datatable_province    = u"Province"
    datatable_country     = u"Pays"
    datatable_postal_code = u"Code Postal"
    label_candidate_table = u"Faites un double-clic sur l'une des lignes " \
                            u"pour remplir les champs ci-dessus"

    calendar_monday    = u"Lundi"
    calendar_tuesday   = u"Mardi"
    calendar_wednesday = u"Mercredi"
    calendar_thursday  = u"Jeudi"
    calendar_friday    = u"Vendredi"
    calendar_saturday  = u"Samedi"
    calendar_sunday    = u"Dimanche"
    calendar_january   = u"Janvier"
    calendar_february  = u"Février"
    calendar_march     = u"Mars"
    calendar_april     = u"Avril"
    calendar_may       = u"Mai"
    calendar_june      = u"Juin"
    calendar_jully     = u"Juillet"
    calendar_august    = u"Août"
    calendar_september = u"Septembre"
    calendar_october   = u"Octobre"
    calendar_november  = u"Novembre"
    calendar_december  = u"Décembre"

    ################  COLUMN HEADER  ##################
    col_candidate  = u"Candidat"
    col_visitlabel = u"Visite"
    col_withwhom   = u"Avec qui"
    col_when   = u"Date/Heure"
    col_where  = u"Endroit"
    col_status = u"Statut"

    ####################  STATUS  #####################
    status_active    = u"actif"
    status_tentative = u"provisoire"
    #################  DATA WINDOWS  ##################
    data_window_title = u"DATA WINDOW" #TODO trouver un titre français
    ##################  DIALOGBOX  ####################
    # very not sure what to do about that section
    dialog_yes   = u"Oui"
    dialog_no    = u"Non"
    dialog_ok    = u"OK"
    dialog_close = u"Vous êtes sur le point de fermer cette fenêtre sans " \
                   u"sauvegarder!\n\nVoulez-vous continuer?"
    dialog_title_confirm   = u"Veuillez confirmer!"
    dialog_title_error     = u"Erreur"
    dialog_bad_dob_format  = u"La date de naissance doit être formatté en " \
                             u"AAAA-MM-JJ!"
    dialog_no_data_entered = u"Au moins un des champs doit être entré pour " \
                             u"chercher un candidat."
    warning_filters_set    = u"ATTENTION: des filtres sont en fonction. " \
                             u"Seuls les candidats correspondant aux filtres " \
                             u"sont montrés"
    dialog_candID_already_exists  = u"L'identifiant existe déjà!"
    dialog_missing_cand_info_schedul = u"Les champs 'Identifiant', 'Prénom', " \
                                       u"'Nom de famille', 'Sexe' et "         \
                                       u"'Date de naissance' sont requis!"
    dialog_missing_cand_info_IDmapper = u"Les champs 'Identifiant', "  \
                                        u"'Prénom', 'Nom de famille' " \
                                        u"et 'Date de naissance' sont requis!"
    ################  DATA WINDOW  ###################
    schedule_pane    = u"Calendrier"
    candidate_pane   = u"Candidat"
    candidate_dob    = u"Date de naissance (AAAA-MM-JJ)"
    candidate_phone  = u"Téléphone"
    candidate_pscid  = u"ID"
    candidate_status = u"Status"
    candidate_gender = u"Sexe"
    candidate_firstname = u"Prénom"
    candidate_lastname  = u"Nom de famille"

    schedule_visit_label  = u"Visite"
    schedule_visit_rank   = u"#"
    schedule_visit_status = u"Status"
    schedule_visit_when   = u"Date"
    schedule_optional     = u"Optionnel"
    schedule_no_visit_yet = u"Aucune visite de programmé pour ce candidat"

elif language == "en":
    app_title = u"LORIS tools"
    #APPLICATION menu
    application_menu    = u"Application"
    application_setting = u"Preferences"
    application_quit    = u"Quit"
    #PROJECT menu
    #menuproject   = u"Project"   #TODO remove?
    #openproject   = u"Open project"
    #modifyproject = u"Modify open project"
    #newproject    = u"New project"
    #CANDIDATE menu
    candidate_menu   = u"Candidate"
    candidate_add    = u"New candidate"
    candidate_search = u"Search:"
    candidate_update = u"Update"
    candidate_get_id = u"Get a canditate ID"
    candidate_exclude_include_toggle = u"Include/Exclude a candidate"
    #clear_all_field = u"Clear"
    #CALENDAR menu
    calendar_menu = u"Calendar"
    calendar_new_appointment = u"New appointment"
    #ANONYMIZER menu
    anonymizer_menu = u"DICOM"
    anonymizer_run  = u"Anonymizer"
    #HELP menu
    help_menu     = u"Help"
    help_get_help = u"Get some help"
    help_about_window = u"About this..."
    ######################  PROJECT INFO PANE  #######################
    project_info_pane   = u"Project Information"
    project_detail_pane = u"Project Details"
    visit_detail_pane   = u"Visit Details"
    target_recruitment  = u"Recruitment target"
    current_recruitment = u"Current recruitment"
    project_name  = u"Project"
    project_start = u"Start"
    project_end   = u"End"
    total_visit   = u"Total number of Visits"
    ####################  MULTI-TAB DATA SECTION  #####################
    calendar_pane   = u"Calendar"
    candidate_pane  = u"Candidates"
    datatable_id    = u"ID"
    datatable_dob   = u"Date of Birth"
    datatable_phone = u"Phone"
    datatable_city  = u"City"
    datatable_address  = u"Address"
    datatable_province = u"Province"
    datatable_country  = u"Country"
    datatable_firstname   = u"First Name"
    datatable_lastname    = u"Last Name"
    label_candidate_table = u"Double click on row to populate fields above"
    datatable_postal_code = u"Postal Code"

    calendar_monday    = u"Monday"
    calendar_tuesday   = u"Tuesday"
    calendar_wednesday = u"Wednesday"
    calendar_thursday  = u"Thursday"
    calendar_friday    = u"Friday"
    calendar_saturday  = u"Saturday"
    calendar_sunday    = u"Sunday"
    calendar_january   = u"January"
    calendar_february  = u"February"
    calendar_march     = u"Marc"
    calendar_april     = u"April"
    calendar_may       = u"May"
    calendar_june      = u"June"
    calendar_jully     = u"Jully"
    calendar_august    = u"August"
    calendar_september = u"September"
    calendar_october   = u"October"
    calendar_november  = u"November"
    calendar_december  = u"December"

    ################  COLUMN HEADER  ##################
    col_candidate  = u"Candidate"
    col_visitlabel = u"Visit"
    col_withwhom   = u"Whom"
    col_when   = u"Date/Time"
    col_where  = u"Place"
    col_status = u"Status"

    ####################  STATUS  #####################
    status_active    = u"active"
    status_tentative = u"tentative"

    #################  DATA WINDOWS  ##################
    data_window_title = u"Data Window"

    ##################  DIALOGBOX  ####################
    # very not sure what to do about that section
    dialog_yes   = u"Yes"
    dialog_no    = u"No"
    dialog_ok    = u"OK"
    dialog_close = u"You are about to close this window without saving!\n\n" \
                   u"Do you want to continue?"
    dialog_title_confirm   = u"Please confirm!"
    dialog_title_error     = u"Error"
    dialog_bad_dob_format  = u"Date of Birth should be in YYYY-MM-DD format!"
    dialog_no_data_entered = u"At least one of the fields needs to be entered " \
                             u"to search_event a candidate."
    warning_filters_set    = u"WARNING: filters are set. Only matching " \
                             u"candidates are shown."
    dialog_candID_already_exists  = u"Identifier already exists!"
    dialog_missing_cand_info_schedul = u"'Identifier', 'Firstname', "         \
                                       u"'Lastname', 'Date of Birth' and " \
                                       u"'Gender' fields are required!"
    dialog_missing_cand_info_IDmapper = u"'Identifier', 'Firstname', "     \
                                        u"'Lastname' and 'Date of Birth' " \
                                        u"fields are required!"

    ################  DATA WINDOW  ###################
    schedule_pane    = u"Calendar"
    candidate_pane   = u"Candidate"
    candidate_dob    = u"Date of Birth (YYYY-MM-DD)"
    candidate_phone  = u"Phone"
    candidate_pscid  = u"ID"
    candidate_status = u"Status"
    candidate_gender = u"Sex"
    candidate_firstname   = u"Firstname"
    candidate_lastname    = u"Lastname"
    schedule_visit_label  = u"Visit"
    schedule_visit_rank   = u"#"
    schedule_visit_status = u"Status"
    schedule_visit_when   = u"Date"
    schedule_optional     = u"Optional"
    schedule_no_visit_yet = u"No visit scheduled for that candidate yet"