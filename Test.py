"""
Professional TODO Android Application with Login
Built with Kivy and KivyMD
Features: CRUD Operations, User Authentication, Modern UI
"""

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.scrollview import MDScrollView
from kivy.lang import Builder
from kivy.core.window import Window
import json
import os
from datetime import datetime

# Set window size for testing (remove for actual Android build)
Window.size = (360, 640)

KV = '''
MDScreenManager:
    LoginScreen:
    RegisterScreen:
    TodoScreen:

<LoginScreen>:
    name: 'login'
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 1, 1, 1, 1
        
        MDTopAppBar:
            title: "TODO App - Login"
            md_bg_color: 1, 1, 1, 1
            elevation: 2
        
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(30)
            spacing: dp(20)
            
            Widget:
                size_hint_y: 0.3
            
            MDLabel:
                text: "Welcome Back!"
                font_style: "H4"
                halign: "center"
                theme_text_color: "Primary"
            
            MDLabel:
                text: "Login to manage your tasks"
                font_style: "Caption"
                halign: "center"
                theme_text_color: "Secondary"
            
            Widget:
                size_hint_y: 0.1
            
            MDTextField:
                id: username
                hint_text: "Username"
                mode: "rectangle"
                icon_left: "account"
                size_hint_x: 1
            
            MDTextField:
                id: password
                hint_text: "Password"
                mode: "rectangle"
                password: True
                icon_left: "lock"
                size_hint_x: 1
            
            MDRaisedButton:
                text: "LOGIN"
                pos_hint: {"center_x": 0.5}
                size_hint_x: 0.8
                on_release: app.login()
            
            MDTextButton:
                text: "Don't have an account? Register"
                pos_hint: {"center_x": 0.5}
                on_release: app.root.current = 'register'
            
            Widget:
                size_hint_y: 0.3

<RegisterScreen>:
    name: 'register'
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 1, 1, 1, 1
        
        MDTopAppBar:
            title: "TODO App - Register"
            md_bg_color: 1, 1, 1, 1
            left_action_items: [["arrow-left", lambda x: app.go_back_to_login()]]
            elevation: 2
        
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(30)
            spacing: dp(20)
            
            Widget:
                size_hint_y: 0.2
            
            MDLabel:
                text: "Create Account"
                font_style: "H4"
                halign: "center"
                theme_text_color: "Primary"
            
            MDLabel:
                text: "Register to get started"
                font_style: "Caption"
                halign: "center"
                theme_text_color: "Secondary"
            
            Widget:
                size_hint_y: 0.1
            
            MDTextField:
                id: reg_username
                hint_text: "Username"
                mode: "rectangle"
                icon_left: "account"
            
            MDTextField:
                id: reg_password
                hint_text: "Password"
                mode: "rectangle"
                password: True
                icon_left: "lock"
            
            MDTextField:
                id: reg_confirm_password
                hint_text: "Confirm Password"
                mode: "rectangle"
                password: True
                icon_left: "lock-check"
            
            MDRaisedButton:
                text: "REGISTER"
                pos_hint: {"center_x": 0.5}
                size_hint_x: 0.8
                on_release: app.register()
            
            Widget:
                size_hint_y: 0.2

<TodoScreen>:
    name: 'todo'
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 1, 1, 1, 1
        
        MDTopAppBar:
            title: "My Tasks"
            md_bg_color: 1, 1, 1, 1
            right_action_items: [["logout", lambda x: app.logout()]]
            elevation: 2
        
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(15)
            spacing: dp(10)
            
            MDTextField:
                id: task_title
                hint_text: "Task Title"
                mode: "rectangle"
                icon_left: "text"
            
            MDTextField:
                id: task_description
                hint_text: "Task Description"
                mode: "rectangle"
                icon_left: "text-box"
                multiline: True
                max_height: dp(100)
            
            MDRaisedButton:
                text: "ADD TASK"
                pos_hint: {"center_x": 0.5}
                size_hint_x: 0.5
                on_release: app.add_task()
            
            MDLabel:
                text: "Your Tasks"
                font_style: "H6"
                size_hint_y: None
                height: dp(30)
                padding: [dp(10), 0]
            
            MDScrollView:
                MDList:
                    id: task_list
'''


class LoginScreen(MDScreen):
    pass


class RegisterScreen(MDScreen):
    pass


class TodoScreen(MDScreen):
    pass


class TodoApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_user = None
        self.users_file = 'users.json'
        self.tasks_file = 'tasks.json'
        self.dialog = None
        self.edit_task_id = None
        
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)
    
    def on_start(self):
        self.load_users()
        self.load_tasks()
    
    def load_users(self):
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)
    
    def load_tasks(self):
        if not os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'w') as f:
                json.dump({}, f)
    
    def show_dialog(self, title, text):
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()
    
    def register(self):
        screen = self.root.get_screen('register')
        username = screen.ids.reg_username.text.strip()
        password = screen.ids.reg_password.text.strip()
        confirm = screen.ids.reg_confirm_password.text.strip()
        
        if not username or not password:
            self.show_dialog("Error", "Please fill all fields")
            return
        
        if password != confirm:
            self.show_dialog("Error", "Passwords don't match")
            return
        
        with open(self.users_file, 'r') as f:
            users = json.load(f)
        
        if username in users:
            self.show_dialog("Error", "Username already exists")
            return
        
        users[username] = password
        with open(self.users_file, 'w') as f:
            json.dump(users, f)
        
        self.show_dialog("Success", "Registration successful! Please login.")
        self.go_back_to_login()
    
    def login(self):
        screen = self.root.get_screen('login')
        username = screen.ids.username.text.strip()
        password = screen.ids.password.text.strip()
        
        if not username or not password:
            self.show_dialog("Error", "Please enter username and password")
            return
        
        with open(self.users_file, 'r') as f:
            users = json.load(f)
        
        if username in users and users[username] == password:
            self.current_user = username
            self.root.current = 'todo'
            self.load_user_tasks()
            screen.ids.username.text = ""
            screen.ids.password.text = ""
        else:
            self.show_dialog("Error", "Invalid username or password")
    
    def logout(self):
        self.current_user = None
        self.root.current = 'login'
    
    def go_back_to_login(self):
        screen = self.root.get_screen('register')
        screen.ids.reg_username.text = ""
        screen.ids.reg_password.text = ""
        screen.ids.reg_confirm_password.text = ""
        self.root.current = 'login'
    
    def add_task(self):
        screen = self.root.get_screen('todo')
        title = screen.ids.task_title.text.strip()
        description = screen.ids.task_description.text.strip()
        
        if not title:
            self.show_dialog("Error", "Please enter a task title")
            return
        
        with open(self.tasks_file, 'r') as f:
            tasks = json.load(f)
        
        if self.current_user not in tasks:
            tasks[self.current_user] = []
        
        task_id = len(tasks[self.current_user]) + 1
        new_task = {
            'id': task_id,
            'title': title,
            'description': description,
            'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'completed': False
        }
        
        tasks[self.current_user].append(new_task)
        
        with open(self.tasks_file, 'w') as f:
            json.dump(tasks, f, indent=2)
        
        screen.ids.task_title.text = ""
        screen.ids.task_description.text = ""
        self.load_user_tasks()
    
    def load_user_tasks(self):
        screen = self.root.get_screen('todo')
        task_list = screen.ids.task_list
        task_list.clear_widgets()
        
        with open(self.tasks_file, 'r') as f:
            tasks = json.load(f)
        
        if self.current_user not in tasks or not tasks[self.current_user]:
            return
        
        for task in tasks[self.current_user]:
            item = TwoLineAvatarIconListItem(
                text=task['title'],
                secondary_text=task['description'][:50] + "..." if len(task['description']) > 50 else task['description'],
                on_release=lambda x, t=task: self.show_task_options(t)
            )
            
            icon = IconLeftWidget(
                icon="check-circle" if task['completed'] else "circle-outline",
                theme_text_color="Custom",
                text_color=(0, 1, 0, 1) if task['completed'] else (0.5, 0.5, 0.5, 1)
            )
            item.add_widget(icon)
            
            task_list.add_widget(item)
    
    def show_task_options(self, task):
        if self.dialog:
            self.dialog.dismiss()
        
        self.dialog = MDDialog(
            title=task['title'],
            text=task['description'],
            buttons=[
                MDFlatButton(
                    text="COMPLETE" if not task['completed'] else "UNCOMPLETE",
                    on_release=lambda x: self.toggle_complete(task['id'])
                ),
                MDFlatButton(
                    text="DELETE",
                    on_release=lambda x: self.delete_task(task['id'])
                ),
                MDFlatButton(
                    text="CLOSE",
                    on_release=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()
    
    def toggle_complete(self, task_id):
        with open(self.tasks_file, 'r') as f:
            tasks = json.load(f)
        
        for task in tasks[self.current_user]:
            if task['id'] == task_id:
                task['completed'] = not task['completed']
                break
        
        with open(self.tasks_file, 'w') as f:
            json.dump(tasks, f, indent=2)
        
        self.dialog.dismiss()
        self.load_user_tasks()
    
    def delete_task(self, task_id):
        with open(self.tasks_file, 'r') as f:
            tasks = json.load(f)
        
        tasks[self.current_user] = [t for t in tasks[self.current_user] if t['id'] != task_id]
        
        with open(self.tasks_file, 'w') as f:
            json.dump(tasks, f, indent=2)
        
        self.dialog.dismiss()
        self.load_user_tasks()


if __name__ == '__main__':
    TodoApp().run()