from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import customtkinter as ct
from tkinter import *
from tkinter import messagebox

# Load environment variables
load_dotenv()
API = os.getenv('groq_API')

# ---------------- GUI Setup ---------------- #

ct.set_appearance_mode("System")
ct.set_default_color_theme("dark-blue")

root = ct.CTk()
root.title("Comic Story Generator")
root.geometry("1080x720")

# ---------------- Functions ---------------- #

def story_Gen_GUI():
    genre = genre_entry.get()
    character = character_entry.get()
    length = length_var.get()

    if not genre or not character:
        output_textbox.delete("1.0", END)
        output_textbox.insert("1.0", "❗ Please enter both genre and main character ❗")
        return

    try:
        llm = ChatGroq(
            temperature=1.2,
            groq_api_key=API,
            model_name="gemma2-9b-it"
        )
        
        context = (
            f"The user has entered a {length.lower()} comic story. "
            f"Genre: {genre}. Main Character: {character}. "
            f"Write a creative story based on this without asking any questions."
        )
        response = llm.invoke(context)
        output_textbox.delete("1.0", END)
        output_textbox.insert("1.0", response.content)
    except Exception as e:
        output_textbox.delete("1.0", END)
        output_textbox.insert("1.0", f"⚠ Error:\n{str(e)}")

def clear_fields():
    genre_entry.delete(0, END)
    character_entry.delete(0, END)
    output_textbox.delete("1.0", END)

def save_story():
    story = output_textbox.get("1.0", END).strip()
    if not story:
        messagebox.showwarning("Nothing to Save", "There's no story to save.")
        return
    with open("generated_story.txt", "w", encoding="utf-8") as file:
        file.write(story)
    messagebox.showinfo("Saved", "Story saved to generated_story.txt ✅")

# ---------------- Widgets ---------------- #

heading = ct.CTkLabel(root, text="⚡ AI GEN ⚡", font=("Small Fonts", 48, "bold"))
heading.pack(pady=5)

# Genre
genre_label = ct.CTkLabel(root, text="Enter Genre(s):", font=("Helvetica", 20, "italic"))
genre_label.pack(pady=5)
genre_entry = ct.CTkEntry(root, width=400, height=40, font=("Helvetica", 16, "italic"))
genre_entry.pack(pady=5)
genre_entry.bind("<Return>", lambda event: story_Gen_GUI())

# Character
character_label = ct.CTkLabel(root, text="Enter Main Character:", font=("Helvetica", 20, "italic"))
character_label.pack(pady=5)
character_entry = ct.CTkEntry(root, width=400, height=40, font=("Helvetica", 16, "italic"))
character_entry.pack(pady=5)
character_entry.bind("<Return>", lambda event: story_Gen_GUI())

# Length dropdown
length_label = ct.CTkLabel(root, text="Select Story Length:", font=("Helvetica", 20, "italic"))
length_label.pack(pady=10)

length_var = ct.StringVar(value="Medium")
length_menu = ct.CTkOptionMenu(root, variable=length_var, values=["Short", "Medium", "Epic"])
length_menu.pack(pady=5)

# Buttons
generate_btn = ct.CTkButton(root, text="Generate Story", command=story_Gen_GUI)
generate_btn.pack(pady=10)

clear_btn = ct.CTkButton(root, text="Clear", command=clear_fields)
clear_btn.pack(pady=5)

save_btn = ct.CTkButton(root, text="💾 Save Story", command=save_story)
save_btn.pack(pady=5)

# Output
output_label = ct.CTkLabel(root, text="Generated Story:", font=("Helvetica", 20, "italic"))
output_label.pack(pady=10)

output_textbox = ct.CTkTextbox(root, width=800, height=350, font=("Times New Roman", 16), wrap="word")
output_textbox.pack(pady=10)

# Credits
mark_label = ct.CTkLabel(root, text="By : Arijeet Kurse \n Division: D", font=("Times New Roman", 16, "italic"))
mark_label.pack(padx=20, pady=10, anchor="w")

# ---------------- Run GUI ---------------- #

root.mainloop()
