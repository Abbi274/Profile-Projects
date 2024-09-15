import re

class User: 
    def __init__(self, name): 
        self.name = name 
        self.borrowed = set() # set of titles checked out  
        self.fine = 0 
        self.favorites = set() # set of fave (type, title) 
        self.card_issued = False 
        
    @staticmethod 
    def parse_fine(instruction):
        full_match = re.fullmatch(r'pay fees \$(\d+) (.*)', instruction) 
        if full_match: 
            return(full_match.group(1),full_match.group(2)) 
        else: 
            raise KeyError() 
        
    def add_fine(self, amount): 
        self.fine += amount 
    
    def pay_fine(self, amount): 
        self.fine -= amount 
        return f'${amount} paid. User fines = ${self.fine}'
    
    def checkout(self, title): 
        self.borrowed.add(title) 
        
    def can_checkout(self): 
        if self.fine: 
            return False
        else: 
            return True 
        
    def need_card(self):
        if not self.card_issued: 
            self.card_issued = True 
            return 'Issue New Card'
             # else lost card and added $1 fine to re-issue 
        self.add_fine(1) 
        return 'Issue New Card. Fine Added'
            
    def add_favorite(self, fav_tuple): 
        self.favorites.add(fav_tuple) 
   
    def return_book(self, title): 
        if title in self.borrowed: 
            self.borrowed.discard(title) 
        
    def __str__(self): 
        return f'{self.name}'
    
class Book:  
    def __init__(self, title, author): 
        self.title = title 
        self.author = author 
        self.book_id = None 
        self.borrowed_by = None

    @staticmethod 
    def parse_def(book_representation):  
        full_match = re.fullmatch('(.*) by (.*)', book_representation) 
        if full_match:
            return Book(full_match[1], full_match[2]) 
        else: 
                raise KeyError() 
    @staticmethod  
    def parse_title_auth(rest): 
        full_match = re.fullmatch('(.*) by (.*)', rest) 
        if full_match: 
            return (full_match[1], full_match[2]) 
        else: 
            raise KeyError() 
            
    def __str__(self): 
        return f'"{self.title}" by {self.author}'
    
class Movie: 
    def __init__(self, id, title):
        self.id = id 
        self.title = title 
        self.borrowed_by = None 
    
    def return_movie(self): 
        self.borrowed_by = None
        
    def _str__(self): 
        return f'"{self.title}"'
        
class Library: 
    def __init__(self): 
        self.book_library = {}
        self.user_catalogue = {}
        self.childrens_book_library = {}
        self.movies = {} 
        self.titles = {} # map each object by title as well 
        
    def register(self, book_type, new_book): 
        if book_type == 'book': 
            if new_book.book_id not in self.book_library: 
                self.book_library[new_book.book_id] = new_book
                self.titles[new_book.title] = new_book 
                
        else: 
            if new_book.book_id not in self.childrens_book_library: 
                self.childrens_book_library[new_book.book_id] = new_book
                self.titles[new_book.title] = new_book 
                
    def register_movie(self, movie):
        if movie.id not in self.movies: 
            self.movies[id] = movie 
        self.titles[movie.title] = movie
      
    def find_user(self, name): 
        if name not in self.user_catalogue: 
            self.user_catalogue[name] = User(name)
        return self.user_catalogue[name]
        
def simulate_library(instructions):
    output = []
    library = Library()
    
    for instruction in instructions:
        if instruction.startswith('pay'): 
            fee, name = User.parse_fine(instruction)  
            user = library.find_user(name) 
            if user.fine == 0: 
                output.append('No fine due')
                continue
            output.append(user.pay_fine(int(fee))) 
            continue 
            
        command, subcommands = instruction.split(' ', 1) 
        if command == 'library_card': 
            user = library.find_user(subcommands) 
            output.append(user.need_card())  

        elif command == 'register': 
            if subcommands.startswith('DVD'): 
                movie_id, movie = subcommands.split(' ',1) 
                library.register_movie(Movie(movie_id, movie))
                continue 
                
            book_type, book_id, rest = subcommands.split(' ', 2) 
            new_book = Book.parse_def(rest)
            if new_book:   # if a new book can be added (not key error) add it 
                new_book.book_id = book_id  
                library.register(book_type, new_book)
                
           
        elif command == 'favorite':
            first_name, last_name, object_type, title = subcommands.split(' ', 3)  
            name = first_name + ' ' + last_name 
            user = library.find_user(name) 
            user.add_favorite((type, title))
            output.append('Title added to user\'s favorites') 
        
        elif command == 'checkout': 
            first_name, last_name, object_type, rest = subcommands.split(' ', 3)
            if object_type == 'book' or object_type == 'childrens_book':
                title, author = Book.parse_title_auth(rest) 
            else: 
                rest = title
            if title not in library.titles:
                output.append('Book does not exist')
                continue 
            book = library.titles[title] 
            if book.borrowed_by is None: 
                # then can check out 
                name = first_name + ' ' + last_name 
                user = library.find_user(name)
                can_checkout = user.can_checkout() 
                if can_checkout: 
                    book.borrowed_by = user
                    user.checkout(title)  
                    output.append(f'{title} checked out by {user.name}') 
                else: 
                    output.append('User must pay fine')  
            else: 
                output.append('Book currently unavailable') 
        
        elif command == 'return': 
            object_type, rest = subcommands.split(' ', 1) 
            if object_type == 'dvd':
                if rest not in library.titles: 
                    output.append('Not in System')
                    continue 
                movie = library.titles[rest] 
                movie.return_movie() 
                output.append('Movie returned') 
            
            elif object_type == 'book': 
                title, author = Book.parse_title_auth(rest)
                if title not in library.titles: 
                    output.append('Not in System')
                book = library.titles[title] 
                if book.borrowed_by is None: 
                    continue 
                book.borrowed_by.return_book(title)
                book.borrowed_by = None 
                output.append('Book returned') 
            else: 
                title, author = Book.parse_title_auth(rest)
                if title not in library.titles: 
                    output.append('Not in System')
                book = library.titles[title] 
                if book.borrowed_by is None: 
                    continue 
                book.borrowed_by.return_book(title)
                book.borrowed_by = None 
                output.append('Childrens book returned')
                
    return output 




instructions = ['library_card John Doe', 
    'register book F_325 The Lion, the Witch and the Wardrobe by C.S. Lewis',
    'register book 123 Python for Everybody by Charles Severance',
    'register DVD_F_797 Canadian Bacon',
    'register J_F_832 childrens_book Frog and Toad by Arnold Lobel', 
    'library_card Jane Smith',
    'favorite Jane Smith childrens_book Amelia Bedilia',
    'checkout Jane Smith childrens_book Frog and Toad by Arnold Lobel',
    'checkout John Doe childrens_book Frog and Toad by Arnold Lobel',
    'library_card Jane Smith',
    'checkout John Doe book The Lion, the Witch and the Wardrobe by C.S. Lewis', 
    'checkout John Doe DVD Canadian Bacon',
    'return childrens_book Frog and Toad by Arnold Lobel',
    'return book The Lion, the Witch and the Wardrobe by C.S. Lewis',
    'return dvd Canadian Bacon',
    'pay fees $1 Jane Smith' 
]           

print(simulate_library(instructions))

