# Library imports
import tkinter as tk
from tkinter import messagebox
import webbrowser
import os
from win32com.client import Dispatch
import subprocess

# Read xmx and xms from xmx.xms file, if it does not exist, create it with default values
if os.path.exists('xmx.xms'):
    with open('xmx.xms', 'r') as file:
        lines = file.readlines()
    # split with =
    xmx = int(lines[0].split('=')[1].strip())
    xms = int(lines[1].split('=')[1].strip())
else:
    xmx = 4096
    xms = 1024
    # Create xmx.xms file
    with open('xmx.xms', 'w') as file:
        file.write('xmx=' + str(xmx) + '\n')
        file.write('xms=' + str(xms) + '\n')

# Global variables
server_process = None

# Function to show a specific page
def show_frame(frame):
    frame.tkraise()

# Create the main application window
root = tk.Tk()
root.title("Minecraft server made easy")
root.geometry("600x700")

# Create a menu bar
menu_bar = tk.Menu(root)

# Create the frames for each page
frame1 = tk.Frame(root)
frame2 = tk.Frame(root)
frame3 = tk.Frame(root)
frame4 = tk.Frame(root)
frame5 = tk.Frame(root)
frame6 = tk.Frame(root)

# Loop through each frame and configure it
for frame in (frame1, frame2, frame3, frame4, frame5, frame6):
    frame.grid(row=0, column=0, sticky="nsew")

############################################### Setup menu ###############################################################

def first_time_run():
    global server_process
    server_process = subprocess.Popen(['java', '-Xmx' + str(xmx) + 'M', '-Xms'+ str(xms) + 'M', '-jar', 'server.jar', 'nogui'])

    # wait until eula.txt is created
    while not os.path.exists('eula.txt'):
        # wait 100 ms to check again
        root.after(100)

    # Change eula.txt to accept the EULA
    if os.path.exists('eula.txt'):
        with open('eula.txt', 'r') as file:
            filedata = file.read()
        filedata = filedata.replace('eula=false', 'eula=true')
        with open('eula.txt', 'w') as file:
            file.write(filedata)
    server_process.terminate()

    # kill terminal window
    os.system('taskkill /f /im cmd.exe')

# Open URL in browser
def callback(url):
    webbrowser.open_new(url)

lbl = tk.Label(frame1, text="Initial setup for the server", font = ('Arial', 20), justify="left")
lbl.pack(anchor="w")

lbl = tk.Label(frame1, text = "1. Download the correct version of the Minecraft server jar from:", font = ('Arial', 12), justify="left")
lbl.pack(anchor="w")
lbl = tk.Label(frame1, text="https://mcversions.net", fg="blue", cursor="hand2", font = ('Arial', 12), justify="left")
lbl.pack(anchor="w", padx=10)
lbl.bind("<Button-1>", lambda e: callback("https://mcversions.net"))

lbl = tk.Label(frame1, text = "2. Move the downloaded jar file to the same location as this program.\nThe location of this program will also be the location of the server, so move\nthis program if needed.", font = ('Arial', 12), justify="left")
lbl.pack(anchor="w", pady=10)

lbl = tk.Label(frame1, text = "3. Setup the server, by clicking this button: ", font = ('Arial', 12), justify="left")
lbl.pack(anchor="w")

btn = tk.Button(frame1, text = "Server setup" , fg = "red", command=first_time_run, justify="left")
btn.pack(anchor="w", padx=10, pady=10)

lbl = tk.Label(frame1, text = "4. If you want players joining from outside your local network, you need to port forward\nthe ports specified in the server properties (query and server port). This has to be\ndone on your router,more info here:", font = ('Arial', 12), justify="left")
lbl.pack(anchor="w")
lbl = tk.Label(frame1, text="https://www.wikihow.com/Portforward-Minecraft", fg="blue", cursor="hand2", font = ('Arial', 12), justify="left")
lbl.pack(anchor="w", padx=10)
lbl.bind("<Button-1>", lambda e: callback("https://www.wikihow.com/Portforward-Minecraft"))

