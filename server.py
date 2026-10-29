import socket 
from threading import Thread 
import pygame 
import pynput
import time 

class Person: 
    def __init__(self, sock, ad):
        self.sock = sock 
        self.address = ad

class Server: 
    def __init__(self, host, port, name, max_clients):
        pygame.init()
        self.win = pygame.display.set_mode((900, 500))
        self.name = name 
        pygame.display.set_caption("Cat Slack")
        self.font = pygame.font.Font(size=32)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(max_clients)
        self.running = True 
        self.clients = [] 
        self.recievers = []
        self.terminal = ""
        self.line = 0 
        self.debug = False 
        self.accepter = Thread(target=self.accept)
        self.accepter.start()
        self.gui = ["System: Server Started! Welcome to CatNet."]
        self.kyl = Thread(target=self.kl)
        self.kyl.start()
        self.main_loop() 

    def accept(self):
        while self.running: 
            client, addr = self.socket.accept()
            self.clients.append(Person(client, addr))
            self.gui.append("New Client @" + str(addr))
            r = Thread(target=self.reciever, args=(client,))
            r.start()
            self.recievers.append(r)
            
        
        

    def reciever(self, socket):
        socker = socket
        while self.running: 
            data = socker.recv(1024)
            data = data.decode() 
            data = str(data)
            self.gui.append(data)
            for cli in self.clients:
                if cli.sock == socket:
                    pass 
                else:
                    cli.sock.sendall(data.encode())

                
           

    def on_press(self, key):
        key = str(key)
        key = key.replace("'","")
        if key == "Key.enter":
            if self.terminal == "debug":
                self.debug = not self.debug 
            else:
                self.gui.append("You: " + self.terminal)
                self.terminal = self.terminal.encode()
                for cli in self.clients:
                    cli.sock.sendall(self.name +": " + self.terminal)
            self.terminal = ""
        elif key == "Key.backspace":
            self.terminal = self.terminal[:-1]
        elif key == "Key.shift": pass 
        elif key == "Key.space":
            self.terminal = self.terminal + " "
        else:
            self.terminal = self.terminal + key 



    def on_release(self, key):
        pass

    def kl(self):
        with pynput.keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as kl:
            kl.join()

   

    def main_loop(self):
        while self.running: 
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT: 
                    self.running = False
                    pygame.quit()
                

            self.win.fill((0,0,0))

            

            for index, line in enumerate(self.gui):
                if self.debug:
                    self.font = pygame.font.Font(size=12)
                    sur = self.font.render(''.join(format(ord(char), '08b') for char in line), False, (255, 255, 255))
                else:
                    self.font = pygame.font.Font(size=32)
                    sur = self.font.render(line, False, (255, 255, 255))
                self.win.blit(sur, (50, 350 - (len(self.gui) * 35) + (index * 35)))

            

            surface = self.font.render(self.terminal, False, (255, 0, 0))
            self.win.blit(surface, (50, 450))

            

            pygame.display.flip()
            # ''.join(format(ord(char), '08b') for char in data))

if __name__ == "__main__":
    name = input("Name?: ")
    clis = int(input("Max Clients (int): "))
    server = Server(socket.gethostbyname(socket.gethostname()), 12345, name, clis)
