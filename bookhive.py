import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# ---------- BookHive App Class ----------
class BookHiveApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BookHive")
        self.geometry("1600x900")
        self.configure(bg="#FFE4E1")
        self.book_data = self.get_book_data()
        self.images = []  # To prevent garbage collection
        self.create_main_ui()

    def create_main_ui(self):
        # --- Decorative Side Images ---
        img1 = Image.open("C:/Users/ADMIN/Downloads/book (2).jpg")
        img1 = img1.resize((300, 300))
        photo1 = ImageTk.PhotoImage(img1)
        label4 = tk.Label(self, image=photo1, bg="#FFE4E1")
        label4.place(x=100, y=20)

        img2 = Image.open("C:/Users/ADMIN/Downloads/book (1).jpg")
        img2 = img2.resize((300, 300))
        photo2 = ImageTk.PhotoImage(img2)
        label5 = tk.Label(self, image=photo2, bg="#FFE4E1")
        label5.place(x=1150, y=20)

        # Store image references
        self.images.extend([photo1, photo2])

        # --- Labels ---
        label1 = tk.Label(self, text="BookHive", font=("Arial", 75, "bold"), bg="#FFE4E1")
        label1.place(x=575, y=20)
        label2 = tk.Label(self, text="Welcome to the world of books!", font=("Bell MT", 38), fg="#4B0082", bg="#FFE4E1")
        label2.place(x=400, y=150)
        label3 = tk.Label(self, text="Find your next read:", font=("Bell MT", 38), bg="#FFE4E1")
        label3.place(x=550, y=250)

        # --- Filters ---
        self.genre_var = tk.StringVar()
        self.price_var = tk.StringVar()
        self.pages_var = tk.StringVar()

        genres = list(self.book_data.keys())
        genre_dropdown = ttk.Combobox(self, textvariable=self.genre_var, font=("Arial", 18), width=20)
        genre_dropdown['values'] = ["All"] + genres
        genre_dropdown.set("Select Genre")
        genre_dropdown.place(x=150, y=350)

        price_dropdown = ttk.Combobox(self, textvariable=self.price_var, font=("Arial", 18), width=20)
        price_dropdown['values'] = ["Any", "Below Rs.200", "Rs.200-Rs.500", "Above Rs.500"]
        price_dropdown.set("Select Price Range")
        price_dropdown.place(x=500, y=350)

        pages_dropdown = ttk.Combobox(self, textvariable=self.pages_var, font=("Arial", 18), width=20)
        pages_dropdown['values'] = ["All", "<200 pages", "200-400 pages", ">400 pages"]
        pages_dropdown.set("No of Pages")
        pages_dropdown.place(x=850, y=350)

        filter_btn = tk.Button(self, text="Apply Filters", font=("Arial", 20), command=self.apply_filters, bg="darkgreen", fg="white")
        filter_btn.place(x=1250, y=345)

        # --- Scrollable Canvas ---
        self.canvas_frame = tk.Frame(self, bg="#FFE4E1")
        self.canvas_frame.place(x=100, y=450, width=1400, height=400)

        self.canvas = tk.Canvas(self.canvas_frame, bg="#FFE4E1", width=1400, height=500)
        scrollbar = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollable_frame = tk.Frame(self.canvas, bg="#FFE4E1")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

    def clear_results(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def apply_filters(self):
        self.clear_results()
        selected_genre = self.genre_var.get()
        selected_price = self.price_var.get()
        selected_pages = self.pages_var.get()

        filtered_books = []

        for genre, books in self.book_data.items():
            if selected_genre != "All" and genre != selected_genre:
                continue
            for path, title, img_coords, txt_coords, price, pages in books:
                if selected_price == "Below Rs.200" and price >= 200:
                    continue
                elif selected_price == "Rs.200-Rs.500" and not (200 <= price <= 500):
                    continue
                elif selected_price == "Above Rs.500" and price <= 500:
                    continue

                if selected_pages == "<200 pages" and pages >= 200:
                    continue
                elif selected_pages == "200-400 pages" and not (200 <= pages <= 400):
                    continue
                elif selected_pages == ">400 pages" and pages <= 400:
                    continue

                filtered_books.append((path, title, price, pages))

        if not filtered_books:
            tk.Label(self.scrollable_frame, text="No matching books found.", font=("Arial", 18), bg="#FFE4E1").grid(row=0, column=0, padx=20, pady=20)
            return

        for i, (path, title, price, pages) in enumerate(filtered_books):
            try:
                img = Image.open(path).resize((140, 200))
                img_tk = ImageTk.PhotoImage(img)
            except:
                img_tk = None

            col = i % 7
            row = (i // 7)

            if img_tk:
                img_label = tk.Label(self.scrollable_frame, image=img_tk, bg="#FFE4E1")
                img_label.image = img_tk
                img_label.grid(row=row * 2, column=col, padx=20, pady=(10, 0), sticky="n")

            text = f"{title}\nRs.{price} | {pages} pages"
            desc_label = tk.Label(self.scrollable_frame, text=text, font=("Arial", 14), bg="#FFE4E1", wraplength=120, justify="center")
            desc_label.grid(row=row * 2 + 1, column=col, padx=20, pady=(0, 20), sticky="n")

    def get_book_data(self):
        # Return your original `book_data` dictionary here
        return {
            "Fiction": [
                ("C:/Users/ADMIN/Downloads/fiction-20250513T084917Z-1-001/fiction/blindsight.jpg", "Blindsight.", (100, 200), (100, 430),150, 175),
                ("C:/Users/ADMIN/Downloads/fiction-20250513T084917Z-1-001/fiction/coffee.jpg", "Before the Coffee gets Cold", (300, 200), (300, 430),280,300),
                ("C:/Users/ADMIN/Downloads/fiction-20250513T084917Z-1-001/fiction/mahashweta.jpg", "Mahashweta", (500, 200), (500, 430),380,200),
                ("C:/Users/ADMIN/Downloads/fiction-20250513T084917Z-1-001/fiction/redclock.jpg", "Red Clocks", (700, 200), (700, 430),550,450),
                ("C:/Users/ADMIN/Downloads/fiction-20250513T084917Z-1-001/fiction/thepower.jpg", "The Power", (900, 200), (900, 430),450,250),
                ("C:/Users/ADMIN/Downloads/fiction-20250513T084917Z-1-001/fiction/thealchemist.jpg", "The Alchemist", (1100, 200), (1100, 430),290,480),
                ("C:/Users/ADMIN/Downloads/fiction-20250513T084917Z-1-001/fiction/thesecretgarden.jpg", "The Secret Garden", (1300, 200), (1300, 430),600,700),

            ],
            "Mystery": [
                ("C:/Users/ADMIN/Downloads/mystery-20250513T084917Z-1-001/mystery/gggtm.jpg", "A Good Girl's Guide to Murder", (100, 200), (100, 430),350, 280),
                ("C:/Users/ADMIN/Downloads/mystery-20250513T084917Z-1-001/mystery/gielonthetrain.jpg", "Girl on the Train", (300, 200), (300, 430),180,180),
                ("C:/Users/ADMIN/Downloads/mystery-20250513T084917Z-1-001/mystery/gonegirl.jpg", "Gone Girl", (500, 200), (500, 430),480,250),
                ("C:/Users/ADMIN/Downloads/mystery-20250513T084917Z-1-001/mystery/murderonorientexp.jpg", "Murder on the Orient Express", (700, 200), (700, 430),500,350),
                ("C:/Users/ADMIN/Downloads/mystery-20250513T084917Z-1-001/mystery/sherlockholmes.jpg", "The Adventures of Sherlock Holmes", (900, 200), (900, 430),450,550),
                ("C:/Users/ADMIN/Downloads/mystery-20250513T084917Z-1-001/mystery/thehoundofbaserkvilles.jpg", "The Hound Of Baskervilles", (1100, 200), (1100, 430),290,190),
                ("C:/Users/ADMIN/Downloads/mystery-20250513T084917Z-1-001/mystery/rebecca.jpg", "Rebecca", (1300, 200), (1300, 430),170,370),
                
            ],
            "Children": [
                ("C:/Users/ADMIN/Downloads/kids-20250513T084917Z-1-001/kids/bagofstories.jpg", "Grandma's Bag of Stories", (100, 200), (100, 430),350, 280),
                ("C:/Users/ADMIN/Downloads/kids-20250513T084917Z-1-001/kids/famousfive.jpg", "The Famous Five", (300, 200), (300, 430),280,300),
                ("C:/Users/ADMIN/Downloads/kids-20250513T084917Z-1-001/kids/geronimo.jpg", "My Name is Stilton: Geronimo Stilton", (500, 200), (500, 430),680,700),
                ("C:/Users/ADMIN/Downloads/kids-20250513T084917Z-1-001/kids/lasttrainjourney.jpg", "the Great Train Journey", (700, 200), (700, 430),500,350),
                ("C:/Users/ADMIN/Downloads/kids-20250513T084917Z-1-001/kids/secretseven.jpg", "The Secret Seven", (900, 200), (900, 430),450,250),
                ("C:/Users/ADMIN/Downloads/kids-20250513T084917Z-1-001/kids/matilda.jpg", "Matilda", (1100, 200), (1100, 430),250,480),
                ("C:/Users/ADMIN/Downloads/kids-20250513T084917Z-1-001/kids/wimpykid.jpg", "The Diary of a Wimpy Kid", (1300, 200), (1300, 430),250,300),
            ],
            "Fantasy": [
                ("C:/Users/ADMIN/Downloads/fantasy-20250513T084918Z-1-001/fantasy/colorofmagic.jpg", "The Color Of Magic", (100, 200), (100, 430),100, 150),
                ("C:/Users/ADMIN/Downloads/fantasy-20250513T084918Z-1-001/fantasy/harrypotter.jpeg", "Harry Potter and the Prisoner of Azkaban", (300, 200), (300, 430),280,300),
                ("C:/Users/ADMIN/Downloads/fantasy-20250513T084918Z-1-001/fantasy/mockingbird.jpeg", "How to Kill a Mockingbird", (500, 200), (500, 430),580,700),
                ("C:/Users/ADMIN/Downloads/fantasy-20250513T084918Z-1-001/fantasy/northernlights.jpg", "Northern Lights", (700, 200), (700, 430),500,350),
                ("C:/Users/ADMIN/Downloads/fantasy-20250513T084918Z-1-001/fantasy/unicorn.jpg", "The Last Unicorn", (900, 200), (900, 430),450,250),
                ("C:/Users/ADMIN/Downloads/fantasy-20250513T084918Z-1-001/fantasy/The_Buried_Giant.png", "The Buried Giant", (1100, 200), (1100, 430),290,480),
                ("C:/Users/ADMIN/Downloads/fantasy-20250513T084918Z-1-001/fantasy/therageofdragons.jpg", "The Rage of Dragons", (1300, 200), (1300, 430),170,170),
            ],
            "Romance": [
                ("C:/Users/ADMIN/Downloads/romance-20250513T084917Z-1-001/romance/americanroomate.jpg", "The American Roomate Experimate", (100, 200), (100, 430),350, 280),
                ("C:/Users/ADMIN/Downloads/romance-20250513T084917Z-1-001/romance/booklovers.jpg", "Book Lovers", (300, 200), (300, 430),160,200),
                ("C:/Users/ADMIN/Downloads/romance-20250513T084917Z-1-001/romance/pridenprejudice.jpeg", "Pride and Prejudice", (500, 200), (500, 430),480,200),
                ("C:/Users/ADMIN/Downloads/romance-20250513T084917Z-1-001/romance/vacation.jpg", "The People We Meet on Vacation", (700, 200), (700, 430),500,350),
                ("C:/Users/ADMIN/Downloads/romance-20250513T084917Z-1-001/romance/verity.jpg", "Verity", (900, 200), (900, 430),550,650),
                ("C:/Users/ADMIN/Downloads/romance-20250513T084917Z-1-001/romance/TheNotebook.jpg", "The Notebook", (1100, 200), (1100, 430),290,480),
                ("C:/Users/ADMIN/Downloads/romance-20250513T084917Z-1-001/romance/halfasoul.jpg", "Half A Soul", (1300, 200), (1300, 430),100,520),
            ],
        }

# ---------- Login Page ----------
class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login Page")
        self.geometry("400x350")
        self.minsize(400, 350)
        self.configure(bg="#FFE4E1")
        self.create_login_form()
        self.add_image()

    def add_image(self):
        try:
            image = Image.open("mahashweta.jpg").resize((100, 100))
            photo = ImageTk.PhotoImage(image)
            image_label = tk.Label(self, image=photo, bg="#FFE4E1")
            image_label.image = photo
            image_label.pack(pady=10)
        except:
            tk.Label(self, text="PSP MINI PROJECT by: \n933. Mansvi Mor \n934. Swarali Marwadi \n936. Methika M \n946. Saachi Patwari", fg="red", bg="#FFE4E1",font=("Arial,20")).pack(pady=10)

    def create_login_form(self):
        title = tk.Label(self, text="BookHive Login", font=("Arial", 40, "bold"), bg="#FFE4E1", fg="#4B0082")
        title.pack(pady=5)

        tk.Label(self, text="Username:", bg="#FFE4E1",font=("Arial,20")).pack(pady=5)
        self.entry_username = tk.Entry(self)
        self.entry_username.pack(pady=5)

        tk.Label(self, text="Password:", bg="#FFE4E1",font=("Arial,20")).pack(pady=5)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack(pady=5)

        tk.Button(self, text="Login", command=self.check_credentials, bg="darkgreen", fg="white").pack(pady=15)

    def check_credentials(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username == "admin" and password == "password123":
            self.destroy()
            app = BookHiveApp()
            app.mainloop()
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password!")

# ---------- Main Launcher ----------
if __name__ == "__main__":
    login = LoginPage()
    login.mainloop()