lbl = tk.Label(frame1, text = "5. The server setup is now done. Server properties, ops, whitelisted players and more\ncan be changed at the menus at the top. \n\nThe server can be started and stopped in the menu 'Start/stop'. \n\nIf you want to use a specific seed, you should add it\nin the server properties menu before starting the server.\n\nIf you want to change the seed after you started the server, you should delete the \nfolder 'world'. \nWARNING: Your current world will be deleted permanently.", font = ('Arial', 12), justify="left")
lbl.pack(anchor="w", pady=10)

################################################# Server properties #############################################################

def read_property(property):
    # Check if server.properties exists
    if not os.path.exists('server.properties'):
        return ' '
    with open('server.properties', 'r') as file:
        lines = file.readlines()

    for line in lines:
        # Check if line start with property and =
        if line.startswith(property + '='):
            # return the value after the =
            return line.split('=')[1].strip()

    return ' '

lbl = tk.Label(frame2, text="Edit server properties", font = ('Arial', 20), justify="left")
lbl.pack(anchor="w")

# Max memory
frame = tk.Frame(frame2)
lbl = tk.Label(frame, text = "Xmx (Max memory in MB):", font = ('Arial', 12))
lbl.pack(side=tk.LEFT)
xmx_entry = tk.Entry(frame)
xmx_entry.pack(side=tk.LEFT, padx=170)
xmx_entry.insert(0, xmx)
frame.pack(anchor="w")

# Initial memory
frame = tk.Frame(frame2)
lbl = tk.Label(frame, text = "Xms (Initial memory in MB):", font = ('Arial', 12))
lbl.pack(side=tk.LEFT)
xms_entry = tk.Entry(frame)
xms_entry.pack(side=tk.LEFT, padx=163)
xms_entry.insert(0, xms)
frame.pack(anchor="w")

# Difficulty
frame = tk.Frame(frame2)
lbl = tk.Label(frame, text = "Difficulty (easy/normal/hard):", font = ('Arial', 12))
lbl.pack(side=tk.LEFT)
difficulty_entry = tk.Entry(frame)
difficulty_entry.pack(side=tk.LEFT, padx=157)
difficulty_entry.insert(0, read_property('difficulty'))
frame.pack(anchor="w")

# Gamemode
frame = tk.Frame(frame2)
lbl = tk.Label(frame, text = "Gamemode (survival/creative/adventure/spectator):", font = ('Arial', 12))
lbl.pack(side=tk.LEFT)
gamemode_entry = tk.Entry(frame)
gamemode_entry.pack(side=tk.LEFT)
gamemode_entry.insert(0, read_property('gamemode'))
frame.pack(anchor="w")

# seed
frame = tk.Frame(frame2)
lbl = tk.Label(frame, text = "Seed:", font = ('Arial', 12))
lbl.pack(side=tk.LEFT)
seed_entry = tk.Entry(frame)
seed_entry.pack(side=tk.LEFT, padx=310)
seed_entry.insert(0, read_property('level-seed'))
frame.pack(anchor="w")

# max players
frame = tk.Frame(frame2)
lbl = tk.Label(frame, text = "Max players:", font = ('Arial', 12))
lbl.pack(side=tk.LEFT)
max_players_entry = tk.Entry(frame)
max_players_entry.pack(side=tk.LEFT, padx=265)
max_players_entry.insert(0, read_property('max-players'))
frame.pack(anchor="w")

# motd
frame = tk.Frame(frame2)
lbl = tk.Label(frame, text = "MOTD:", font = ('Arial', 12))
lbl.pack(side=tk.LEFT)
motd_entry = tk.Entry(frame)
motd_entry.pack(side=tk.LEFT, padx=302)
motd_entry.insert(0, read_property('motd'))
frame.pack(anchor="w")

# query port
frame = tk.Frame(frame2)
lbl = tk.Label(frame, text = "Query port:", font = ('Arial', 12))
lbl.pack(side=tk.LEFT)
query_port_entry = tk.Entry(frame)
query_port_entry.pack(side=tk.LEFT, padx=276)
query_port_entry.insert(0, read_property('query.port'))
frame.pack(anchor="w")

