import tkinter as tk
import random
from tkinter import PhotoImage, ttk
from PIL import Image, ImageTk, ImageSequence
import os

'''
Accuracy:
Score for Accuracy = (Actual Accuracy / 100) * 40

Consistency:
Score for Consistency = (Actual Consistency / 100) * 30

Time of Completion:
Score for Time = (Maximum Time / Actual Time) * 20

Words Per Minute:
Score for WPM = (Actual WPM / Maximum WPM) * 10
'''

resultFrame = None
dpRanks = None
critWindow = None

def displayCriteria():
    global critWindow, crit_text
    # Destroy the current window or frame
    home.destroy()

    # Create a new window
    critWindow = tk.Frame(window)
    critWindow.pack()

    criteria = '''
    Accuracy:
    Score for Accuracy = (Actual Accuracy / 100) * 40

    Consistency:
    Score for Consistency = (Actual Consistency / 100) * 30

    Time of Completion:
    Score for Time = (Maximum Time / Actual Time) * 20

    Words Per Minute:
    Score for WPM = (Actual WPM / Maximum WPM) * 10
    '''

    # Create a Text widget to display the criteria
    crit_text = tk.Text(window, wrap=tk.WORD)
    crit_text.pack(fill='both', expand=True)

    crit_text.tag_configure("center", justify="center")
    crit_text.tag_add("center", "1.0", "end")

    # Insert the criteria into the Text widget
    crit_text.insert("1.0", criteria)

    # Disable text editing (optional)
    crit_text.config(state=tk.DISABLED)


    back_button = tk.Button(critWindow, text="<- Back",  borderwidth=5, bg="cyan", font=("Exo 2 Medium", 12), width=20, command=Homescreen)
    back_button.pack(side="bottom")


def displayRanks():
    global dpRanks
    home.destroy()
    rank = 1
    headers = ['Ranking','Participant ID', 'Name', 'Accuracy', 'Consistency', 'WPM', 'Time', 'Total Score']

    dpRanks = tk.Frame(window)
    dpRanks.pack()
    style = ttk.Style()
    style.configure("Ranking.TLabel", background='#F6DAE4', font=("Exo 2 Medium", 10))

    tk.Label(dpRanks, text="Result Meow!!!", font=("Franklin Gothic Demi Cond", 20), fg="#00C4D4").grid(row=0, column=0, columnspan=8, pady=10)

    for col, header in enumerate(headers):
        ttk.Label(dpRanks, text=header, style="Ranking.TLabel", width=10).grid(row=1, column=col, padx=2)

    for row, (participant, values) in enumerate(rankings):
        participant_data = participant.split(' -> ')
        participant_id = random.randint(101, 999)
        name = participant_data[1]
        values = [rank, participant_id, name] + values  # Include the name in the data
        rank+=1

        for col, value in enumerate(values):
            ttk.Label(dpRanks, text=value, style="Ranking.TLabel", width=10).grid(row=row + 2, column=col, padx=2, pady=5)
    
    backButton = tk.Button(dpRanks, text="<- Back",  borderwidth=5, bg="cyan", font=("Exo 2 Medium", 12), width=20, command=Homescreen)
    backButton.grid(row=len(rankings)+3, column=0, columnspan=8, pady=10)


def Homescreen():
    global home
    if resultFrame:
        resultFrame.destroy()
    if dpRanks:
        dpRanks.destroy()
    if critWindow:
        critWindow.destroy()
        crit_text.destroy()

    home = tk.Frame(window)
    home.pack()

    calculateScores = tk.Button(home, text="Calculate Scores", borderwidth=5, bg="cyan", font=("Exo 2 Medium", 12), command=calculateScoreButton, width=20, height=1)
    seeRankings = tk.Button(home, text="See Rankings",borderwidth=5, bg="cyan", font=("Exo 2 Medium", 12), command=displayRanks, width=20, height=1)
    seeScoringMetrics = tk.Button(home, text="See Scoring Metrics", borderwidth=5, bg="cyan", font=("Exo 2 Medium", 12),command=displayCriteria , width=20, height=1)

    calculateScores.pack(pady=15)
    seeRankings.pack(pady=15)
    seeScoringMetrics.pack(pady=15)


def calculateRankings(ptEntry=None, event=None):
    global resultFrame, rankings
    rankings = {}
    rank = 1
    headers = ['Ranking','Participant ID', 'Name', 'Accuracy', 'Consistency', 'WPM', 'Time', 'Total Score']
    
    resultFrame = tk.Frame(window)
    resultFrame.pack()

    style = ttk.Style()
    style.configure("Ranking.TLabel", background='#F6DAE4', font=("Exo 2 Medium", 10))

    tk.Label(resultFrame, text="Result Meow!!!", font=("Franklin Gothic Demi Cond", 20), fg="#00C4D4").grid(row=0, column=0, columnspan=8, pady=10)

    for ptID, stats in ptEntry.items():
        resAccuracy = (float(stats[1]) / 100) * 45
        resConsistency = (float(stats[2]) / 100) * 35
        resWPM = (float(stats[4]) / 100) * 20
        totalScore = round(resAccuracy + resConsistency + resWPM, 2)
        rankings[f'{ptID} -> {stats[0]}'] = ["{:.2f}".format(resAccuracy), "{:.2f}".format(resConsistency), "{:.2f}".format(resWPM), stats[3] ,totalScore]
    
    rankings = sorted(rankings.items(), key=lambda score : score[1][4], reverse=True)

    for col, header in enumerate(headers):
        ttk.Label(resultFrame, text=header, style="Ranking.TLabel", width=10).grid(row=1, column=col, padx=2)

    for row, (participant, values) in enumerate(rankings):
        participant_data = participant.split(' -> ')
        participant_id = random.randint(101, 999)
        name = participant_data[1]
        values = [rank, participant_id, name] + values  # Include the name in the data
        rank+=1

        for col, value in enumerate(values):
            ttk.Label(resultFrame, text=value, style="Ranking.TLabel", width=10).grid(row=row + 2, column=col, padx=2, pady=5)
    
    backButton = tk.Button(resultFrame, text="<- Back",  borderwidth=5, bg="cyan", font=("Exo 2 Medium", 12), width=20, command=Homescreen)
    backButton.grid(row=len(rankings)+3, column=0, columnspan=8, pady=10)

