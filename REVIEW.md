# REVIEW.md


## Reviewers:

- **Daan Pijfers**
- **Finn Dokter**


## Verbeterpunten:  

### Punt 1
- **Wat is het tegengekomen probleem?**   
  `Dode code in app.py LEADERBOARD: race_lookup functie (line 62) doet niks momenteel.`  
- **Hoe zou je dit beter kunnen maken?**  
  `Het idee was om deze functie te gebruiken om in de Plotly plot over de x-as te kunnen hoveren met de muis en dan de naam van de race te laten zien aan de gebruiker. Dit is niet gelukt, maar ik was te bang om mijn HTML te CTRL+Z-en. Het staat er voor nu in omdat ik het wel naar de HTML pagina moest doorvoeren anders kreeg ik een error.`
- **Wat voor afweging maak je? Vaak is een keuze voor iets ook een keuze tegen iets anders.**  
  `Ik ga dit niet nog op de valreep aanpassen uit angst dat het ineens niet meer werkt. Ik heb van Jelle nog hulp moeten krijgen om de plot uiteindelijk werkend te krijgen nadat ik de 'With Penalties' tick heb geïmplementeerd en ik heb het daarna gewwon gelaten voor wat het was.`
- **Illustreer met enkele voorbeelden.**
  `Ik zou niet precies weten wat hier als voorbeeld telt. Ik zou het gewoon een keer moeten verwijderen zonder de functionaliteit te beïnvloeden maar daar had ik geen tijd voor.`

### Punt 2
- **Wat is het tegengekomen probleem?**   
  `Zero-sum rating niet geïmplementeerd. In de ratings tabel is zero_sum_rating toegevoegd in de hoop dat ik hier nog wat mee zou kunnen. Het idee erachter was dat ik op een andere manier zou gaan raten en het mooie aan dit ratingssysteem is dat het zou optellen naar 0, maar dit was bij mij niet het geval en ik had geen tijd meer om te troubleshooten waarom dit zo was.`  
- **Hoe zou je dit beter kunnen maken?**  
  `Als ik meer tijd had zou ik het kunnen troubleshooten.`
- **Wat voor afweging maak je? Vaak is een keuze voor iets ook een keuze tegen iets anders.**  
  `Tijdsgebrek`
- **Illustreer met enkele voorbeelden.**
  `De zero-sum rating zou (met extra uitleg) in de tabel naast de 'adjusted points komen te staan.`

### Punt 3
- **Wat is het tegengekomen probleem?**   
  `Code in app.py voor LEADERBOARD (line 44) had ik anders kunnen implementeren zodat ik het kon hergebruiken in ALL-TIME LEADERBOARD (line 156).`  
- **Hoe zou je dit beter kunnen maken?**  
  `Ik heb heel andere queries gebruikt voor LEADERBOARD en ALL-TIME LEADERBOARD, wellicht had ik een manier kunnen vinden om in beide een functie aan te roepen die wat overbodige code zou voorkomen.`
- **Wat voor afweging maak je? Vaak is een keuze voor iets ook een keuze tegen iets anders.**  
  `Weet tijdsgebrek en angst dat het dan niet meer zou werken.`
- **Illustreer met enkele voorbeelden.**
  `Ik zou ergens def query_points kunnen maken en die dan aanroepen in beide routes. Verder zou de logica dan afhangen van hoe de rest van de pagina er uit ziet.`
