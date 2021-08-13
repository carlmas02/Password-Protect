from kivymd.app import MDApp
from kivymd.uix.label import MDLabel,MDIcon
from kivymd.uix.button import MDRoundFlatButton
from kivy.lang import Builder
from kivymd.uix.screen import Screen
from kivy.uix.screenmanager import Screen,ScreenManager
from kivymd.uix.list import OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.snackbar import Snackbar

from kivy.core.text import LabelBase
from kivy.core.window import Window
Window.size = (350, 600)

import requests
BASE = "http://testingcarl.pythonanywhere.com/" 


class LoginScreen(Screen):
    pass

class SignupScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class DetailScreen(Screen):
    pass

class AccountScreen(Screen):
    pass

class UpdateScreen(Screen):
    pass

sm = ScreenManager()
sm.add_widget(LoginScreen(name='login_screen'))
sm.add_widget(SignupScreen(name='signup_new'))
sm.add_widget(SignupScreen(name='main'))
sm.add_widget(DetailScreen(name='detail'))
sm.add_widget(AccountScreen(name='account'))
sm.add_widget(AccountScreen(name='update'))

class LoginApp(MDApp):
    def build(self):
        try :
            requests.get(BASE)
        except:
            print("Error")
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Dark"


        self.main_str = Builder.load_file('main_str.kv')

        return self.main_str

    def check(self):
        self.userid = self.main_str.get_screen('login_screen').ids.username.text
        password = self.main_str.get_screen('login_screen').ids.password.text
        
        self.main_str.get_screen('login_screen').ids.username.text = ''
        self.main_str.get_screen('login_screen').ids.password.text = ''
        if self.userid == '' or password == '':
            MDDialog(title = "Error!",text = "Some fields are missing !" ).open()
            return
        resp = requests.get(BASE + f"login/{self.userid}",{"username":self.userid,"password":password})
        if resp.json() == 201:
            self.main_str.get_screen('login_screen').manager.current= 'main'
            self.put_info('obj')
        else :
            MDDialog(title = "Error!",text = "Username and password do not match" ).open()
        
              

    def put_info(self,obj):
        self.data = requests.get(BASE + f"people/{self.userid}").json()
        if self.data == {}:
            print("yo")
            
        for service in self.data:
            item = OneLineListItem(text =service,on_press =self.hello)
            self.main_str.get_screen('main').ids.list_tray.add_widget(item)
        
    def hello(self,item):
        self.last_item = item
        name = item.text
        username = self.data[name][0]
        password = self.data[name][1]
        self.main_str.get_screen('main').manager.current= 'account'
        self.main_str.get_screen('account').ids.account_service.text = name
        self.main_str.get_screen('account').ids.account_username.text = username
        self.main_str.get_screen('account').ids.account_password.text = password

    def create_user(self):
        name = self.main_str.get_screen('signup_new').ids.signup_name.text
        self.userid = self.main_str.get_screen('signup_new').ids.signup_username.text
        password = self.main_str.get_screen('signup_new').ids.signup_password.text 
        
        if name == '' or self.userid == '' or password == '':
            self.bye = MDDialog(title="Error ",text="Some fields are missing")
            self.bye.open()
            return 

        data = requests.put(BASE + f"signup/",{"name":name,'username':self.userid,"password":password}).json()
        if data == 201:
            self.main_str.get_screen('signup_new').manager.current= 'main'
        elif data == 400 :
            self.bye = MDDialog(title="Error ",text="Username already exists !")
            self.bye.open()

        self.main_str.get_screen('signup_new').ids.signup_name.text = ''
        self.main_str.get_screen('signup_new').ids.signup_username.text = ''
        self.main_str.get_screen('signup_new').ids.signup_password.text = ''
            
    def submit_service(self):
        serv_name = self.main_str.get_screen('detail').ids.service_name.text
        serv_username = self.main_str.get_screen('detail').ids.service_username.text
        serv_password = self.main_str.get_screen('detail').ids.service_password.text

        if serv_name == "" or serv_username == "" or serv_password == '':
            self.bye = MDDialog(title= "Error !",text ="All fields must be filled ")
            self.bye.open()
            return

        resp = requests.post(BASE + f"login/{self.userid}",{"service":serv_name,"username":serv_username,"password":serv_password}).json()
        
        if resp== 201:
            self.data = requests.get(BASE + f"people/{self.userid}").json()
            item = OneLineListItem(text =serv_name,on_press =self.hello)
            self.main_str.get_screen('detail').manager.current= 'main'
            self.main_str.get_screen('main').ids.list_tray.add_widget(item)
        else :
           self.bye = MDDialog(title= "Error !",text ="You cannot use same username for two similar services")
           self.bye.open() 

        self.main_str.get_screen('detail').ids.service_name.text = ''
        self.main_str.get_screen('detail').ids.service_username.text = ''
        self.main_str.get_screen('detail').ids.service_password.text = ''

    def callback(self,button):
        self.bye = MDDialog(text = "Details",
            buttons = [MDRoundFlatButton(text = "Delete User",on_release=self.delete_user),
                       MDRoundFlatButton(text = "Logout",on_release=self.logout)]
            )
        self.bye.open()

    def logout(self,obj):
        self.main_str.get_screen('main').ids.list_tray.clear_widgets()
        self.bye.dismiss()
        self.main_str.get_screen('main').manager.current= 'login_screen'

    def update_info(self,button):
        self.bye = MDDialog(
                        text="Settings",
                        buttons=[MDRoundFlatButton(text = "Update",on_release=self.update_service_details),
                                 MDRoundFlatButton(text = "Delete details",on_release=self.delete_single_detail)]
                    )
        
        self.bye.open()

    def delete_single_detail(self,obj):
        _tablename = self.userid
        _serv = self.main_str.get_screen('account').ids.account_service.text
        _uid      = self.main_str.get_screen('account').ids.account_username.text
        collection = _tablename +'-'+ _serv +'-'+ _uid
        resp = requests.delete(BASE + f"people/{collection}").json()
        if resp == 201:
            self.main_str.get_screen('main').ids.list_tray.remove_widget(self.last_item)
            self.main_str.get_screen('account').manager.current= 'main'
            
        self.bye.dismiss()
        
        
    def delete_user(self,obj):
        resp = requests.delete(BASE + f"login/{self.userid}").json()
        Snackbar(text="Account Deleted !").open()
        self.main_str.get_screen('main').manager.current= 'login_screen'
        self.main_str.get_screen('main').ids.list_tray.clear_widgets()
        self.bye.dismiss()

    def update_service_details(self,obj):
        self.bye.dismiss()
        self.main_str.get_screen('account').manager.current= 'update'
        
        self.update_service = self.main_str.get_screen('account').ids.account_service.text
        self.update_username = self.main_str.get_screen('account').ids.account_username.text
        self.update_password = self.main_str.get_screen('account').ids.account_password.text

        self.main_str.get_screen('update').ids.update_username.text = self.update_username
        self.main_str.get_screen('update').ids.update_password.text = self.update_password

        button = MDRoundFlatButton(text="Update",pos_hint={"center_x":0.75,"center_y":0.5},
                        on_press= self.update_single_service)
        self.main_str.get_screen('update').add_widget(button)

    def update_single_service(self,obj):
        u_id = self.userid

        username_new = self.main_str.get_screen('update').ids.update_username.text
        password_new = self.main_str.get_screen('update').ids.update_password.text
        obj_json = {"service": self.update_service,"prev_username":self.update_username,"new_username":None,"new_password":None}
        if username_new != self.update_username:
            obj_json['new_username'] = username_new
        if password_new != self.update_password:
            obj_json['new_password'] = password_new

        data = requests.put(BASE + f"people/{u_id}",obj_json).json()
        if data == 201 :
           self.main_str.get_screen('update').manager.current= 'main'
           self.main_str.get_screen('main').ids.list_tray.clear_widgets()
           self.put_info("obj")



LabelBase.register(name='Light',fn_regular='fonts//Poppins-Light.ttf')
LabelBase.register(name='semibold',fn_regular='fonts//Poppins-Semibold.ttf')

if __name__ == '__main__':
	LoginApp().run()