# server port
frame = tk.Frame(frame2)
lbl = tk.Label(frame, text = "Server port:", font = ('Arial', 12))
lbl.pack(side=tk.LEFT)
server_port_entry = tk.Entry(frame)
server_port_entry.pack(side=tk.LEFT, padx=271)
server_port_entry.insert(0, read_property('server-port'))
frame.pack(anchor="w")

# Simulation distance
frame = tk.Frame(frame2)
lbl = tk.Label(frame, text = "Simulation distance:", font = ('Arial', 12))
lbl.pack(side=tk.LEFT)
simulation_distance_entry = tk.Entry(frame)
simulation_distance_entry.pack(side=tk.LEFT, padx=212)
simulation_distance_entry.insert(0, read_property('simulation-distance'))
frame.pack(anchor="w")

# view distance
frame = tk.Frame(frame2)
lbl = tk.Label(frame, text = "View distance:", font = ('Arial', 12))
lbl.pack(side=tk.LEFT)
view_distance_entry = tk.Entry(frame)
view_distance_entry.pack(side=tk.LEFT, padx=250)
view_distance_entry.insert(0, read_property('view-distance'))
frame.pack(anchor="w")

# White list
frame = tk.Frame(frame2)
lbl = tk.Label(frame, text = "White list (true/false):", font = ('Arial', 12))
lbl.pack(side=tk.LEFT)
white_list_entry = tk.Entry(frame)
white_list_entry.pack(side=tk.LEFT, padx=208)
white_list_entry.insert(0, read_property('white-list'))
frame.pack(anchor="w")

# Button to save the properties
button_save = tk.Button(frame2, text="Save properties", command=lambda: save_properties())
button_save.pack(pady=14, padx=357, anchor="w")

lbl = tk.Label(frame2, text="If other properties need to be edited, edit the server.properties file.", font = ('Arial', 12), justify="left")
lbl.pack(anchor="w")

def save_properties():
    global xmx_entry, xms_entry, difficulty_entry, gamemode, level_name, seed, max_players, motd, query_port, server_port, simulation_distance, view_distance, white_list, xmx, xms
    xmx = xmx_entry.get()
    xms = xms_entry.get()
    with open('xmx.xms', 'w') as file:
        file.write('xmx=' + xmx + '\n')
        file.write('xms=' + xms + '\n')

    # Create shortcut to start server on boot
    

    # change start_server.bat file in startup folder if it exists
    username = os.getlogin()
    # Check if shortcut exists
    if os.path.exists('C:\\Users\\'+username+'\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\start_server.bat - Shortcut.lnk'):
        with open('C:\\Users\\'+username+'\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\start_server.bat - Shortcut.lnk', 'w') as file:
            file.write('java -Xmx' + xmx + 'M -Xms' + xms + 'M -jar server.jar nogui')
    else:
        # truncate username to 5 characters
        username_truncated = username[:5]
        if os.path.exists('C:\\Users\\'+username_truncated+'\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\start_server.bat - Shortcut.lnk'):
            with open('C:\\Users\\'+username_truncated+'\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\start_server.bat - Shortcut.lnk', 'w') as file:
                file.write('java -Xmx' + xmx + 'M -Xms' + xms + 'M -jar server.jar nogui')
        else:
            # create shortcut
            os.system('mklink /J "C:\\Users\\'+username_truncated+'\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\start_server.bat - Shortcut.lnk" "C:\\Users\\'+username_truncated+'\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\start_server.bat"')

        # Create shortcut with username untruncated
        os.system('mklink /J "C:\\Users\\'+username+'\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\start_server.bat - Shortcut.lnk" "C:\\Users\\'+username+'\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\start_server.bat"')

    # Change properties only if the entry is not empty
    if difficulty_entry.get() != '':
        difficulty = difficulty_entry.get()
        edit_properties('difficulty', difficulty)
    if gamemode_entry.get() != '':
        gamemode = gamemode_entry.get()
        edit_properties('gamemode', gamemode)
        level_name = 'world'
        edit_properties('level-name', level_name)
    if seed_entry.get() != '':
        seed = seed_entry.get()
        edit_properties('level-seed', seed)
    if max_players_entry.get() != '':
        max_players = max_players_entry.get()
        edit_properties('max-players', max_players)
    if motd_entry.get() != '':
        motd = motd_entry.get()
        edit_properties('motd', motd)
    if query_port_entry.get() != '':
        query_port = query_port_entry.get()
        edit_properties('query-port', query_port)
    if server_port_entry.get() != '':
        server_port = server_port_entry.get()
        edit_properties('server-port', server_port)
    if simulation_distance_entry.get() != '':
        simulation_distance = simulation_distance_entry.get()
        edit_properties('simulation-distance', simulation_distance)
    if view_distance_entry.get() != '':
        view_distance = view_distance_entry.get()
        edit_properties('view-distance', view_distance)
    if white_list_entry.get() != '':
        white_list = white_list_entry.get()
        edit_properties('white-list', white_list)

    messagebox.showinfo("Properties saved", "Properties saved successfully, restart server to apply")

