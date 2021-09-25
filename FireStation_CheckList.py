try:
	from Tkinter import Entry, Frame, Label, StringVar
	from Tkconstants import *
except ImportError:
	from tkinter import *
	from tkinter import messagebox
	from MySQLdb import *
	from tkinter.filedialog import askopenfilename
	from PIL import Image, ImageTk
	import sys, random, math
	import time
	import datetime
	import re
	import os

class Placeholder_State(object):
        __slots__ = 'normal_color', 'normal_font', 'placeholder_text', 'placeholder_color', 'placeholder_font', 'contains_placeholder'

class SampleApp(Tk):
        def __init__(self, *args, **kwargs):
            Tk.__init__(self, *args, **kwargs)

            #self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")


            container = Frame(self)
            container.pack(side="top", fill="both", expand=True)
            container.grid_rowconfigure(0, weight=1)
            container.grid_columnconfigure(0, weight=1)

            self.winfo_toplevel().title("West Coast")

            self.frames = {}
            for F in (StartPage, LoginPage, Menu, MCVChecklist, FaultReporting, RecordsPage):
                page_name = F.__name__
                frame = F(parent=container, controller=self)
                self.frames[page_name] = frame


                frame.grid(row=0, column=0, sticky="nsew")

            self.show_frame("StartPage")

        def show_frame(self, page_name):

            frame = self.frames[page_name]
            frame.tkraise()


class StartPage(Frame):

        def __init__(self, parent, controller):
            Frame.__init__(self, parent)
            self.controller = controller

            self.canvas = Canvas(self,bg='#FFFFFF',width=500,height=500,scrollregion=(0,0,500,500))

            hbar = Scrollbar(self,orient=HORIZONTAL)
            hbar.pack(side=BOTTOM,fill=X)
            hbar.config(command = self.canvas.xview)
            vbar = Scrollbar(self,orient=VERTICAL)
            vbar.pack(side=RIGHT,fill=Y)
            vbar.config(command =self.canvas.yview)
            self.canvas.config(width=700,height=700)
            self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
            self.canvas.pack(side=LEFT,expand=True,fill=BOTH)

            bg_name = Image.open("C:/Users/User/Desktop/Final Drafts/station.jpeg")
            size = (700, 700)
            render = ImageTk.PhotoImage(bg_name)
            resized = bg_name.resize(size,Image.ANTIALIAS)
            render = ImageTk.PhotoImage(resized)

            background = Label(self, image = render)
            background.image = render
            img_window = self.canvas.create_window(0, 0, anchor=NW, window = background)

            self.headline = Label(self, text="WEST COAST MARINE MCV CHECKLIST", width=40, font=(20))
            head_btn_window = self.canvas.create_window(130, 10, anchor=NW, window = self.headline)

            self.enter_btn = Button(self, text="Enter", width=10, command=lambda: controller.show_frame("LoginPage"))
            self.enter_btn.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            enter_btn_window = self.canvas.create_window(305, 50, anchor=NW, window = self.enter_btn)



class LoginPage(Frame):

        def __init__(self, parent, controller):
            Frame.__init__(self, parent)
            self.controller = controller

            self.canvas = Canvas(self,bg='#FFFFFF',width=500,height=500,scrollregion=(0,0,500,500))

            self.connection = connect("localhost", "root", "", "firestationdb")

            hbar = Scrollbar(self,orient=HORIZONTAL)
            hbar.pack(side=BOTTOM,fill=X)
            hbar.config(command = self.canvas.xview)
            vbar = Scrollbar(self,orient=VERTICAL)
            vbar.pack(side=RIGHT,fill=Y)
            vbar.config(command =self.canvas.yview)
            self.canvas.config(width=700,height=700)
            self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
            self.canvas.pack(side=LEFT,expand=True,fill=BOTH)

            bg_name = Image.open("C:/Users/User/Desktop/Final Drafts/MCVfront.jpeg")
            size = (700, 700)
            render = ImageTk.PhotoImage(bg_name)
            resized = bg_name.resize(size,Image.ANTIALIAS)
            render = ImageTk.PhotoImage(resized)

            background = Label(self, image = render)
            background.image = render
            img_window = self.canvas.create_window(0, 0, anchor=NW, window = background)

            USERNAME = StringVar()
            PASSWORD = StringVar()

            self.title_lbl = Label(self, text="Please Login", width=10)
            title_lbl_window = self.canvas.create_window(20, 20, anchor=NW, window = self.title_lbl)

            self.username = Label(self, text="Username", width=10)
            username_window = self.canvas.create_window(50, 50, anchor=NW, window = self.username)

            self.password = Label(self, text="Password", width=10)
            password_window = self.canvas.create_window(50, 80, anchor=NW, window = self.password)

            self.userentry = Entry(self, textvariable=USERNAME, width=20)
            userentry_window = self.canvas.create_window(150, 50, anchor=NW, window = self.userentry)

            self.passentry = Entry(self, textvariable=PASSWORD, show="*", width=20)
            passentry_window = self.canvas.create_window(150, 80, anchor=NW, window = self.passentry)

            self.login_btn = Button(self, text="Login", width=10, command=lambda: self.save_pass_log(self.controller))
            #self.login_btn = Button(self, text="Enter", width=10, command=lambda: controller.show_frame("Menu"))
            login_btn_window = self.canvas.create_window(170, 110, anchor=NW, window = self.login_btn)


        def save_pass_log(self, control):
                self.controller = control
                try:
                        if self.connection:
                                nothing = None
                                cur = self.connection.cursor()

                                rows = 0
                                cur.execute("SELECT * FROM user_accounts")
                                results = cur.fetchall()

                                recordrow = []
                                recordcol = []

                                for row in results:
                                        recordcol = []
                                        for j in range(3):
                                                recordcol.append(row[j])
                                        recordrow.append(recordcol)

                                if (self.userentry.get() == recordrow[0][1]) and (self.passentry.get() == recordrow[0][2]):
                                        self.controller.show_frame("Menu")

                except:
                        messagebox.showinfo('Error', 'Wrong Username or password!')
                finally:
                        print("Welcome!")


class Menu(Frame):

        def __init__(self, parent, controller):
            Frame.__init__(self, parent)
            self.controller = controller

            self.canvas = Canvas(self,bg='#FFFFFF',width=500,height=500,scrollregion=(0,0,500,5000))

            hbar = Scrollbar(self,orient=HORIZONTAL)
            hbar.pack(side=BOTTOM,fill=X)
            hbar.config(command = self.canvas.xview)
            vbar = Scrollbar(self,orient=VERTICAL)
            vbar.pack(side=RIGHT,fill=Y)
            vbar.config(command =self.canvas.yview)
            self.canvas.config(width=700,height=700)
            self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
            self.canvas.pack(side=LEFT,expand=True,fill=BOTH)

            bg_name = Image.open("C:/Users/User/Desktop/Final Drafts/MCVside.jpeg")
            size = (700, 700)
            render = ImageTk.PhotoImage(bg_name)
            resized = bg_name.resize(size,Image.ANTIALIAS)
            render = ImageTk.PhotoImage(resized)

            background = Label(self, image = render)
            background.image = render
            img_window = self.canvas.create_window(0, 0, anchor=NW, window = background)

            self.heading = Label(self, text="WEST COAST APPLIANCES", width=30)
            heading_window = self.canvas.create_window(250, 10, anchor=NW, window = self.heading)

            self.mcv = Label(self, text="MCV:", width=15)
            mcv_window = self.canvas.create_window(10, 40, anchor=NW, window = self.mcv)

            self.mcv_checklist = Button(self, text="MCV Checklist", width=15, command=lambda: controller.show_frame("MCVChecklist"))
            mcv_checklist_window = self.canvas.create_window(10, 70, anchor=NW, window = self.mcv_checklist)

            self.mcv_records = Button(self, text="Past Records", width=15, command=lambda: controller.show_frame("RecordsPage"))
            mcv_records_window = self.canvas.create_window(10, 100, anchor=NW, window = self.mcv_records)
            

