import tkinter as tk
from tkinter import simpledialog
from mcstatus import MinecraftServer
import os.path

class App(tk.Tk):

    global ip
    
    global fh
    fh = 'mcserveraddy.txt'

    def __init__(self):
        super().__init__()
        App.ip = None


        ### IP
        # Check if directory exists. If so pull first IP
        if os.path.isfile(fh):
            with open(fh, 'r') as f:
                # Find IP from last item in file
                lines = f.readlines()
                doclen = len(lines)
                App.ip = lines[doclen-1].split()[1]
            f.close()
        # If there is no existing IP address file, get IP and create file
        if App.ip is None:
            self.withdraw()
            App.ip = simpledialog.askstring("IP", "What is the server's IP address?",parent=self)
            txtentry = "ip: "+App.ip
            with open(fh, 'w+') as f:
                f.writelines(txtentry)
            f.close()
            self.update()
            self.deiconify()
        

        ### Window
        # Define Parameters for Window
        self.title('Homescreen')
        self.configure(bg='#5a8231')
        # Define window size
        window_width = 200
        window_height = 400
        # Get screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # Find center point
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        # Set geometry
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.attributes('-topmost', 1)

        # Define Parameters for Text Box
        self.T = tk.Text(self, height = 10, width = 20)
        self.T.pack(expand = True)
        self.T.configure(bg='#3a541e')
        

        ### Buttons
        # Dimensions
        bw = 15
        bh = 1
        # Button color and button press color
        bcol = '#694715'
        bpcol = '#4a320f'

        # Server Active Button
        server_active = tk.Button(self, text='Is Server Running?', height = bh, width = bw, bd='5', bg=bcol, activebackground=bpcol, command=self.GetServerActive)
        server_active.pack(side='top')
        
        # Server Status Button
        get_server_status = tk.Button(self, text='Get Server Status', height = bh, width = bw, bd='5', bg=bcol, activebackground=bpcol, command=self.GetServerStatus)
        get_server_status.pack(side='top')

        # Active Players Button
        get_active_players = tk.Button(self, text='Get Active Players', height = bh, width = bw, bd='5', bg=bcol, activebackground=bpcol, command=self.GetActivePlayers)
        get_active_players.pack(side='top')

        # Server IP Button
        get_server_ip = tk.Button(self, text='Get Server IP', height = bh, width = bw, bd='5', bg=bcol, activebackground=bpcol, command=self.GetServerIP)
        get_server_ip.pack(side= 'top')

        # Change IP Button --- Override Previous List
        # change_ip_override_button = tk.Button(self, text='Change IP Address', height = bh, width = bw, bd='5', bg=bcol, activebackground=bpcol, command=self.ChangeIP_Overwrite)
        # change_ip_override_button.pack(side='top')

        # Change IP Button --- Add Value to List
        change_ip_list_button = tk.Button(self, text='Change IP Address', height = bh, width = bw, bd='5', bg=bcol, activebackground=bpcol, command=self.ChangeIP_List)
        change_ip_list_button.pack(side='top')

        # Close Window Button
        close_button = tk.Button(self, text='Close', height = bh, width = bw, bd='5', bg=bcol, activebackground=bpcol, command=self.destroy)
        close_button.pack(side= 'top')
    

    ### Useful Functions
    # Change Textbox Contents
    def setTextInput(self,text):
        self.T.delete(1.0,"end")
        self.T.insert(1.0, text)

    # Get Server Activity
    def GetServerActive(self):
        try:
            server = MinecraftServer.lookup(App.ip)
            status = server.status() # if this is possible the server is active
            self.setTextInput("Server is:\nCurrently Active")

        except Exception as exc :
            if str(exc).split()[0:4] == ['can', 'only', 'concatenate', 'str']: self.setTextInput("Server is:\nInactive...");
            elif str(exc) == "timed out": self.setTextInput("Server is:\nOff...");
            else: self.setTextInput("Server is:\nInactive...\n\nError:\n" + str(exc));

    # Get Server Operation Status
    def GetServerStatus(self):
        try:
            server = MinecraftServer.lookup(App.ip)
            status = server.status()
            self.setTextInput("Server is:\nActive\n\nServer has:\n{0} player(s)\n\nReplied in:\n{1} ms".format(status.players.online, status.latency))

        except Exception as exc :
            if str(exc).split()[0:4] == ['can', 'only', 'concatenate', 'str']: self.setTextInput("Server is:\nInactive...");
            elif str(exc) == "timed out": self.setTextInput("Server is:\nOff...");
            else: self.setTextInput("Server is:\nInactive...\n\nError:\n" + str(exc));

    # Get Active Players on Server
    def GetActivePlayers(self):
        try:
            server = MinecraftServer.lookup(App.ip)
            status = server.status()
            usersConnected = [ user['name'] for user in status.raw['players']['sample'] ]
            l = ""
            for ppl in usersConnected:
                l += ppl + "\n"
            self.setTextInput("Users in the Server:\n"+l);

        except Exception as exc :
            if str(exc) == "'sample'": self.setTextInput("Nobody Active on\nServer...");
            elif str(exc).split()[0:4] == ['can', 'only', 'concatenate', 'str']: self.setTextInput("Server is:\nInactive...");
            elif str(exc) == "timed out": self.setTextInput("Server is:\nOff...");
            else: self.setTextInput("Server is:\nInactive...\n\nError:\n" + str(exc));
            
    # Get the Server IP
    def GetServerIP(self):
        self.setTextInput("Server's IP:\n" + str(App.ip))

    # Change Current IP and Overwrite All Previous
    def ChangeIP_Overwrite(self, fh):
        newip = simpledialog.askstring("IP", "What is the new server's IP address?",parent=self, )
        with open(fh, 'w+') as f:
            iptext = "ip: "+newip
            f.writelines(iptext)
        f.close()
        self.update()
        self.destroy()
        new = App()
        new.mainloop()

    # Change Current IP and Add to List
    def ChangeIP_List(self):
        # keeps old values >>> can make a drop down bar
        newip = simpledialog.askstring("IP", "What is the new server's IP address?",parent=self)
        with open(fh, 'a') as f:
            iptext = "\nip: "+newip
            f.writelines(iptext)
        f.close()
        with open(fh, 'r') as f:
            readlist = f.read().split()
            # List of all ip addresses accessed
            iplist = readlist[1::2]
            print(iplist)
        f.close()
        self.update()
        self.destroy()
        new = App()
        new.mainloop()




### Run Program
if __name__ == '__main__':
    app = App()
    app.mainloop()


#### NOTE
# * Make Dropdown bar for all previously used IP's
# * Check if IP is of valid form
# * If a certain number of entries is surpassed, clear
