# ASSESSMENT.md

## Belangrijke punten voor beoordeling

### Codekwaliteit en structuur
- **Netheid:**   
  `Ik denk dat een sterk punt van mijn coderen is dat de meeste scripts die ik gebruik ook redelijk duidelijk zijn. De templates zijn vrij vanzelfsprekend en verder heb ik de structuur van finance en books redelijk goed aangehouden in mijn eigen project.`

- **Unieke aanpak:**  
  `Iets dat ik eerder wel eens heb gezien, maar nooit wist hoe ik dit zelf moest implementeren, is wat ik in mijn compare.html heb staan om de namen en jaren waarin de opgegeven coureur met die naam heeft gereden. Dit heb ik gedaan met een` [EventListener](https://developer.mozilla.org/en-US/docs/Web/API/Document/DOMContentLoaded_event) `in een JavaScript stukje dat een eigen API oproept.`

### Functionaliteit waar ik trots op ben
- **Functie 1:**    
  `Het kunnen updaten van de plot in de leaderboards en de season compare pagina. [In app.py onder LEADERBOARD (lines 44-153) en in leaderboard.html het stukje over de Tick-box met vlak daaronder de verwijzing naar een Plotly plot in JavaScript (lines 38-52)]`

- **Functie 2:**   
  `De implementatie van postgres databases om beide de normale punten en de aangepaste punten op te slaan in een nieuwe tabel genaamd 'ratings'. [In models.py zijn BIJNA alle tabellen gebaseerd op de csv bestanden die ik in de data folder heb, deze worden gevuld in import.py. Het Rating model slaat de uiteindelijke berekeningen op. Deze tabel wordt gevuld in engine.py]`

---

## Grote beslissingen tijdens het project

### Beslissing 1: Alle jaren vóór 2010 hebben het 2010-heden puntensysteem gekregen
- **Waarom heb je deze beslissing genomen?**   
  `Dit was noodzakelijk om consequent te blijven door de seizoenen en het maakt de season compare pagina mogelijk.`

- **Wat was er niet zo handig aan de vorige ontwerpideeën?**   
  `Ik moest simpelweg een oplossing vinden voor het veranderen van het puntensysteem. Het oude puntensysteem maakt het onmogelijk om coureurs van vroeger met hedendaagse coureurs accuraat te vergelijken.`

- **Waarom is de nieuwe oplossing beter?**  
  `Met het consquente puntensysteem maakt het makkelijk om coureurs van vershillende tijdperken met elkaar te vergelijken.`

- **Wat is er suboptimaal aan deze oplossing?**  
  `Het jammere aan deze oplossing is dat dingen zoals sprint races en punten voor de snelste ronden eruit gehaald zijn, waardoor je wel wat informatie mist. Ook is het zo dat coureurs natuurlijk op een andere manier zouden kunnen gaan rijden al is het puntensysteem anders, daar houdt deze oplossing geen rekening mee.`

---

### Beslissing 2: Geen 'Drivers' pagina toegevoegd
- **Waarom heb je deze beslissing genomen?**   
  `Alhoewel het in de eerste instantie mijn plan was om voor elke coureur een eigen pagina te maken was dit uiteindelijk toch wat aan de ambitieuse kant. Ik heb besloten om de leaderboards met de namen en grafieken erbij voor zichzelf te laten spreken.`

- **Wat was er niet zo handig aan de vorige ontwerpideeën?**   
  `Om van alle 800+ coureurs een eigen pagina te maken was te veel werk en het was ook niet zo'n belangrijke toevoeging aan mijn project specifiek. Bovendien was niet alles bekend over alle coureurs, er zijn namelijk meer dan een paar coureurs die bijvoorbeeld maar één race hebben gereden en veel van de coureurs van de jaren '50 hebben incomplete data.`

- **Waarom is de nieuwe oplossing beter?**  
  `Het gebrek van een Drivers pagina houd de app simpel en bespaart mijn veel onnodig werk.`

- **Wat is er suboptimaal aan deze oplossing?**  
  `Het had mooi geweest om per coureur mijn puntensysteem te zien. Zoals Max Verstappen's punten over zijn hele carrière in één grafiek.`