# Edit the properties in the server.properties file
def edit_properties(property, value):
    remove_old_value(property) 

    with open('server.properties', 'r') as file:
        filedata = file.read()

    filedata = filedata + property + '=' + value + '\n'
    with open('server.properties', 'w') as file:
        file.write(filedata)

def remove_old_value(property):
    with open('server.properties', 'r') as file:
        lines = file.readlines()

    # filter out lines that only have property before =
    filtered_lines = [line for line in lines if not line.startswith(property + '=')]
    
    # Write the filtered lines back to the file
    with open('server.properties', 'w') as file:
        file.writelines(filtered_lines)


############################################# OP #################################################################

def get_uuid(player_name):
    import requests
    response = requests.get('https://api.mojang.com/users/profiles/minecraft/' + player_name)
    if response.status_code == 200:
        uuid = response.json()['id']
        return uuid[:8] + '-' + uuid[8:12] + '-' + uuid[12:16] + '-' + uuid[16:20] + '-' + uuid[20:]
    else:
        return 'Error'

def add_op():
    player_name = add_op_entry.get()
    if player_name == '':
        messagebox.showerror("Error", "Please fill in a player name")
        return

    # If file does not exist, create it
    if not os.path.exists('ops.json'):
        with open('ops.json', 'w') as file:
            file.write('[]')

    with open('ops.json', 'r') as file:
        lines = file.readlines()

    # Check if player is already an op
    for line in lines:
        if player_name in line:
            messagebox.showerror("Error", "Player is already an op")
            return

    # get uuid of player using mc api
    uuid = get_uuid(player_name)
   
    # check if there is already an op
    if lines[-1] != '[]':
        # remove last line from ops.json
        lines[-1] = lines[-1][:-2]
        with open('ops.json', 'w') as file:
            file.writelines(lines)
        
        # Add player as op
        with open('ops.json', 'a') as file:
            file.write(',\n{"uuid":"' + uuid + '","name":"' + player_name + '","level":4,"bypassesPlayerLimit": false}]\n')
    else:
        # Add player as op
        with open('ops.json', 'w') as file:
            file.write('[\n{"uuid":"' + uuid + '","name":"' + player_name + '","level":4,"bypassesPlayerLimit": false}]\n')

    messagebox.showinfo("Op added", "Player added as op successfully, restart server to apply")

    show_players('ops.json', ops_names_frame, frame3)