class MCVChecklist(Frame):

        db_name = "checklist.db"
        count = 0

        def __init__(self, parent, controller):
            Frame.__init__(self, parent)
            self.controller = controller
            # SQL Connection
            self.connection = connect("localhost", "root", "", "firestationdb")
            
            self.canvas = Canvas(self,bg='#FFFFFF',width=500,height=500,scrollregion=(0,0,1000,5000))

            hbar = Scrollbar(self,orient=HORIZONTAL)
            hbar.pack(side=BOTTOM,fill=X)
            hbar.config(command = self.canvas.xview)
            vbar = Scrollbar(self,orient=VERTICAL)
            vbar.pack(side=RIGHT,fill=Y)
            vbar.config(command =self.canvas.yview)
            self.canvas.config(width=700,height=700)
            self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
            self.canvas.pack(side=LEFT,expand=True,fill=BOTH)
            
            # personal particular
            self.date_label = Label(self, text="DATE", width=10)
            date_label_window = self.canvas.create_window(10, 10, anchor=NW, window = self.date_label)

            self.name_label = Label(self, text="NAME", width=10)
            name_label_window = self.canvas.create_window(10, 40, anchor=NW, window = self.name_label)

            self.rota_label = Label(self, text="ROTA", width=10)       
            rota_label_window = self.canvas.create_window(10, 70, anchor=NW, window = self.rota_label)

            self.regis_label = Label(self, text="SERIAL", width=10)      
            regis_label_window = self.canvas.create_window(10, 100, anchor=NW, window = self.regis_label)

            date_txt  = StringVar()
            name_txt  = StringVar()
            rota_txt  = StringVar()
            regis_txt = StringVar()

            self.date_en = Entry(self, textvariable=date_txt, width=20)
            date_en_window = self.canvas.create_window(100, 10, anchor=NW, window = self.date_en)

            self.name_en = Entry(self, textvariable=name_txt, width=20)
            name_en_window = self.canvas.create_window(100, 40, anchor=NW, window = self.name_en)

            self.rota_en = Entry(self, textvariable=rota_txt, width=20)
            rota_en_window = self.canvas.create_window(100, 70, anchor=NW, window = self.rota_en)

            self.regis_en = Entry(self, textvariable=regis_txt, width=20)
            regis_en_window = self.canvas.create_window(100, 100, anchor=NW, window = self.regis_en)

            self.save_btn = Button(self, text="Save", width=10, command=self.Saveinfo)
            self.save_btn.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            save_btn_window = self.canvas.create_window(250, 100, anchor=NW, window = self.save_btn)

            self.cancel_btn = Button(self, text="Cancel", command=lambda: controller.show_frame("Menu"), width=10)
            self.cancel_btn.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            cancel_btn_window = self.canvas.create_window(350, 100, anchor=NW, window = self.cancel_btn)

            # serial numbers
            sizex = 10 
            sizey = 180
            yaxis = 180
            posx = 0
            posy = 0

            serials = []
            serialName = ["S/N", "A", "1", "2", "3", "4", "5", "B", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "C", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "D", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

            items = []
            itemsName = ["ITEMS FOR INSPECTION", "ENGINE COMPARTMENT", "Check Engine (OBM)", "Check 2T Oil (Container & Cable)", "Check Fuel Valve (Secondary)", "Check Cable & Wiring", "Check Battery Switch & Compartment", "INTERIOR", "Check Upholstery/Seats/Fans/Windows", "Check Steering/Gears/Throttle/Kill Switch Knob", "Test Steering Turn: Port/Starboard/Mid-Ship", "Test Gears Engage: Fwd/Astern/Neutral", "Check All Switches In Working Condition", "Check For OBM Tell Tale Sign Of Engine", "Check For Navigational Lights & All Other Lights", "Check Analogue Meter Gauge & Digital Tachometer", "Check Horn", "Check Fuel Valve (Primary), Check Fuel Level - Forward & Aft Tank", "Check Comms Equipment: VHF/Matra/PA System", "Check Navigational System: Radar/Echosounder/GPS", "Check Availability Of GPS1 CHART/SPI/TT", "Check Availability Of Medical Box And Its Condition", "Check Pressure & Expiry Date Of Fire Extinguisher", "Look For Sign Of Leakage/Flooding", "EXTERIOR", "General Body Condition & Paint Work", "Check Rubber Fenders Trimming Condition", "Check Railing & Fenders/LifeBuoys In Good Condition", "Check All Lights In Good & Working Condition", "Check PA System And Siren", "Check Radar Antenna & Lightning Arrestor", "Check Bilge Pumps In Good/Working Condition", "Fresh Water Pump In Good/Working Condition", "Check Presence of Anchor/Chain/Ropes", "Check Prescence Of Boats Hook", "Check Wipers & CVS", "OTHERS", "Listen For Unusual Knocks/Sounds", "Check The Function Of Meters", "Wash Vessel Exterior", "Clean Interior/Door Closed", "Forward Fuel Tank Level", "Aft Fuel Tank Level", "Switch Off Ignition & All Lights", "All OBM Engine Trim Up", "Close Windows", "Check Vessels Battery Connection"]

            del serials[:]
            del items[:]

            for i in range(47):
                serials.append(Label(self, text=serialName[i], width=10))
                items.append(Label(self, text=itemsName[i], width=50))

                if (i == 7):
                        yaxis = 210
                elif (i == 24):
                        yaxis = 240
                elif (i == 36):
                        yaxis = 270

                check_window = self.canvas.create_window(sizex, yaxis + (i * 30), anchor=NW, window = serials[i])
                items_window = self.canvas.create_window(100, yaxis + (30*i), anchor=NW, window = items[i])


            # check box
            self.checklb = Label(self, text="STATUS", width=10)
            check_windowlb = self.canvas.create_window(470, 180, anchor=NW, window = self.checklb)

            self.remarks = Label(self, text="REMARKS", width=25)
            remarks_window = self.canvas.create_window(560, 180, anchor=NW, window = self.remarks)
            
            # Initial checkbox Value (Set Default)
            yaxis = 240

            self.CheckVar = []
            self.RmTxt = []

            self.faultreports = []
            faultreportNames = ["Report Fault A1", "Report Fault A2", "Report Fault A3", "Report Fault A4", "Report Fault A5", "Report Fault B1", "Report Fault B2", "Report Fault B3", "Report Fault B4", "Report Fault B5", "Report Fault B6", "Report Fault B7", "Report Fault B8", "Report Fault B9", "Report Fault B10", "Report Fault B11", "Report Fault B12", "Report Fault B13", "Report Fault B14", "Report Fault B15", "Report Fault B16", "Report Fault C1", "Report Fault C2", "Report Fault C3", "Report Fault C4", "Report Fault C5", "Report Fault C6", "Report Fault C7", "Report Fault C8", "Report Fault C9", "Report Fault C10", "Report Fault C11", "Report Fault D1", "Report Fault D2", "Report Fault D3", "Report Fault D4", "Report Fault D5", "Report Fault D6", "Report Fault D7", "Report Fault D8", "Report Fault D9", "Report Fault D10"]

            # Database Entry
            DataBaseName = []
            self.DataBaseNameArray = ["check_engine_obm_tbl", "check_2t_oil_container_and_cable_tbl", "check_fuel_valve_secondary_tbl", "check_cable_and_wiring_tbl", "check_battery_switch_and_compartment_tbl", "check_upholstery_seats_fans_windows_tbl", "check_steering_gears_throttle_kill_switch_knob_tbl", "test_steering_turn_port_starboard_midship_tbl", "test_gears_engage_fwd_astern_neutral_tbl", "check_all_switches_in_working_condition_tbl", "check_for_obm_tell_tale_sign_of_engine_tbl", "check_for_navigational_lights_and_all_other_lights_tbl", "check_analogue_meter_gauge_and_digital_tachometer_tbl", "check_horn_tbl", "check_fuel_valve_primary_check_fuel_level_forward_and_aft_tank_t", "check_comms_equipment_vhf_matra_pa_system_tbl", "check_navigational_system_radar_echosounder_gps_tbl", "check_availability_of_gps1_chart_spi_tt_tbl", "check_availability_of_medical_box_and_its_condition_tbl", "check_pressure_and_expiry_date_of_fire_extinguisher_tbl", "look_for_sign_of_leakage_and_flooding_tbl", "general_body_condition_and_paint_work_tbl", "check_rubber_fenders_trimming_condition_tbl", "check_railing_and_fenders_and_lifebuoys_in_good_condition_tbl", "check_all_lights_in_good_and_working_condition_tbl", "check_pa_system_and_siren_tbl", "check_radar_antenna_and_lightning_arrestor_tbl", "check_bilge_pumps_in_good_and_working_condition_tbl", "fresh_water_pump_in_good_working_condition_tbl", "check_presence_of_anchor_chain_ropes_tbl", "check_prescence_of_boats_hook_tbl", "check_wipers_and_cvs_tbl", "listen_for_unusual_knocks_and_sounds_tbl", "check_the_function_of_meters_tbl", "wash_vessel_exterior_tbl", "clean_interior_door_closed_tbl", "forward_fuel_tank_level_tbl", "aft_fuel_tank_level_tbl", "switch_off_ignition_and_all_lights_tbl", "all_obm_engine_trim_up_tbl", "close_windows_tbl", "check_vessels_battery_connection_tbl"]

            self.checkrecords = []
            checkrecordsArray = ["Record A1", "Record A2", "Record A3", "Record A4", "Record A5", "Record B1", "Record B2", "Record B3", "Record B4", "Record B5", "Record B6", "Record B7", "Record B8", "Record B9", "Record B10", "Record B11", "Record B12", "Record B13", "Record B14", "Record B15", "Record B16", "Record C1", "Record C2", "Record C3", "Record C4", "Record C5", "Record C6", "Record C7", "Record C8", "Record C9", "Record C10", "Record C11", "Record D1", "Record D2", "Record D3", "Record D4", "Record D5", "Record D6", "Record D7", "Record D8", "Record D9", "Record D10"]
            
            cur = self.connection.cursor()

            try:
                for i in range (42):
                    self.CheckVar.append(IntVar(value = 0))     
                    self.check = Checkbutton(self, variable = self.CheckVar[i], width=7)
                    self.check.configure(width = 7, activebackground = "#33B5E5", relief = FLAT)

                    self.RmTxt.append(StringVar())
                    self.remark = Entry(self, textvariable = self.RmTxt[i], width=30)

                    self.faultreports.append(Button(self, text = faultreportNames[i], width=20, command=lambda a=self.DataBaseNameArray[i]: self.Faultinfo(self.controller, a)))
                    self.faultreports[i].configure(width = 20, activebackground = "#33B5E5", relief = FLAT)

                    self.checkrecords.append(Button(self, text= checkrecordsArray[i], width=20, command=lambda b=self.DataBaseNameArray[i]: self.ImageRecords(self.controller, b)))
                    self.checkrecords[i].configure(width = 20, activebackground = "#33B5E5", relief = FLAT)


                    if (i == 5):
                        yaxis = 300
                    elif (i == 21):
                        yaxis = 360
                    elif (i == 32):
                        yaxis = 420
                    
                    check_window = self.canvas.create_window(470, yaxis + (i * 30), anchor=NW, window = self.check)
                    remark_window = self.canvas.create_window(560, yaxis + (i * 30), anchor=NW, window = self.remark)
                    faultreports_window = self.canvas.create_window(760, yaxis + (i * 30), anchor=NW, window = self.faultreports[i])
                    checkrecords_window = self.canvas.create_window(920, yaxis + (i * 30), anchor=NW, window = self.checkrecords[i])
                    sql = "SELECT * FROM " + self.DataBaseNameArray[i]
                    cur.execute(sql)
                    results = cur.fetchall()
                    for row in results:
                        if row[9] == "Saved":
                            self.faultreports[i].configure(width = 20, activebackground = "#33B5E5", relief = FLAT, bg='red') 
            except:
                messagebox.showinfo("SDFSDF")
            finally: 
                print("Load SQL and paint red button if there's record not completed")


                    
        def Saveinfo(self):
            time.strftime('%x %X')
            self.save()        
            self.clear()

        def clear(self):
            self.date_en.delete(0, 'end')
            self.name_en.delete(0, 'end')
            self.rota_en.delete(0, 'end')
            self.regis_en.delete(0, 'end')

            # check_del
            for i in range(42):
                self.CheckVar[i].set(0)

            for i in range(42):
                self.RmTxt[i].set('')


        def save(self):

            if self.connection:
                time.strftime('%Y-%m-%d %H:%M:%S')
                nothing = None
                print("DB Connection started.")
                try:
                    cur = self.connection.cursor()
                    #sql = "INSERT INTO checklisttbl (SN, Date, Name, ROTA) VALUES (%s, %s, %s, %s)", (nothing,nothing,"JLJJ","T0004")
                    cur.execute("INSERT INTO checklist_tbl (DATE, NAME, ROTA, REG, check_1, check_2, check_3, check_4, check_5, check_6, check_7, check_8, check_9, check_10, check_11, check_12, check_13, check_14, check_15, check_16, check_17, check_18, check_19, check_20, check_21, check_22, check_23, check_24, check_25, check_26, check_27, check_28, check_29, check_30, check_31, check_32, check_33, check_34, check_35, check_36, check_37, check_38, check_39, check_40, check_41, check_42, rm_1, rm_2, rm_3, rm_4, rm_5, rm_6, rm_7, rm_8, rm_9, rm_10, rm_11, rm_12, rm_13, rm_14, rm_15, rm_16, rm_17, rm_18, rm_19, rm_20, rm_21, rm_22, rm_23, rm_24, rm_25, rm_26, rm_27, rm_28, rm_29, rm_30, rm_31, rm_32, rm_33, rm_34, rm_35, rm_36, rm_37, rm_38, rm_39, rm_40, rm_41, rm_42) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (time.strftime('%Y-%m-%d %H:%M:%S'), self.name_en.get(), self.rota_en.get(), self.regis_en.get(), \
                        self.CheckVar[0].get(), self.CheckVar[1].get(), self.CheckVar[2].get(), self.CheckVar[3].get(), self.CheckVar[4].get(), self.CheckVar[5].get(), self.CheckVar[6].get(), self.CheckVar[7].get(), self.CheckVar[8].get(), self.CheckVar[9].get(), self.CheckVar[10].get(), self.CheckVar[11].get(), self.CheckVar[12].get(), self.CheckVar[13].get(), self.CheckVar[14].get(), self.CheckVar[15].get(), self.CheckVar[16].get(), self.CheckVar[17].get(), self.CheckVar[18].get(), self.CheckVar[19].get(), self.CheckVar[20].get(), self.CheckVar[21].get(), self.CheckVar[22].get(), self.CheckVar[23].get(), self.CheckVar[24].get(), self.CheckVar[25].get(), self.CheckVar[26].get(), self.CheckVar[27].get(), self.CheckVar[28].get(), self.CheckVar[29].get(), self.CheckVar[30].get(), self.CheckVar[31].get(), self.CheckVar[32].get(), self.CheckVar[33].get(), self.CheckVar[34].get(), self.CheckVar[35].get(), self.CheckVar[36].get(), self.CheckVar[37].get(), self.CheckVar[38].get(), self.CheckVar[39].get(), self.CheckVar[40].get(), self.CheckVar[41].get(), self.RmTxt[0].get(), self.RmTxt[1].get(), self.RmTxt[2].get(), self.RmTxt[3].get(), self.RmTxt[4].get(), self.RmTxt[5].get(), self.RmTxt[6].get(), self.RmTxt[7].get(), self.RmTxt[8].get(), self.RmTxt[9].get(), self.RmTxt[10].get(), self.RmTxt[11].get(), self.RmTxt[12].get(), self.RmTxt[13].get(), self.RmTxt[14].get(), self.RmTxt[15].get(), self.RmTxt[16].get(), self.RmTxt[17].get(), self.RmTxt[18].get(), self.RmTxt[19].get(), self.RmTxt[20].get(), self.RmTxt[21].get(), self.RmTxt[22].get(), self.RmTxt[23].get(), self.RmTxt[24].get(), self.RmTxt[25].get(), self.RmTxt[26].get(), self.RmTxt[27].get(), self.RmTxt[28].get(), self.RmTxt[29].get(), self.RmTxt[30].get(), self.RmTxt[31].get(), self.RmTxt[32].get(), self.RmTxt[33].get(), self.RmTxt[34].get(), self.RmTxt[35].get(), self.RmTxt[36].get(), self.RmTxt[37].get(), self.RmTxt[38].get(), self.RmTxt[39].get(), self.RmTxt[40].get(), self.RmTxt[41].get()))
                    
                    self.connection.commit()
                    messagebox.showinfo('Success', 'Record saved...')
                except:
                    messagebox.showinfo('Error', 'Error in data entry...')
                finally:
                    self.clear()
                    #self.connection.close()


        def Faultinfo(self, control, DataBaseName):

            print("Open New Window ")
            print(DataBaseName)
            self.controller = control
            self.window = Toplevel(self)
            
            #self.connection = connect("localhost", "root", "", "firestationdb")

            self.canvas = Canvas(self.window, bg='#FFFFFF',width=500,height=500,scrollregion=(0,0,1000,5000))
                # Declare fname once only whenever Fault info is clicked
            nothing = None
            self.fname = [nothing, nothing, nothing, nothing, nothing]
            
            hbar = Scrollbar(self.window,orient=HORIZONTAL)
            hbar.pack(side=BOTTOM,fill=X)
            hbar.config(command = self.canvas.xview)
            vbar = Scrollbar(self.window,orient=VERTICAL)
            vbar.pack(side=RIGHT,fill=Y)
            vbar.config(command =self.canvas.yview)
            self.canvas.config(width=700,height=700)
            self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
            self.canvas.pack(side=LEFT,expand=True,fill=BOTH)

            # first image
            self.heading = Label(self.window, text = DataBaseName, width = 50)
            heading_window = self.canvas.create_window(10, 10, anchor=NW, window = self.heading)

            self.back_btn = Button(self.window, text="Back", command=lambda: self.controller.show_frame("Menu"), width=(10))
            self.back_btn.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            back_btn__window = self.canvas.create_window(370, 10, anchor=NW, window = self.back_btn)

            self.ImgLabel = Label(self.window, text="Image:", width=(10))
            ImgLabel_window = self.canvas.create_window(10, 40, anchor=NW, window = self.ImgLabel)

            self.descriptionlabel = Label(self.window, text="Description:", width=10)
            descriptionlabel_window = self.canvas.create_window(10, 350, anchor=NW, window = self.descriptionlabel)

            self.description_1 = Text(self.window, height= 6, width=60, bg="yellow")
            description_1_window = self.canvas.create_window(10, 380, anchor=NW, window = self.description_1)

            self.rectificationlabel = Label(self.window, text="Rectification", width=10)
            rectificationlabel_window = self.canvas.create_window(10, 500, anchor=NW, window = self.rectificationlabel)

            self.rectification_1 = Text(self.window, height= 6, width=60, bg="red")
            rectification_1_window = self.canvas.create_window(10, 530, anchor=NW, window = self.rectification_1)
            
            self.browse_button = Button(self.window, text="Browse", command=self.load_file, width=10)
            self.browse_button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            browse_btn_window = self.canvas.create_window(10, 650, anchor=NW, window = self.browse_button)

            self.completed_button = Button(self.window, text="Complete", command=lambda a = DataBaseName: self.completeSQL(a), width=10, bg="light green")
            self.completed_button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            completed_btn_window = self.canvas.create_window(415, 650, anchor=NW, window = self.completed_button)

            
            self.save_button = Button(self.window, text="Save", command=lambda a = DataBaseName: (self.save_file(a)), width=10)
            #self.save_button = Button(self.window, text="Save", command=lambda a = "faultreport_tbl": self.save_file(a), width=10)
            self.save_button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            save_btn_window = self.canvas.create_window(100, 650, anchor=NW, window = self.save_button)

            self.delete_button = Button(self.window, text="Delete", command=lambda a = DataBaseName: self.del_file(a), width=10, bg="red")
            self.delete_button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            delete_btn_window = self.canvas.create_window(190, 650, anchor=NW, window = self.delete_button)

            self.count = 0
            self.img = [] 

            if self.connection:
                # Select Query Example :- Selecting data from the table.
                cursor = self.connection.cursor()
                # This is to prove that the connection to the server is "Established".
                print("DB Connection was a great success...")

                try :
                    sql = "SELECT * FROM " + DataBaseName
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    for row in results:
                        if (row[9] != "Completed") :
                            for i in range (2 , 7):
                                if row[i] != None:
                                    print(row[i])
                                    load = Image.open(row[i])
                                    render = ImageTk.PhotoImage(load)
                                    size = (220, 250)
                                    resized = load.resize(size,Image.ANTIALIAS)
                                    render = ImageTk.PhotoImage(resized)

                                    # labels can be text or images
                                    self.img = Label(self.window, image=render)
                                    self.img.image = render
                                    img_window = self.canvas.create_window(10 + ( (i - 2) * 220), 80, anchor=NW, window = self.img)

                            self.description_1.insert("0.0",row[7])
                            self.rectification_1.insert("0.0",row[8])
                    
                except:
                    messagebox.showinfo('Error', 'Search in data entry...')
                finally:
                    print("Query Over")

               

        def load_file(self):
            # Open browser to get path
            
            
            self.fname[self.count] = askopenfilename(filetypes=(("JPG","*.jpg"),
                                               ("Template files", "*.tplate"),
                                               ("HTML files", "*.html;*.htm"),
                                               ("All files", "*.*") ))
         
            load = Image.open(self.fname[self.count])
            render = ImageTk.PhotoImage(load)
            size = (220, 250)
            resized = load.resize(size,Image.ANTIALIAS)
            render = ImageTk.PhotoImage(resized)

            if (self.count < 5):
                self.img.append(Label(self.window, image = render))
                # labels can be text or images
                self.img[self.count].image = render
                #self.img.place(x=10, y = 80)
                img_window = self.canvas.create_window(10 + (self.count * 220), 80, anchor = NW, window = self.img[len(self.img) - 1])

                self.count = self.count + 1 

        def save_file(self, DataBaseName) :
            index = 0

            try:
                if self.connection:
                    nothing = None
                    cur = self.connection.cursor()
                    rows = 0
                    cur.execute("SELECT * FROM " + DataBaseName)
                    results = cur.fetchall()
                    for row in results:
                        rows = rows + 1
                    cur.execute("INSERT INTO " + DataBaseName + " (SN, Date, ImageFile, Image2, Image3, Image4, Image5, Description, Rectification, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (str(rows + 1), time.strftime('%Y-%m-%d %H:%M:%S'), self.fname[0], self.fname[1], self.fname[2], self.fname[3], self.fname[4], self.description_1.get("1.0",END), self.rectification_1.get("1.0",END), "Saved"))

                    cur.execute("SELECT * FROM " + DataBaseName)
                    results = cur.fetchall()
                    for row in results:
                    	if row[9] != "Completed":
                    		index = self.DataBaseNameArray.index(DataBaseName)
                    		self.faultreports[index].configure(width = 20, activebackground = "#33B5E5", relief = FLAT, bg='red')

                    self.connection.commit()
                    messagebox.showinfo('Success', 'Record saved...')

            except:
                messagebox.showinfo('Error', 'Error in data entry...')
            finally:
                print("Uploaded")
                    		


        def del_file(self, DataBaseName) :

            for i in range (self.count):
                self.img[i].destroy()
            self.img = []
            self.description_1.delete('1.0', END)
            self.rectification_1.delete('1.0', END)

            try:
                if self.connection:
                    cur = self.connection.cursor()
                    rows = 0
                    result = cur.execute("SELECT * FROM " + DataBaseName)
                    results = cur.fetchall()
                    for row in results:
                        rows = rows + 1
                    print(rows)
                    cur.execute("DELETE FROM " + DataBaseName + " WHERE " + DataBaseName + ".SN = " + str(rows))

                    self.connection.commit()
                    index = self.DataBaseNameArray.index(DataBaseName)
                    self.faultreports[index].configure(width = 20, activebackground = "#33B5E5", relief = FLAT, bg='gray95')

                messagebox.showinfo('Success', 'Record deleted...')

            except:
                messagebox.showinfo('Error', 'Error in data entry...')
            finally:
                print("Deleted")

        def wipe_entry(self):

            for i in range (self.count):
                self.img[i].destroy()
            self.img = []
            self.description_1.delete('1.0', END)
            self.rectification_1.delete('1.0', END)


        def completeSQL(self, DataBaseName) :
            try:
                if self.connection:
                    cur = self.connection.cursor()
                    rows = 0
                    cur.execute("SELECT * FROM " + DataBaseName)
                    results = cur.fetchall()
                    for row in results:
                        rows = rows + 1

                    print(rows)
                    cur.execute("UPDATE " + DataBaseName + " SET status = 'Completed', Rectification = '" + str(self.rectification_1.get('1.0', END)) +"' WHERE " + DataBaseName + ".SN = " + str(rows))

                    cur.execute("SELECT * FROM " + DataBaseName)
                    results = cur.fetchall()
                    for row in results:
                    	if row[9] == "Completed":
                    		index = self.DataBaseNameArray.index(DataBaseName)
                    		self.faultreports[index].configure(width = 20, activebackground = "#33B5E5", relief = FLAT, bg='gray95')

                    self.connection.commit()
                messagebox.showinfo('Success', 'Record Completed') 

            except:
                messagebox.showinfo('Error', 'Upate Failed...')
            finally:
                print("SQL Update Status Completed")
                self.wipe_entry()
                #self.connection.close()

        def ImageRecords(self, control, DataBaseName):

            print("Open New Window ")
            print(DataBaseName)
            self.controller = control
            self.window = Toplevel(self)
            self.search_var = StringVar()
            self.search_var.trace("w", self.update_list)

            placeholder = "Type and press enter"

            self.canvas = Canvas(self.window, bg='#FFFFFF',width=500,height=500,scrollregion=(0,0,1000,10000))
            
            hbar = Scrollbar(self.window,orient=HORIZONTAL)
            hbar.pack(side=BOTTOM,fill=X)
            hbar.config(command = self.canvas.xview)
            vbar = Scrollbar(self.window,orient=VERTICAL)
            vbar.pack(side=RIGHT,fill=Y)
            vbar.config(command =self.canvas.yview)
            self.canvas.config(width=700,height=700)
            self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
            self.canvas.pack(side=LEFT,expand=True,fill=BOTH)

            # first image
            self.heading = Label(self.window, text = DataBaseName, width = 50)
            heading_window = self.canvas.create_window(10, 10, anchor=NW, window = self.heading)

            dateLabel = Label(self.window, text="DATE", width=10)
            dateLabel_window = self.canvas.create_window(10, 40, anchor=NW, window = dateLabel)

            searchtxt = Entry(self.window, width=30, background="white", highlightcolor="#009688", highlightthickness=1)
            searchtxt_window = self.canvas.create_window(100, 40, anchor=NW, window = searchtxt)

            searchbtn = Button(self.window, text="Search", command=lambda a=searchtxt.get(), b= DataBaseName: self.searchFun(searchtxt.get(), b, self.window, self.canvas), width=10)
            searchbtn_window = self.canvas.create_window(300, 40, anchor=NW, window = searchbtn)

            
            for i in range(10):
                self.date = Label(self.window, text="Date:", width=(10))
                date_window = self.canvas.create_window(10, 100+(i*680), anchor=NW, window = self.date)

                self.ImgLabel = Label(self.window, text="Image:", width=(10))
                ImgLabel_window = self.canvas.create_window(10, 130+(i*680), anchor=NW, window = self.ImgLabel)

                self.descriptionlabel = Label(self.window, text="Description:", width=10)
                descriptionlabel_window = self.canvas.create_window(10, 410+(i*680), anchor=NW, window = self.descriptionlabel)

                self.description_1 = Text(self.window, height= 6, width=60, bg="yellow")
                description_1_window = self.canvas.create_window(10, 440+(i*680), anchor=NW, window = self.description_1)

                self.rectificationlabel = Label(self.window, text="Rectification", width=10)
                rectificationlabel_window = self.canvas.create_window(10, 560+(i*680), anchor=NW, window = self.rectificationlabel)

                self.rectification_1 = Text(self.window, height= 6, width=60, bg="red")
                rectification_1_window = self.canvas.create_window(10, 590+(i*680), anchor=NW, window = self.rectification_1)

        def searchFun(self, searchtxt, DataBaseName, control, canv) :

            xaxis = 0
            yaxis = 50
            print(searchtxt)
            print(DataBaseName)
            
            if self.connection:
                # Select Query Example :- Selecting data from the table.
                cursor = self.connection.cursor()
                # This is to prove that the connection to the server is "Established".
                print("DB Connection was a great success.lolz.")
                
                try :
                    if (searchtxt == "January"):
                        sql = "SELECT * FROM " + DataBaseName + " WHERE Date >= '2019-01-01 00:00:00' AND Date <= '2019-01-31 23:59:59'"
                        cursor.execute(sql)
                        results = cursor.fetchall()
                    elif (searchtxt == "February"):
                        sql = "SELECT * FROM " + DataBaseName + " WHERE Date >= '2019-02-01 00:00:00' AND Date <= '2019-02-29 23:59:59'"
                        cursor.execute(sql)
                        results = cursor.fetchall()
                    elif (searchtxt == "March"):
                        sql = "SELECT * FROM " + DataBaseName + " WHERE Date >= '2019-03-01 00:00:00' AND Date <= '2019-03-31 23:59:59'"
                        cursor.execute(sql)
                        results = cursor.fetchall()
                    elif (searchtxt == "April"):
                        sql = "SELECT * FROM " + DataBaseName + " WHERE Date >= '2019-04-01 00:00:00' AND Date <= '2019-04-30 23:59:59'"
                        cursor.execute(sql)
                        results = cursor.fetchall()
                    elif (searchtxt == "May"):
                        sql = "SELECT * FROM " + DataBaseName + " WHERE Date >= '2019-05-01 00:00:00' AND Date <= '2019-05-31 23:59:59'"
                        cursor.execute(sql)
                        results = cursor.fetchall()
                    elif (searchtxt == "June"):
                        sql = "SELECT * FROM " + DataBaseName + " WHERE Date >= '2019-06-01 00:00:00' AND Date <= '2019-06-30 23:59:59'"
                        cursor.execute(sql)
                        results = cursor.fetchall()
                    elif (searchtxt == "July"):
                        sql = "SELECT * FROM " + DataBaseName + " WHERE Date >= '2019-07-01 00:00:00' AND Date <= '2019-07-31 23:59:59'"
                        cursor.execute(sql)
                        results = cursor.fetchall()
                    elif (searchtxt == "August"):
                        sql = "SELECT * FROM " + DataBaseName + " WHERE Date >= '2019-08-01 00:00:00' AND Date <= '2019-08-31 23:59:59'"
                        cursor.execute(sql)
                        results = cursor.fetchall()
                    elif (searchtxt == "September"):
                        sql = "SELECT * FROM " + DataBaseName + " WHERE Date >= '2019-09-01 00:00:00' AND Date <= '2019-09-30 23:59:59'"
                        cursor.execute(sql)
                        results = cursor.fetchall()
                    elif (searchtxt == "October"):
                        sql = "SELECT * FROM " + DataBaseName + " WHERE Date >= '2019-10-01 00:00:00' AND Date <= '2019-10-31 23:59:59'"
                        cursor.execute(sql)
                        results = cursor.fetchall()
                    elif (searchtxt == "November"):
                        sql = "SELECT * FROM " + DataBaseName + " WHERE Date >= '2019-11-01 00:00:00' AND Date <= '2019-11-30 23:59:59'"
                        cursor.execute(sql)
                        results = cursor.fetchall()
                    elif (searchtxt == "December"):
                        sql = "SELECT * FROM " + DataBaseName + " WHERE Date >= '2019-12-01 00:00:00' AND Date <= '2019-12-31 23:59:59'"
                        cursor.execute(sql)
                        results = cursor.fetchall()

                    
                except:
                    messagebox.showinfo('Error', 'Search in data entry...')
                finally:
                    print("Query Over")
                    self.connection.close()

                numofrecord = 0
                recordsRow = []
                recordCol = []
                
                for row in results:
                        recordCol = []
                        for j in range (9):
                                recordCol.append(row[j])
                                
                        recordsRow.append(recordCol)
                        print(recordsRow)
                        print("\n")
                        self.date = Label(control, text= row[1], width=(25))
                        date_window = canv.create_window(100, 100+(numofrecord * 680), anchor=NW, window = self.date)
                        for i in range (2, 7):
                                if row[i] != None:
                                        load = Image.open(row[i])
                                        render = ImageTk.PhotoImage(load)
                                        size = (220, 250)
                                        resized = load.resize(size,Image.ANTIALIAS)
                                        render = ImageTk.PhotoImage(resized)
                                        self.img = Label(self.window, image=render)
                                        self.img.image = render
                                        img_window = self.canvas.create_window(10 + ((i - 2)*220), 155 + (numofrecord * 680), anchor=NW, window = self.img)
                        self.descriptionlabel = Label(control, text= row[7], width=56, height=6, anchor=NW, bg="yellow")
                        descriptionlabel_window = canv.create_window(15, 442+(numofrecord*680), anchor=NW, window = self.descriptionlabel)
                        self.rectificationlabel = Label(control, text= row[8], width=56, height=6, anchor=NW, bg="red")
                        rectificationlabel_window = canv.create_window(15, 592+(numofrecord*680), anchor=NW, window = self.rectificationlabel)
                        numofrecord = numofrecord + 1


        def update_list(self, *args):
            search_term = self.search_var.get()

        def add_placeholder_to(entry, placeholder, color="grey", font=None):
            normal_color = entry.cget("fg")
            normal_font = entry.cget("font")

            if font is None:
                font = normal_font

            state = Placeholder_State()
            state.normal_color=normal_color
            state.normal_font=normal_font
            state.placeholder_color=color
            state.placeholder_font=font
            state.placeholder_text = placeholder
            state.contains_placeholder=True

            def on_focusin(event, entry=entry, state=state):
                if state.contains_placeholder:
                    entry.delete(0, "end")
                    entry.config(fg = state.normal_color, font=state.normal_font)
            
                    state.contains_placeholder = False

            def on_focusout(event, entry=entry, state=state):
                if entry.get() == '':
                    entry.insert(0, state.placeholder_text)
                    entry.config(fg = state.placeholder_color, font=state.placeholder_font)
                
                    state.contains_placeholder = True

            entry.insert(0, placeholder)
            entry.config(fg = color, font=font)

            entry.bind('<FocusIn>', on_focusin, add="+")
            entry.bind('<FocusOut>', on_focusout, add="+")

            entry.placeholder_state = state

            return state


    
class RecordsPage(Frame):
        def __init__(self, parent, controller):
            Frame.__init__(self, parent)
            self.controller = controller
            self.search_var = StringVar()
            self.search_var.trace("w", self.update_list)

            self.connection = connect("localhost", "root", "", "firestationdb")
            placeholder = "Type and press enter"

            self.canvas = Canvas(self,bg='#FFFFFF',width=500,height=500,scrollregion=(0,0,1000, 55000))

            hbar = Scrollbar(self,orient=HORIZONTAL)
            hbar.pack(side=BOTTOM,fill=X)
            hbar.config(command = self.canvas.xview)
            vbar = Scrollbar(self,orient=VERTICAL)
            vbar.pack(side=RIGHT,fill=Y)
            vbar.config(command =self.canvas.yview)
            self.canvas.config(width=700,height=700)
            self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
            self.canvas.pack(side=LEFT,expand=True,fill=BOTH)

            
            # Search Bar
            dateLabel = Label(self, text="DATE", width=10)
            dateLabel_window = self.canvas.create_window(10, 10, anchor=NW, window = dateLabel)

            searchtxt = Entry(self, width=30, background="white", highlightcolor="#009688", highlightthickness=1)
            searchtxt_window = self.canvas.create_window(100, 10, anchor=NW, window = searchtxt)


            print(self.search_var)

            #Send Query button
            searchbtn = Button(self, text="Search", command=lambda a=searchtxt.get(): self.searchFun(searchtxt.get()), width=10)
            searchbtn_window = self.canvas.create_window(300, 10, anchor=NW, window = searchbtn)

            backbtn = Button(self, text="Back", command=lambda: controller.show_frame("Menu"), width=10)
            backbtn_window = self.canvas.create_window(380, 10, anchor=NW, window = backbtn)

            # Table 1
            for i in range(31):

                self.date_label = Label(self, text="DATE", width=10)
                date_label_window = self.canvas.create_window(10, 70 + (i * 1680), anchor=NW, window = self.date_label)

                self.name_label = Label(self, text="NAME", width=10)
                name_label_window = self.canvas.create_window(10, 100 + (i * 1680), anchor=NW, window = self.name_label)

                self.rota_label = Label(self, text="ROTA", width=10)       
                rota_label_window = self.canvas.create_window(10, 130 + (i * 1680), anchor=NW, window = self.rota_label)

                self.regis_label = Label(self, text="SERIAL", width=10)      
                regis_label_window = self.canvas.create_window(10, 160 + (i * 1680), anchor=NW, window = self.regis_label)

                self.check = Label(self, text="STATUS", width=10)
                check_window = self.canvas.create_window(470, 190 + (i * 1680), anchor=NW, window = self.check)

                self.remarks = Label(self, text="REMARKS", width=25)
                remarks_window = self.canvas.create_window(560, 190 + (i * 1680), anchor=NW, window = self.remarks)

            for num in range(31):
                sizex = 10 
                sizey = 190
                yaxis = 190
                posx = 0
                posy = 0

                serials = []
                serialName = ["S/N", "A", "1", "2", "3", "4", "5", "B", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "C", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "D", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

                items = []
                itemsName = ["ITEMS FOR INSPECTION", "ENGINE COMPARTMENT", "Check Engine (OBM)", "Check 2T Oil (Container & Cable)", "Check Fuel Valve (Secondary)", "Check Cable & Wiring", "Check Battery Switch & Compartment", "INTERIOR", "Check Upholstery/Seats/Fans/Windows", "Check Steering/Gears/Throttle/Kill Switch Knob", "Test Steering Turn: Port/Starboard/Mid-Ship", "Test Gears Engage: Fwd/Astern/Neutral", "Check All Switches In Working Condition", "Check For OBM Tell Tale Sign Of Engine", "Check For Navigational Lights & All Other Lights", "Check Analogue Meter Gauge & Digital Tachometer", "Check Horn", "Check Fuel Valve (Primary), Check Fuel Level - Forward & Aft Tank", "Check Comms Equipment: VHF/Matra/PA System", "Check Navigational System: Radar/Echosounder/GPS", "Check Availability Of GPS1 CHART/SPI/TT", "Check Availability Of Medical Box And Its Condition", "Check Pressure & Expiry Date Of Fire Extinguisher", "Look For Sign Of Leakage/Flooding", "EXTERIOR", "General Body Condition & Paint Work", "Check Rubber Fenders Trimming Condition", "Check Railing & Fenders/LifeBuoys In Good Condition", "Check All Lights In Good & Working Condition", "Check PA System And Siren", "Check Radar Antenna & Lightning Arrestor", "Check Bilge Pumps In Good/Working Condition", "Fresh Water Pump In Good/Working Condition", "Check Presence of Anchor/Chain/Ropes", "Check Prescence Of Boats Hook", "Check Wipers & CVS", "OTHERS", "Listen For Unusual Knocks/Sounds", "Check The Function Of Meters", "Wash Vessel Exterior", "Clean Interior/Door Closed", "Forward Fuel Tank Level", "Aft Fuel Tank Level", "Switch Off Ignition & All Lights", "All OBM Engine Trim Up", "Close Windows", "Check Vessels Battery Connection"]

                del serials[:]
                del items[:]

                for i in range(47):
                        serials.append(Label(self, text=serialName[i], width=10))
                        items.append(Label(self, text=itemsName[i], width=50))
                        if (i == 7):
                                yaxis = 220
                        elif (i == 24):
                                yaxis = 250
                        elif (i == 36):
                                yaxis = 280

                        check_window = self.canvas.create_window(sizex, yaxis + (i * 30) + (num * 1680), anchor=NW, window = serials[i])
                        items_window = self.canvas.create_window(100, yaxis + (30*i) + (num * 1680), anchor=NW, window = items[i])

    		# End

        def searchFun(self, searchtxt) :

            xaxis = 0
            yaxis = 50
            
            if self.connection:
                # Select Query Example :- Selecting data from the table.
                cursor = self.connection.cursor()
                # This is to prove that the connection to the server is "Established".
                print("DB Connection was a great success.hhehe.")
                
                try :
                    if (searchtxt == "January"):
                        sql = "SELECT * FROM checklist_tbl WHERE Date >= '2019-01-01 00:00:00' AND Date <= '2019-01-31 23:59:59'"
                        cursor.execute(sql)
                        results = cursor.fetchall()
                    elif (searchtxt == "February"):
                        sql = "SELECT * FROM checklist_tbl WHERE Date >= '2019-02-01 00:00:00' AND Date <= '2019-02-29 23:59:59'"
                        cursor.execute(sql)
                        results = cursor.fetchall()
                    elif (searchtxt == "March"):
                        sql = "SELECT * FROM checklist_tbl WHERE Date >= '2019-03-01 00:00:00' AND Date <= '2019-03-31 23:59:59'"
                        cursor.execute(sql)
                        results = cursor.fetchall()
                    elif (searchtxt == "April"):
                        sql = "SELECT * FROM checklist_tbl WHERE Date >= '2019-04-01 00:00:00' AND Date <= '2019-04-30 23:59:59'"
                        cursor.execute(sql)
                        results = cursor.fetchall()
                    elif (searchtxt == "May"):
                        sql = "SELECT * FROM checklist_tbl WHERE Date >= '2019-05-01 00:00:00' AND Date <= '2019-05-31 23:59:59'"
                        cursor.execute(sql)
                        results = cursor.fetchall()
                    elif (searchtxt == "June"):
                        sql = "SELECT * FROM checklist_tbl WHERE Date >= '2019-06-01 00:00:00' AND Date <= '2019-06-30 23:59:59'"
                        cursor.execute(sql)
                        results = cursor.fetchall()
                    elif (searchtxt == "July"):
                        sql = "SELECT * FROM checklist_tbl WHERE Date >= '2019-07-01 00:00:00' AND Date <= '2019-07-31 23:59:59'"
                        cursor.execute(sql)
                        results = cursor.fetchall()
                    elif (searchtxt == "August"):
                        sql = "SELECT * FROM checklist_tbl WHERE Date >= '2019-08-01 00:00:00' AND Date <= '2019-08-31 23:59:59'"
                        cursor.execute(sql)
                        results = cursor.fetchall()
                    elif (searchtxt == "September"):
                        sql = "SELECT * FROM checklist_tbl WHERE Date >= '2019-09-01 00:00:00' AND Date <= '2019-09-30 23:59:59'"
                        cursor.execute(sql)
                        results = cursor.fetchall()
                    elif (searchtxt == "October"):
                        sql = "SELECT * FROM checklist_tbl WHERE Date >= '2019-10-01 00:00:00' AND Date <= '2019-10-31 23:59:59'"
                        cursor.execute(sql)
                        results = cursor.fetchall()
                    elif (searchtxt == "November"):
                        sql = "SELECT * FROM checklist_tbl WHERE Date >= '2019-11-01 00:00:00' AND Date <= '2019-11-30 23:59:59'"
                        cursor.execute(sql)
                        results = cursor.fetchall()
                    elif (searchtxt == "December"):
                        sql = "SELECT * FROM checklist_tbl WHERE Date >= '2019-12-01 00:00:00' AND Date <= '2019-12-31 23:59:59'"
                        cursor.execute(sql)
                        results = cursor.fetchall()
                 
                except:
                    messagebox.showinfo('Error', 'Search in data entry...')
                finally:
                    print("Query Over")
                    self.connection.close()


                numofrecord = 0
                recordsRow = []
                recordCol = []

                for row in results:
                        for i in range(4):
                                recordCol.append(row[i])

                        recordsRow.append(recordCol)
                        print(recordsRow[numofrecord])

                        sizex = 100
                        sizey = 70
                        yaxis = 70
                        posx = 0
                        posy = 0

                        record = []
                        recordName = [row[0], row[1], row[2], row[3]]

                        del record[:]

                    # Date Name Rota SN
                        for i in range(4):
                                record.append(Label(self, text=recordName[i], width=20))
                                record_window = self.canvas.create_window(100, 70 + (i * 30) + (numofrecord * 1680), anchor=NW, window = record[i])

                        numofrecord = numofrecord + 1


                numofrecord2 = 0
                recordsRow2 = []
                recordCol2 = []

                for row in results:
                        for i in range(42):
                                recordCol2.append(row[i])
                    # RecordsRow2[0][0] = Date # RecordsRow2[0][1] = Name # RecordsRow2[1][0] = 2nd Entry Date
                        recordsRow2.append(recordCol2)
                        recordCol2 = []
                        print(recordsRow2[numofrecord2])

                        sizex = 470
                        sizey = 250
                        yaxis = 250
                        posx = 0
                        posy = 0

                    # For Loop through the recordsRow2.
                        record1 = []
                        record1Name = [row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25], row[26], row[27], row[28], row[29], row[30], row[31], row[32], row[33], row[34], row[35], row[36], row[37], row[38], row[39], row[40], row[41], row[42], row[43], row[44], row[45]]

                        record2 = []
                        record2Name = [row[46], row[47], row[48], row[49], row[50], row[51], row[52], row[53], row[54], row[55], row[56], row[57], row[58], row[59], row[60], row[61], row[62], row[63], row[64], row[65], row[66], row[67], row[68], row[69], row[70], row[71], row[72], row[73], row[74], row[75], row[76], row[77], row[78], row[79], row[80], row[81], row[82], row[83], row[84], row[85], row[86], row[87]]

                        del record1[:]
                        del record2[:]	

                        for i in range(42):
                                record1.append(Label(self, text=record1Name[i], width=10))
                                record2.append(Label(self, text=record2Name[i], width=25))

                                if (i == 5):
                                        yaxis = 310
                                elif (i == 21):
                                        yaxis = 370
                                elif (i == 32):
                                        yaxis = 430

                                record1_window = self.canvas.create_window(470, yaxis + (i*30) + (numofrecord2*1680), anchor=NW, window = record1[i])
                                record2_window = self.canvas.create_window(560, yaxis + (i*30) + (numofrecord2*1680), anchor=NW, window = record2[i])

                        numofrecord2 = numofrecord2 + 1

            # Finished the currently row query. Therefore, y-axis need to be increase.
                        

        def update_list(self, *args):
            search_term = self.search_var.get()

        def add_placeholder_to(entry, placeholder, color="grey", font=None):
            normal_color = entry.cget("fg")
            normal_font = entry.cget("font")

            if font is None:
                font = normal_font

            state = Placeholder_State()
            state.normal_color=normal_color
            state.normal_font=normal_font
            state.placeholder_color=color
            state.placeholder_font=font
            state.placeholder_text = placeholder
            state.contains_placeholder=True

            def on_focusin(event, entry=entry, state=state):
                if state.contains_placeholder:
                    entry.delete(0, "end")
                    entry.config(fg = state.normal_color, font=state.normal_font)
            
                    state.contains_placeholder = False

            def on_focusout(event, entry=entry, state=state):
                if entry.get() == '':
                    entry.insert(0, state.placeholder_text)
                    entry.config(fg = state.placeholder_color, font=state.placeholder_font)
                
                    state.contains_placeholder = True

            entry.insert(0, placeholder)
            entry.config(fg = color, font=font)

            entry.bind('<FocusIn>', on_focusin, add="+")
            entry.bind('<FocusOut>', on_focusout, add="+")

            entry.placeholder_state = state

            return state


class FaultReporting(Frame):
        def __init__(self, parent, controller):
            Frame.__init__(self, parent)
            self.controller = controller

    
    
if __name__ == "__main__":
        app = SampleApp()
        app.mainloop()
