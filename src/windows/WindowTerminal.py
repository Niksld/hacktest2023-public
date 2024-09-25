import dearpygui.dearpygui as dpg

from windows.Window import Window
from configuration import LEVEL_DATA, get_progress_requirement

class WindowTerminal(Window):
    def __init__(self, theme = None):
        super().__init__("terminal", 610, 500, ["center", 0, 0], False, True, theme=theme, no_collapse=True, label="Terminál")
        # Ondra asi vypnul window title někde... a nevím kde...
        # Chci svoje labely :(
        # --mas to tam :)

        self.displayed_text = [f"MatoShell v8 [Načtení profilů trvalo 727 ns]\n"]
        self.path = "root@localhost:~$ "
        self.legal_commands = ["echo", "clear", "help", "test", "app", "neofetch"]
        self.current_source = "srandy.scr4p3r0va-banda.cz"
        self.sources_data = LEVEL_DATA["sources"]
        self.help = {
            "test": "Syntax: test <text>.\nVypíše zadaný výraz.",
            "echo": "Syntax: echo <text>.\nVypíše zadaný výraz.",
            "help": "Syntax: help <command>.\nVypíše nápovědu k zadanému příkazu\nSyntax: help.\nVypíše seznam všech příkazů.",
            "clear": "Vymaže všechnu historii terminálu.",
            "app": "Syntax: app source <url>.\nPřidá zdroj pro instalaci aplikací.\nSyntax: app install <app>.\nNainstaluje zadanou aplikaci.",
            "neofetch": "Vypíše informace o systému.\n"
        }
        self.no_path_print = False # použito v případě, že uživatel spustí příkaz, ale ze stylistických důvodů nechceme vypsat path

        dpg.add_text(tag="terminal.text", parent=self.tag, wrap=610, before="terminal.input")
        dpg.add_input_text(tag="terminal.input", parent=self.tag , width=self.width-2, pos=(0,self.height-30), on_enter=True, callback=self.run, hint="Příkaz..." )
        self.echo(self.path, False)

    def run(self) -> None:
        """Handler volání příkazů"""
        raw_input = dpg.get_value("terminal.input")
        dpg.set_value("terminal.input","")
        dpg.focus_item("terminal.input")
        self.echo(raw_input, False)

        #  Detail/QoL: Bylo by fajn mít možnost vypisovat věci postupně. Prostě delay/sleep.
        # --melo by jit skrze multithreading/dpg.split_frame(), snad to nebude delat trable
        # Marty to uz tam davno je? :D
        # -- Tenhle komentář už tu taky nějakou chvíli je :D Konkrétně 3 týdny.

        # POZOR - při používání delaye je potřeba zabránit spuštění více příkazů najednou
        # input se musí zakázat s dpg.disable_item("terminal.input") a pak znovu povolit s dpg.enable_item("terminal.input")
        # (povolení musí být v delayi, jinak se to vypne a pak hned zapne)
        command = raw_input.split()

        match command:
            case ["echo", *arguments]:
                if arguments:
                    self.echo(" ".join(arguments))
                else:
                    self.echo("")

            case ["clear", *arguments]:
                self.displayed_text.clear()
                self.update_text("", scroll=False, refresh=True)
                dpg.set_y_scroll("terminal",0)
                dpg.set_item_pos("terminal.input",(0,470))

            case ["help"]:
                self.echo("")
                for key, value in self.help.items():
                    self.echo(f"{key}: \n{value}\n")

            case ["help", *arguments]:
                for command in arguments:
                    self.echo(self.help.get(command, f"{command}: příkaz nenalezen\n"))


            # Tohle by mělo vědět, co má člověk už stáhnutý atd...
            # Tahal bych to podle levelu.
            case ["app", *arguments]:
                if len(arguments) == 2:
                    match arguments[0]:
                        case "source":
                            dpg.disable_item("terminal.input")
                            self.no_path_print = True

                            # obechcávka na scroll
                            for i in range(4):
                                self.echo(f"\n")
                            #self.remove_line(0,7)

                            self.displayed_text[3] = f"\nPřipojováni k serveru {arguments[1]}"
                            for i in range(15):
                                self.delay(lambda:self.set_dots(3), 0.2*i)
                            if arguments[1] in list(self.sources_data.keys()) and get_progress_requirement(self.progress["progress"], "1###############"):
                                self.current_source = arguments[1]
                                self.delay(lambda: self.set_value(1, value=f"Zdroj úspěšně změnen na adresu: {self.current_source}\n"), 3)
                            else:
                                self.delay(lambda: self.set_value(1,value=f"\nCHYBA: Server na adrese {arguments[1]} nenalezen\n"), 3)
                            self.delay(lambda: (dpg.enable_item("terminal.input"), self.set_value(0,self.path)), 3)

                        case "install":
                            if not get_progress_requirement(self.progress["progress"], "1###############"):
                                self.echo(f"CHYBA: připojení ke zdroji selhalo, zkontrolujte připojení k síti\n")
                            if arguments[1] in list(self.sources_data[self.current_source]):
                                dpg.disable_item("terminal.input")
                                self.echo(f"Stahování balíčku {arguments[1]}...\n")
                                self.no_path_print = True
                                self.delay(lambda:(self.echo(f"Stahování balíčku {arguments[1]} úspěšně dokončeno!\n"), self.echo(self.path, "clear" not in command), dpg.enable_item("terminal.input")),4)
                                if arguments[1] == "virusstudio":
                                    self.delay(lambda: self.set_progress(1, 2), 4)
                            else:
                                self.echo("CHYBA: balíček nenalezen, zkontrolujte název balíčku a adresu zdroje\n")
                        case _:
                            pass

                elif len(arguments) == 1:
                    match arguments[0]:
                        case "source":
                            self.echo(f"Aktuální zdroj pro stahování: {self.current_source}\nPro změnu použijte: app source <adresa>\n")
                        case "install":
                            self.echo("Syntax: app install <balíček>\n")
                else:
                    self.echo("Syntax: app <source/install> ...\n")

            case ["neofetch"]:
                self.echo("""
        NKKKKKKKKKKN              root@localhost
     Xkdc;;;;;;;;;;cdkX           --------------
   Xxc,,;:cccccccc:;,,cxX         OS: Windblows 2064 Pro
 Nk:;::c::;,,,,,,,;::::;cxX       Uptime: 1 den, 3 hodiny
Nk;,:c:;;:lk00000Ooc;;::;,cK      Lokální IP: 192.168.1.13
0,':::;'dNW       WWk,,::;,c0     Motherboard: ASUS ROG STRIX B550
O,':c;'oN           Wk,,:c,'x     CPU: AMD Ryzen 9 5900X
O,':c,.x             O,':c,'x     GPU: NVIDIA GeForce RTX 4070 Ti
O,':c,'x            Kl,;c:,,k     Operační paměť:
O,':c,'x         W0kl';c:,,xN     4.2 GiB / 31.9 GiB (13.125%)
O,':c,'x W0olllllc;';::;;cxN
O,':c,'x O,,;;;;;;:cc:;ckXW       Disk:  C: 13.79GiB / 240 GiB
O,':c,.x O;,,,,,,,,,;cxX                 D: 105.35GiB / 986GiB
O,':c,.x WKxooooooookXW
O,':c,.x
O,':c,'x
0;'::,,k
Nk,..'dX
    """)

            case []:
                self.echo("Nebyl zadán žádný příkaz, zadejte help pro seznam příkazů\n")

            case _:
                self.echo(f"{' '.join(command)}: příkaz nenalezen, zadejte help pro seznam příkazů\n")

        if not self.no_path_print:
            self.echo(self.path, "clear" not in command)
        else:
            self.no_path_print = False

    def set_dots(self, index:int) -> None:
        self.displayed_text[index] += "."
        self.update_text("", refresh=True, scroll=False)

    def set_value(self, index:int, value:str) -> None:
        self.displayed_text[index] = value
        self.update_text("", refresh=True, scroll=False)

    def remove_line(self, index:int = 0, end:int = None) -> str:
        """Odstranění řádku z terminálu na určeném indexu

        Default je 0 - Poslední vypsaný řádek

        Vrací string odstraněného řádku
        """
        if end is None:
            end = index

        if end == index:
            self.displayed_text.pop(index)
        else:
            for i in range(index, end+1):
                self.displayed_text.pop(0)
        self.update_text("", refresh=True, scroll=False)


    def scroll_down(self) -> None:
            try: #  Dobrej napad actually ondro
                self.delay(lambda: (dpg.set_y_scroll("terminal", dpg.get_y_scroll_max("terminal")), dpg.set_item_pos("terminal.input", (0, int(dpg.get_item_height("terminal")+dpg.get_y_scroll_max("terminal")-30)))), 0.0001)
            except Exception:
                pass

    def echo(self, text: str, newline: bool = True) -> str:
        self.update_text(("\n" if newline else "") + text, newline)
        return ("\n" if newline else "") + text # idk, může se někdy hodit.

    def update_text(self, text: str, scroll: bool = True, refresh:bool = False) -> None:
        """Vypsání textu do terminálu

            newline: default->True - Ovládání jestli na řádek chceme newline
            refresh: default->False - Funkce pro znovu vypsání textu bez přidání nového.
        """
        #  Text se ukládá do seznamu (kvuli zobrazeni minulých příkazů)
        #  0 -> dole (nejnovejsi prikaz), 15 -> nahore (nejstarsi zadany prikaz, brzo vyhozen)
        # self.displayed_text[1:16] = self.displayed_text[0:15]
        # self.displayed_text[0] = text

        if not refresh:
            self.displayed_text.insert(0, text)

        text_buffer = ""

        for i in range(len(self.displayed_text)-1,-1,-1):
            text_buffer += self.displayed_text[i]

        if scroll: # Eh good enough.
            self.scroll_down()

        dpg.set_value("terminal.text", text_buffer)