def remove_player(filename, player_name_entry, nameframe, frame):
    player_name = player_name_entry.get()
    if player_name == '':
        messagebox.showerror("Error", "Please fill in a player name")
        return

    with open(filename, 'r') as file:
        lines = file.readlines()

    # Check if player is already an op
    for line in lines:
        if player_name in line:
            lines.remove(line)
            if lines[0] == '[\n' and len(lines) == 1:
                with open(filename, 'w') as file:
                    file.write('[]')
            # if last character is , replace with ]
            elif len(lines[-1]) > 2:
                if lines[-1][-2] == ',':
                    lines[-1] = lines[-1][:-2] + ']\n'
                    with open(filename, 'w') as file:
                        file.writelines(lines)
                else:
                    with open(filename, 'w') as file:
                        file.writelines(lines)
            else:
                with open(filename, 'w') as file:
                    file.writelines(lines)
            messagebox.showinfo("Payer removed", "Player removed successfully, restart server to apply")
            show_players(filename, nameframe, frame)
            return
        
    messagebox.showerror("Error", "Player is not in the list")

lbl = tk.Label(frame3, text="Add/remove ops", font = ('Arial', 20), justify="left")
lbl.pack(anchor="w")

# Add op
frame = tk.Frame(frame3)
lbl = tk.Label(frame, text = "Add player (fill in player name): ", font = ('Arial', 12))
lbl.pack(side=tk.LEFT)
add_op_entry = tk.Entry(frame)
add_op_entry.pack(side=tk.LEFT, padx=30)
frame.pack(anchor="w")

# Button to add op
button_add_op = tk.Button(frame3, text="Add op", command=lambda: add_op())
button_add_op.pack(pady=10, anchor="w")

# Remove op
frame = tk.Frame(frame3)
lbl = tk.Label(frame, text = "Remove player (fill in player name): ", font = ('Arial', 12))
lbl.pack(side=tk.LEFT)
remove_op_entry = tk.Entry(frame)
remove_op_entry.pack(side=tk.LEFT, padx=1)
frame.pack(anchor="w")

# Button to remove op
button_remove_op = tk.Button(frame3, text="Remove op", command=lambda: remove_player('ops.json', remove_op_entry, ops_names_frame, frame3))
button_remove_op.pack(pady=10, anchor="w")

def show_players(filename, nameframe, frame):
    for widget in nameframe.winfo_children():
        widget.destroy()

    # If file does not exist, create it
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            file.write('[]')

    with open(filename, 'r') as file:
        lines = file.readlines()

    if lines[0] != '[]':
        for line in lines:
            if 'name' in line:
                # get username after name string
                name = line.split('"name":')[1].split('"')[1]
                lbl = tk.Label(nameframe, text=name, font = ('Arial', 12), justify="left")
                lbl.pack(anchor="w")
    nameframe.pack(anchor="w")

# Show current ops
lbl = tk.Label(frame3, text="Current ops", font = ('Arial', 20), justify="left")
lbl.pack(anchor="w")
ops_names_frame = tk.Frame(frame3)
show_players('ops.json', ops_names_frame, frame3)

############################################### Whitelist ###############################################################

def add_player(filename, player_name_entry, nameframe, frame):
    player_name = player_name_entry.get()
    if player_name == '':
        messagebox.showerror("Error", "Please fill in a player name")
        return

    # If file does not exist, create it
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            file.write('[]')

    with open(filename, 'r') as file:
        lines = file.readlines()

    # Check if player is already in file
    for line in lines:
        if player_name in line:
            messagebox.showerror("Error", "Player is already on the list")
            return

    # get uuid of player using mc api
    uuid = get_uuid(player_name)
   
    # check if there is already a player on the list
    if lines[-1] != '[]':
        # remove ] from file
        lines[-1] = lines[-1][:-2]
        with open(filename, 'w') as file:
            file.writelines(lines)
        
        # Add player as whitelisted
        with open(filename, 'a') as file:
            file.write(',\n{"uuid":"' + uuid + '","name":"' + player_name + '"}]\n')
    else:
        # Add player as whitelisted
        with open(filename, 'w') as file:
            file.write('[\n{"uuid":"' + uuid + '","name":"' + player_name + '"}]\n')

    messagebox.showinfo("List updated", "Player added to list successfully, restart server to apply")

    show_players(filename, nameframe, frame)

