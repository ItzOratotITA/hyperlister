import subprocess
import time
import sys

DEFAULT_CONFIG = {
    "paths": {"dir": "./config.yml"},
    "targets": {"list": "lista.md", "title": "Lista della spesa"},
}


def y(text):
    return f"[yellow]{text}[/yellow]"


TITLE = "Hyperlister"


def p():
    from rich.console import Console
    from rich.markdown import Markdown
    import yaml

    console = Console()
    with console.status("Preparazione all'avvio...") as status:
        loadconfig = yaml.safe_load
        with open("./config.yml", "r") as configfile:
            config = loadconfig(configfile)
        CONFIG_DIR = config["paths"]["dir"]
        LIST_TARGET = config["targets"]["list"]
        LIST_TITLE = config["targets"]["title"]

    console.rule(TITLE)
    console.print(
        rf"""
           {y('. .')}
     {y(' ____ |/')}
     {y('/    \\<>')}
     {y('| /\\ | |')}\
     {y('| \\/ | |')} \
    {y('<>____---')}  \ [white]/--------------------------------------[/white]\
                | Benvenuto a [bold blue]{TITLE}![/bold blue]               |
                | Scrivi ciò che vuoi aggiungerci        |
                | e scrivi "stop" per fermare.           |
                |                                        |
                | Se vuoi modificare il file dove viene  |
                | salvata la lista, modifica             |
                | "targets->list" in [magenta]{CONFIG_DIR}[/magenta]        |
                |                                        |
                | [yellow][BETA][/yellow] Scrivi [red]"delitem"[/red] per aprire     |
                | la schermata di eliminazione di un     |
                | elemento.                              |
                 \--------------------------------------[white]/[/white]
    
        """
    )

    articles = []
    delitems = False

    def deleteitems():
        deleteitem = console.input("[red]Cosa vorresti eliminare?[/red] ")

        with open(LIST_TARGET, "r") as lista_contenuto:
            data = lista_contenuto.read()
            with open(LIST_TARGET, "w") as lista_nuovo:
                data_new = data.replace(deleteitem, "(eliminato)")
                lista_nuovo.write(data_new)

    while True:
        add = console.input("[blue]Cosa vuoi inserire nella lista?[/blue] ")
        if add.lower() == "stop":
            break
        if add.lower() == "delitem":
            delitems = True
            break
        else:
            articles.append(add)

    def scrivi():
        global risposta
        with open(LIST_TARGET, "a") as lista:
            with open(LIST_TARGET, "r") as lista_read:
                if not LIST_TITLE in lista_read.read():
                    lista.write(f"\n# {LIST_TITLE} - {LIST_TARGET}\n\n")
                    risposta = "mai creato"
                else:
                    risposta = "creato"
            for article in articles:
                lista.write(f"- {article}\n")

    with console.status("Caricamento in corso...", spinner="bouncingBall"):
        scrivi()
    if delitems:
        deleteitems()
    time.sleep(0.7)

    console.print(
        rf"""
    
     {y(r'      . .')}
     {y(r' ____ |/')}
     {y(r'/    \<>')}
     {y(r'| /\ | |')}\
     {y(r'| \/ | | ')}\
    {y('<>____---')}  \ [white]/--------------------------------------[/white][white]\\[/white]
                [white]|[/white] [green]Lista creata/modificata con successo.[/green]  |
                 [white]\\[/white]--------------------------------------[white]/[/white]
    
    """
    )
    with open(LIST_TARGET, "r") as lista_debug:
        md = Markdown(lista_debug.read())
        console.print(md)
        console.print()
        console.input("[red]Press ENTER to exit[/red]")
        time.sleep(0.5)


def setup():
    print(
        rf"""
    
       . .
  ____ |/
 /    \<>
 | /\ | |\
 | \/ | | \
<>____---  \ /----------------------------------------\
            | Benvenuto al setup di {TITLE}!       |
             \----------------------------------------/
    
    """
    )
    print(
        """
Sto installando: rich, pyyaml.
Questa operazione non dovrebbe impiegare molto tempo.
    """
    )
    subprocess.run(["pip", "install", "pyyaml", "rich"])
    import yaml

    print(
        """
Sto creando i file di configurazione...
    """
    )
    with open("config.yml", "w") as f:
        yaml.dump(DEFAULT_CONFIG, f, default_flow_style=False)
    avvia = input("Desideri avviare il programma? (y/n) ")
    if "y" in avvia.lower() or "s" in avvia.lower():
        p()


args = sys.argv

try:
    if args[1] in ("--setup", "/s", "/setup", "-s"):
        setup()
except IndexError:
    try:
        p()
    except:
        print("Ehi la... prima installa il programma.")
        setup()
