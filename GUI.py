from tkinter import *
from tkinter import font, ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import cardAI, gptConnect, time, threading


root = Tk()
root.title("CardAI")

generating = False

#Frames
radioframe_prompt = Frame(root)
radioframe_prompt.grid(row = 1, column = 0)
frame_prompt = Frame(root)
frame_prompt.grid(row = 2, column = 0)
frame_deck = Frame(root)
file_deck = Frame(root)
frame_bottom = Frame(root)
frame_bottom.grid(row = 4, column = 0)

def select():
    if not generating:
        enable_disable_button()
        if choice.get() == 0:
            frame_prompt.grid(row = 2, column = 0)
            frame_deck.grid_forget()
        elif choice.get() == 1:
            frame_prompt.grid_forget()
            frame_deck.grid(row = 2, column = 0)

def makeImage():
    generating = True
    if choice.get() == 0:
        p_bar.start(130 + 130 * v_aiImage.get())
        cardAI.image(gptConnect.getMagicCard(e_prompt.get()), hasImage = bool(v_aiImage.get()), output = e_fileName.get().replace(".png","").replace(".jpg",""))
    elif choice.get() == 1:
        #print(file_path)
        #print(s_deck.get("1.0", END))
        prompts = s_deck.get("1.0", END).split("\n")[:-1]
        #print(len(prompts))
        i = 0
        for i in range(len(prompts)):
            try:
                p_bar["value"] = 100 * (1.0 * i / len(prompts))
                #print("Generating " + prompt)
                cardAI.image(gptConnect.getMagicCard("Name - " + prompts[i]), hasImage = bool(v_aiImage.get()), output = file_path + "/" + str(i) + " - " + prompts[i].replace("/", "-").replace("\\","-"))
            except Exception as error:
                print(error)
                i -= 1
                continue


    b_generate.config(state=NORMAL)
    rb_Prompt.config(state=NORMAL)
    rb_DeckPaste.config(state=NORMAL)
    
    generating = False
    p_bar.stop()
    p_bar.grid_forget()

def generate():
    p_bar.grid(row = 3, column = 0)
    b_generate.config(state=DISABLED)
    rb_Prompt.config(state=DISABLED)
    rb_DeckPaste.config(state=DISABLED)
    command_thread = threading.Thread(target=makeImage)
    command_thread.start()
            
#Progressbar

p_bar = ttk.Progressbar(root, mode = "determinate", length = 300)
#p_bar
#p_bar.grid(row = 3, column = 0)

#Radio Button Prompts
choice = IntVar()
rb_Prompt = Radiobutton(radioframe_prompt, command = select, variable = choice, value = 0, text = "Card Prompt")
rb_DeckPaste = Radiobutton(radioframe_prompt, command = select, variable = choice, value = 1, text = "Deck Prompt")
rb_Prompt.grid(row = 0, column = 0)
rb_DeckPaste.grid(row = 0, column = 1)


#Title Label
f_titleFont = font.Font(family="Helvetica", size=20)
l_title = Label(root, text = "CardAI", font = f_titleFont)
l_title.grid(row = 0, column = 0, sticky = "nsew")


def enable_disable_button(*args):
    if choice.get() == 0:
        if v_prompt.get() and v_fileName.get():
            b_generate.config(state=NORMAL)  # Enable the button
        else:
            b_generate.config(state=DISABLED)  # Disable the button
    elif choice.get() == 1:
        if file_path:
            b_generate.config(state=NORMAL)  # Enable the button
        else:
            b_generate.config(state=DISABLED)  # Disable the button

#Text Prompt===================================================

l_prompt = Label(frame_prompt, text = "Card Prompt: ")
l_prompt.grid(row = 0, column = 0)
v_prompt = StringVar()
e_prompt = Entry(frame_prompt, textvariable=v_prompt)
e_prompt.grid(row = 0, column = 1)
v_prompt.trace("w", enable_disable_button)

l_file = Label(frame_prompt, text = "Output Name: ")
l_file.grid(row = 1, column = 0)
v_fileName = StringVar()
e_fileName = Entry(frame_prompt, textvariable=v_fileName)
e_fileName.grid(row = 1, column = 1)
v_fileName.trace("w", enable_disable_button)

#Deck Prompt==================================================

l_deck = Label(frame_deck, text = "Enter each prompt, seperated by lines")
l_deck.grid(row = 0, column = 0)
s_deck = ScrolledText(frame_deck, width = 50, height = 10)
s_deck.grid(row = 1, column = 0)

def getFolder():
    global file_path
    file_path = filedialog.askdirectory()
    if file_path:
        l_folder.config(text = file_path.split("/")[-1])
    else:
        l_folder.config(text = "Select Output Folder")
    enable_disable_button()

subFrame = Frame(frame_deck)
subFrame.grid(row = 2, column = 0)

file_path = ""
b_folder = Button(subFrame, text = "Select Output Folder", command = getFolder)
b_folder.grid(row = 1, column = 1)
l_folder = Label(subFrame, text = "Select Output Folder")
l_folder.grid(row = 1, column = 0)

def loadFromFile():
    filetypes = (("Text files", "*.txt"), ("All files", "*.*"))
    
    s_deck.delete("1.0", END)
    loadFilePath = filedialog.askopenfilename(filetypes=filetypes)
    if loadFilePath == "":
        return

    try:
        with open(loadFilePath, "r") as f:
            s_deck.insert(END, f.read())
    except:
        messagebox.showerror(title="Error", message="Unable to read text from file")
        

b_file = Button(subFrame, text = "Load from File", command = loadFromFile)
b_file.grid(row = 1, column = 2)

#Bottom======================================================
v_aiImage = IntVar()
c_aiImage = Checkbutton(frame_bottom, text='Use AI Image', variable = v_aiImage)
c_aiImage.grid(row = 4, column = 1)

b_generate = Button(frame_bottom, text = "Generate", command = generate, state=DISABLED)
b_generate.grid(row = 4, column = 0)












root.mainloop()