lbl = tk.Label(frame4, text="Add/remove whitelisted players", font = ('Arial', 20), justify="left")
lbl.pack(anchor="w")

# Add player
frame = tk.Frame(frame4)
lbl = tk.Label(frame, text = "Add player (fill in player name): ", font = ('Arial', 12))
lbl.pack(side=tk.LEFT)
add_player_entry = tk.Entry(frame)
add_player_entry.pack(side=tk.LEFT, padx=30)
frame.pack(anchor="w")

# Button to add player
button_add_player = tk.Button(frame4, text="Add player to whitelist", command=lambda: add_player('whitelist.json', add_player_entry, whitelisted_names_frame, frame4))
button_add_player.pack(pady=10, anchor="w")

# Remove player
frame = tk.Frame(frame4)
lbl = tk.Label(frame, text = "Remove player (fill in player name): ", font = ('Arial', 12))
lbl.pack(side=tk.LEFT)
remove_player_entry = tk.Entry(frame)
remove_player_entry.pack(side=tk.LEFT, padx=1)
frame.pack(anchor="w")

# Button to remove player
button_remove_player = tk.Button(frame4, text="Remove player from whitelist", command=lambda: remove_player('whitelist.json', remove_player_entry, whitelisted_names_frame, frame4))
button_remove_player.pack(pady=10, anchor="w")

# Show current whitelisted players
lbl = tk.Label(frame4, text="Current whitelisted players", font = ('Arial', 20), justify="left")
lbl.pack(anchor="w")
whitelisted_names_frame = tk.Frame(frame4)
show_players('whitelist.json', whitelisted_names_frame, frame4)

############################################ Banned players ##################################################################

lbl = tk.Label(frame5, text="Add/remove banned players", font = ('Arial', 20), justify="left")
lbl.pack(anchor="w")

# Add player
frame = tk.Frame(frame5)
lbl = tk.Label(frame, text = "Add player (fill in player name): ", font = ('Arial', 12))
lbl.pack(side=tk.LEFT)
add_banned_player_entry = tk.Entry(frame)
add_banned_player_entry.pack(side=tk.LEFT, padx=30)
frame.pack(anchor="w")

# Button to add player
button_add_player = tk.Button(frame5, text="Add player to banned list", command=lambda: add_player('banned-players.json', add_banned_player_entry, banned_names_frame, frame5))
button_add_player.pack(pady=10, anchor="w")

# Remove player
frame = tk.Frame(frame5)
lbl = tk.Label(frame, text = "Remove player (fill in player name): ", font = ('Arial', 12))
lbl.pack(side=tk.LEFT)
remove_banned_player_entry = tk.Entry(frame)
remove_banned_player_entry.pack(side=tk.LEFT, padx=1)
frame.pack(anchor="w")

# Button to remove player
button_remove_player = tk.Button(frame5, text="Remove player from banned list", command=lambda: remove_player('banned-players.json', remove_banned_player_entry, banned_names_frame, frame5))
button_remove_player.pack(pady=10, anchor="w")

# Show current banned players
lbl = tk.Label(frame5, text="Current banned players", font = ('Arial', 20), justify="left")
lbl.pack(anchor="w")
banned_names_frame = tk.Frame(frame5)
show_players('banned-players.json', banned_names_frame, frame5)

############################################## Start/stop server ################################################################

server_started = False
def start_server():
    global server_process, server_started
    print('Starting server')

    if server_started:
        messagebox.showerror("Error", "Server is already running")
        return
    server_process = subprocess.Popen(['java', '-Xmx' + str(xmx) + 'M', '-Xms'+ str(xms) + 'M', '-jar', 'server.jar', 'nogui'])
    server_started = True

def stop_server():
    global server_started
    print('Stopping server')

    if server_started:
        server_process.terminate()
        server_started = False

        # if server was started on boot, find the running process and kill it
        output = os.system('taskkill /f /im java.exe')