def result(event=None):
    for participants in range(2, participantsNumber + 2):
        pstats = []
        for stats in range(0, 5):
            pstats.append(participant_entries[f'Participant_{participants-1}'][stats].get())
        ptStatistics[f'Participant_{participants-1}'] = pstats

    calculateRankings(ptStatistics)

    participantsFrame.destroy()

def inputParticipants(event=None):
    global ptStatistics, participants, participantsNumber, participant_entries, resultbtn, participantsFrame
    
    participantsNumber = int(nParticipantsEntry.get())

    ptStatistics = {}
    participant_entries = {}

    participantsFrame = tk.Frame(window)
    participantsFrame.pack()

    

    title = tk.Label(participantsFrame, text="Enter the Participants Name and their Speed Test Result", font=("Franklin Gothic Demi Cond", 20), fg="#00C4D4")
    title.grid(row=0, column=0, columnspan=5)

    pName = tk.Label(participantsFrame, text="Name", font=("Exo 2 Medium", 10), bg='#F6DAE4', borderwidth=1)
    pName.grid(row=1, column=0)
    pAccuracy = tk.Label(participantsFrame, text="Accuracy (%)", font=("Exo 2 Medium", 10), bg='#F6DAE4', borderwidth=1)
    pAccuracy.grid(row=1, column=1)
    pConsistency = tk.Label(participantsFrame, text="Consistency (%)", font=("Exo 2 Medium", 10), bg='#F6DAE4', borderwidth=1)
    pConsistency.grid(row=1, column=2)
    pTC = tk.Label(participantsFrame, text="T.C (s)", font=("Exo 2 Medium", 10), bg='#F6DAE4', borderwidth=1)
    pTC.grid(row=1, column=3)
    pWPM = tk.Label(participantsFrame, text="W.P.M", font=("Exo 2 Medium", 10), bg='#F6DAE4',  borderwidth=1)
    pWPM.grid(row=1, column=4)

    for participants in range(2, participantsNumber+2):
        pstats = []
        for stats in range(0, 5):
            info = tk.Entry(participantsFrame, font=("Roboto Serif 36pt Light", 10), bg="#D4F0F7", borderwidth=1)
            info.grid(row=participants, column=stats, pady=2)
            pstats.append(info)
        participant_id = f'Participant_{participants-1}'
        ptStatistics[participant_id] = []
        participant_entries[participant_id] = pstats

    resultbtn = tk.Button(participantsFrame, text="Give me Meow!!", borderwidth=5, bg="cyan", font=("Exo 2 Medium", 12), command=result)
    resultbtn.grid(row=participants+1, column=0, columnspan=5, pady=10)

    entryFrame.destroy()

def calculateScoreButton():
    global entryFrame, nParticipantsEntry

    home.destroy()
    
    entryFrame = tk.Frame(window)
    entryFrame.pack(pady=10)
    
    nParticipants = tk.Label(entryFrame, text="Number of Participants:", font=("Exo 2 Medium", 12))
    nParticipantsEntry = tk.Entry(entryFrame, font=("Roboto Serif 36pt Light", 12), bg="#D4F0F7", borderwidth=1)
    nParticipants.grid(row=0, column=0)
    nParticipantsEntry.grid(row=0, column=1, padx=7)

    doneButton = tk.Button(entryFrame, text="(Meow Meow) Done!", borderwidth=5, bg="cyan", font=("Exo 2 Medium", 12) , command=inputParticipants)
    doneButton.grid(row=1, column=0, columnspan=2, pady=10)

    nParticipantsEntry.bind("<Return>", inputParticipants)

window = tk.Tk()
window.title("Speed Typing Scoring Calculator")
windowW = 800
windowH = 700
screenH = window.winfo_screenheight()
screenW = window.winfo_screenwidth()
window.geometry(f"{windowW}x{windowH}+{(screenW - windowW) // 2}+{((screenH - 40)  - windowH) // 2}")
# window.resizable(width=False, height=False)


backgroundImage = PhotoImage(file="./link.png")
backgroundLabel = tk.Label(window, image=backgroundImage)
backgroundLabel.place(relheight=1, relwidth=1)

labelTitle = tk.Label(window, text="Speed Typing Scoring Metrics", anchor="center", justify="center", font=("Franklin Gothic Demi Cond", 30, "italic"), fg="#00C4D4")
labelTitle.pack(pady=30)

gif = Image.open('C:\\Users\\Student\\OneDrive\\Desktop\\Projects\\Algorithms\\speed_typing\\cat.gif')
frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif)]

def animate(count):
    gif_label.configure(image=frames[count])
    count = (count + 1) % len(frames)
    window.after(50, animate, count)

gif_label = tk.Label(window)
gif_label.pack()
animate(0)

Homescreen()

window.mainloop()
