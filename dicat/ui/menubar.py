#import standard packages
import Tkinter
#import internal packages
import lib.multilanguage as MultiLanguage
import ui.datawindow as DataWindow

class SchedulerMenuBar(Tkinter.Menu):
    def __init__(self, parent):
        Tkinter.Menu.__init__(self, parent)
        # create an APPLICATION pulldown menu
        application_menu = Tkinter.Menu(self, tearoff=False)
        self.add_cascade(label=MultiLanguage.application_menu,underline=0, menu=application_menu)
        application_menu.add_command(label=MultiLanguage.application_setting, underline=1, command=self.app_settings)
        application_menu.add_separator()
        application_menu.add_command(label=MultiLanguage.application_quit, underline=1, command=self.quit_application)
        # create a CANDIDATE pulldown menu
        candidate_menu = Tkinter.Menu(self, tearoff=False)
        self.add_cascade(label=MultiLanguage.candidate_menu, underline=0, menu=candidate_menu)
        candidate_menu.add_command(label=MultiLanguage.candidate_add, command=self.add_candidate)
        candidate_menu.add_command(label=MultiLanguage.candidate_find, command=self.find_candidate)
        candidate_menu.add_command(label=MultiLanguage.candidate_update, command=self.update_candidate)
        candidate_menu.add_separator()
        candidate_menu.add_command(label=MultiLanguage.candidate_get_id, command=self.get_candidate_id)
        candidate_menu.add_separator()
        candidate_menu.add_command(label=MultiLanguage.candidate_exclude_include_toggle, command=self.exclude_candidate)
        # create a CALENDAR pulldown menu
        calendar_menu = Tkinter.Menu(self, tearoff=False)
        self.add_cascade(label=MultiLanguage.calendar_menu, underline=0, menu=calendar_menu)
        calendar_menu.add_command(label=MultiLanguage.calendar_new_appointment, command=self.open_calendar)
        # create a HELP pulldown menu
        help_menu = Tkinter.Menu(self, tearoff=0)
        self.add_cascade(label=MultiLanguage.help_menu, underline=0, menu=help_menu)
        help_menu.add_command(label=MultiLanguage.help_get_help, command=self.open_help)
        help_menu.add_command(label=MultiLanguage.help_about_window, command=self.about_application)

    def app_settings(self):
        #TODO implement app_settings()
        print 'running appsettings'
        pass

    def quit_application(self):
        #TODO implement quit_application()
        print 'running quit_application'
        self.quit()
        pass

    def open_calendar(self):
        #TODO implement open_calendar()
        print 'running open_calendar'
        pass

    def dicom_anonymizer(self):
        #TODO implement dicom_anonymizer()
        print 'running dicom anonymizer'
        pass

    def add_candidate(self):
        #TODO implement add_candidate()
        DataWindow.DataWindow(self, "new")
        print 'running add_candidate'
        pass

    def find_candidate(self):
        #TODO implement find_candidate()
        print 'running find_candidate'
        pass

    def update_candidate(self):
        #TODO implement update_candidate()
        print 'running update_candidate'
        pass

    def get_candidate_id(self):
        #TODO get_candidate_id()
        print 'running get_candidate_id'
        pass

    def exclude_candidate(self):  #need renaming
        #TODO exclude_candidate()
        print 'running incativate_candidate'
        pass

    def open_help(self):
        #TODO open_help()
        print 'running open_help'
        pass

    def about_application(self):
        #TODO about_application()
        print 'running about_application'
        pass