def autostart():
    # Create a batch file that starts the server
    with open('start_server.bat', 'w') as file:
        file.write('java -Xmx' + str(xmx) + 'M -Xms' + str(xms) + 'M -jar server.jar nogui')

    # create shortcut of batch file in startup folder
    username = os.getlogin()
    # Check if shortcut exists
    if os.path.exists('C:\\Users\\'+username+'\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\start_server.bat - Shortcut.lnk'):
        with open('C:\\Users\\'+username+'\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\start_server.bat - Shortcut.lnk', 'w') as file:
            file.write('java -Xmx' + str(xmx) + 'M -Xms' + str(xms) + 'M -jar server.jar nogui')
    else:
        # truncate username to 5 characters
        username_truncated = username[:5]
        if os.path.exists('C:\\Users\\'+username_truncated+'\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\start_server.bat - Shortcut.lnk'):
            with open('C:\\Users\\'+username_truncated+'\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\start_server.bat - Shortcut.lnk', 'w') as file:
                file.write('java -Xmx' + str(xmx) + 'M -Xms' + str(xms) + 'M -jar server.jar nogui')
        else:
            # create shortcut
            shell = Dispatch('WScript.Shell')
            path = 'C:\\Users\\'+username_truncated+'\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\start_server.bat - Shortcut.lnk'
            shortcut = shell.CreateShortCut(path)
            # get current path
            path = os.getcwd()
            # set target path
            shortcut.Targetpath = path + '\\start_server.bat'
            # start in location of start_server.bat
            shortcut.WorkingDirectory = path
            shortcut.save()

        # create shortcut
        shell = Dispatch('WScript.Shell')
        path = 'C:\\Users\\'+username+'\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\start_server.bat - Shortcut.lnk'
        shortcut = shell.CreateShortCut(path)
        # get current path
        path = os.getcwd()
        # set target path
        shortcut.Targetpath = path + '\\start_server.bat'
        # start in location of start_server.bat
        shortcut.WorkingDirectory = path
        shortcut.save()
        
def remove_autostart():
    username = os.getlogin()
    output = os.system('del "C:\\Users\\'+username+'\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\start_server.bat - Shortcut.lnk"')
    if output == 0:
        messagebox.showinfo("Server will not start on boot", "Server will not start on boot")
    else:
        # truncate username to 5 characters
        username = username[:5]
        output = os.system('del "C:\\Users\\'+username+'\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\start_server.bat - Shortcut.lnk"')
        if output == 0:
            messagebox.showinfo("Server will not start on boot", "Server will not start on boot")
        else:
            messagebox.showerror("Error", "Could not delete file from startup folder, please delete manually")

lbl = tk.Label(frame6, text="Start/stop server", font = ('Arial', 20), justify="left")
lbl.pack(anchor="w")
button_start = tk.Button(frame6, text="Start server", command=lambda: start_server())
button_start.pack(anchor="w", pady=10, padx=10)
button_stop = tk.Button(frame6, text="Stop server", command=lambda: stop_server())
button_stop.pack(anchor="w", pady=10, padx=10)
button_autostart = tk.Button(frame6, text="Start server on boot", command=lambda: autostart())
button_autostart.pack(anchor="w", pady=10, padx=10)
button_remove_autostart = tk.Button(frame6, text="Remove server from boot", command=lambda: remove_autostart())
button_remove_autostart.pack(anchor="w", pady=10, padx=10)

##############################################################################################################

# Add menu options for navigation
menu_bar.add_command(label="Setup", command=lambda: show_frame(frame1))
menu_bar.add_command(label="Server properties", command=lambda: show_frame(frame2))
menu_bar.add_command(label="Ops", command=lambda: show_frame(frame3))
menu_bar.add_command(label="Whitelist", command=lambda: show_frame(frame4))
menu_bar.add_command(label="Banned players", command=lambda: show_frame(frame5))
menu_bar.add_command(label="Start/stop", command=lambda: show_frame(frame6))

# Configure the menu bar
root.config(menu=menu_bar)

# Show the first frame initially
show_frame(frame1)

# Start the main loop
root.mainloop()
