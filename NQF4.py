<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <title>Vocabulaire Pelckmans - Oefenplatform</title>
    <style>
        :root { --primary: #3498db; --success: #2ecc71; --danger: #e74c3c; --bg: #121212; --card: #1e1e1e; --accent: #f1c40f; }
        body { background-color: var(--bg); color: white; font-family: 'Segoe UI', sans-serif; margin: 0; }
        #container { width: 95%; max-width: 1100px; margin: 40px auto; text-align: center; }
        
        .selector-container { background: var(--card); padding: 25px; border-radius: 12px; margin-bottom: 30px; border: 1px solid #333; }
        select { padding: 12px; background: #333; color: white; border-radius: 6px; border: 1px solid var(--primary); font-size: 16px; width: 250px; cursor: pointer; }

        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; }
        .set-card { background: var(--card); padding: 20px; border-radius: 12px; border: 1px solid #333; transition: 0.3s; }
        .set-card:hover { border-color: var(--primary); transform: translateY(-3px); }
        
        .btn { background: var(--primary); color: white; border: none; padding: 12px; border-radius: 6px; cursor: pointer; font-size: 15px; width: 100%; margin-top: 10px; transition: 0.3s; }
        .btn:hover { filter: brightness(1.2); }

        .screen { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: var(--bg); z-index: 100; justify-content: center; align-items: center; flex-direction: column; }
        
        #word-display { font-size: 60px; font-weight: bold; margin: 40px 0; color: var(--accent); text-shadow: 2px 2px 10px rgba(0,0,0,0.5); padding: 0 20px; text-align: center; }
        #timer-container { width: 70%; height: 12px; background: #333; border-radius: 6px; margin: 20px auto; overflow: hidden; }
        #timer-bar { width: 100%; height: 100%; background: var(--success); transition: width 1s linear; }

        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 12px; border: 1px solid #444; text-align: left; }
        th { background: #333; color: var(--primary); }
        .scroll-area { width: 85%; max-height: 70vh; overflow-y: auto; background: #1e1e1e; padding: 15px; border-radius: 10px; }
    </style>
</head>
<body>

<div id="container">
    <h1>Pelckmans Vocabulaire Trainer</h1>
    <p style="color: #888;">Selecteer een Trajet om de 10 oefensets te genereren.</p>
    
    <div class="selector-container">
        <label style="margin-right: 15px;">Kies Trajet:</label>
        <select id="trajet-select" onchange="generateSets(this.value)">
            <option value="">-- Maak een keuze --</option>
            <option value="1">Trajet 1</option>
            <option value="2">Trajet 2</option>
            <option value="3">Trajet 3</option>
            <option value="4">Trajet 4</option>
            <option value="5">Trajet 5</option>
            <option value="6">Trajet 6</option>
            <option value="7">Trajet 7</option>
        </select>
    </div>

    <div class="grid" id="set-grid"></div>
</div>

<div id="exercise" class="screen">
    <div id="info-header" style="font-size: 1.2rem; color: #aaa;"></div>
    <div id="timer-container"><div id="timer-bar"></div></div>
    <div id="word-display">Laden...</div>
    <div style="display:flex; gap:15px;">
        <button class="btn" style="width:140px; background:#555;" id="pause-btn" onclick="togglePause()">Pause</button>
        <button class="btn" style="width:140px; background:var(--danger);" onclick="location.reload()">Stop</button>
    </div>
</div>

<div id="result" class="screen">
    <h2 style="color: var(--success);">Set Voltooid!</h2>
    <div class="scroll-area">
        <table>
            <thead><tr><th>Nederlands</th><th>Français</th></tr></thead>
            <tbody id="res-body"></tbody>
        </table>
    </div>
    <button class="btn" style="margin-top: 20px; width:250px;" onclick="location.reload()">Terug naar Menu</button>
</div>

<script>
// Volledige database gebaseerd op Trajet 
const woordenLijst = [
    {t:1, nl:"de baai", fr:"la baie"}, {t:1, nl:"de blauw-wit-rode vlag", fr:"le drapeau bleu blanc rouge"}, {t:1, nl:"het (verkeers)bord", fr:"le panneau"}, {t:1, nl:"de bouillabaisse", fr:"la bouillabaisse"}, {t:1, nl:"de camping", fr:"le camping"}, {t:1, nl:"de bron", fr:"la source"}, {t:1, nl:"de Franse driekleur", fr:"le drapeau tricolore"}, {t:1, nl:"de klif", fr:"la falaise"}, {t:1, nl:"de leuze", fr:"la devise"}, {t:1, nl:"de Mont Blanc", fr:"le mont Blanc"}, {t:1, nl:"de rotskloof", fr:"les gorges"}, {t:1, nl:"het departement", fr:"le département"}, {t:1, nl:"de departementale weg", fr:"la RD, la D"}, {t:1, nl:"de gastenkamer", fr:"la chambre d'hôtes"}, {t:1, nl:"de nationale feestdag", fr:"la fête nationale"}, {t:1, nl:"de regering", fr:"le gouvernement"}, {t:1, nl:"de staat", fr:"l'État"}, {t:1, nl:"het volkslied", fr:"l'hymne national"}, {t:1, nl:"de hoofdstad", fr:"la capitale"}, {t:1, nl:"de koning", fr:"le roi"}, {t:1, nl:"de koningin", fr:"la reine"}, {t:1, nl:"het koninkrijk", fr:"le royaume"}, {t:1, nl:"de republiek", fr:"la république"}, {t:1, nl:"de revolutie", fr:"la revolutie"}, {t:1, nl:"de rots", fr:"la roche"}, {t:1, nl:"de schaaldieren", fr:"les crustacés"}, {t:1, nl:"zuurkoolschotel", fr:"la choucroute"}, {t:1, nl:"de slakken", fr:"les escargots"}, {t:1, nl:"het streekproduct", fr:"le produit du terroir"}, {t:1, nl:"het symbool", fr:"le symbole"}, {t:1, nl:"de tartiflette", fr:"la tartiflette"}, {t:1, nl:"het teken", fr:"le signe"}, {t:1, nl:"de tol", fr:"le péage"}, {t:1, nl:"het uitzicht", fr:"le point de vue"}, {t:1, nl:"vakantiewoning", fr:"le gîte"}, {t:1, nl:"de vallei", fr:"la vallée"}, {t:1, nl:"de zeshoek", fr:"l'hexagone"}, {t:1, nl:"het Zuiden", fr:"le Midi"},
    {t:2, nl:"de begrafenis", fr:"l'enterrement"}, {t:2, nl:"bestellen", fr:"commander"}, {t:2, nl:"de bestelling", fr:"la commande"}, {t:2, nl:"Beste wensen!", fr:"Meilleurs voeux!"}, {t:2, nl:"boeket bloemen", fr:"le bouquet de fleurs"}, {t:2, nl:"het budget", fr:"le budget"}, {t:2, nl:"het cadeau", fr:"le cadeau"}, {t:2, nl:"de confetti", fr:"les confettis"}, {t:2, nl:"de dansvloer", fr:"la piste de danse"}, {t:2, nl:"de discobal", fr:"la boule disco"}, {t:2, nl:"de dj", fr:"le DJ"}, {t:2, nl:"het feest", fr:"la soirée"}, {t:2, nl:"feesten", fr:"faire la fête"}, {t:2, nl:"het feestmaal", fr:"le repas de fête"}, {t:2, nl:"de feestzaal", fr:"la salle des fêtes"}, {t:2, nl:"de fotocabine", fr:"le photomaton"}, {t:2, nl:"de fuif", fr:"la boum"}, {t:2, nl:"Gefeliciteerd!", fr:"Félicitations!"}, {t:2, nl:"de gelegenheid", fr:"l'occasion"}, {t:2, nl:"Gelukkige feestdag!", fr:"Bonne fête!"}, {t:2, nl:"Gelukkige verjaardag!", fr:"Joyeux anniversaire!"}, {t:2, nl:"Gelukkig Nieuwjaar!", fr:"Bonne année!"}, {t:2, nl:"geschenkverpakking", fr:"l'emballage cadeau"}, {t:2, nl:"de ijsthee", fr:"le thé glacé"}, {t:2, nl:"de kaars", fr:"la bougie"}, {t:2, nl:"de e-kaart", fr:"la carte"}, {t:2, nl:"de kermis", fr:"la kermesse"}, {t:2, nl:"de kerstboom", fr:"le sapin de Noël"}, {t:2, nl:"Oudejaarsavond", fr:"la Saint-Sylvestre"}, {t:2, nl:"de receptie", fr:"la réception"}, {t:2, nl:"het servet", fr:"la serviette"}, {t:2, nl:"Sinterklaas", fr:"la Saint-Nicolas"}, {t:2, nl:"de slinger", fr:"la guirlande"}, {t:2, nl:"de ster van de dag", fr:"la star du jour"}, {t:2, nl:"Succes!", fr:"Bonne chance!"}, {t:2, nl:"tafelkleed", fr:"la nappe"}, {t:2, nl:"kaarsen uitblazen", fr:"souffler les bougies"}, {t:2, nl:"uit eten gaan", fr:"aller au restaurant"}, {t:2, nl:"uitgaan", fr:"sortir en boîte"}, {t:2, nl:"uitgeven", fr:"dépenser"}, {t:2, nl:"het uitje", fr:"la sortie"}, {t:2, nl:"uitnodigen", fr:"inviter"}, {t:2, nl:"Vaderdag", fr:"la fête des Pères"}, {t:2, nl:"Valentijnsdag", fr:"la Saint-Valentin"}, {t:2, nl:"verjaardag (huwelijk)", fr:"l'anniversaire"}, {t:2, nl:"verkleed", fr:"déguisé"}, {t:2, nl:"verrassend", fr:"surprenant"}, {t:2, nl:"versieren", fr:"décorer"}, {t:2, nl:"de versiering", fr:"la decoration"}, {t:2, nl:"vieren", fr:"célébrer"}, {t:2, nl:"de vj", fr:"le VJ"}, {t:2, nl:"liefje", fr:"le petit copain"}, {t:2, nl:"wensen", fr:"souhaiter"}, {t:2, nl:"verkleden", fr:"se déguiser"},
    {t:3, nl:"het abonnement", fr:"l'abonnement"}, {t:3, nl:"de app", fr:"l'appli"}, {t:3, nl:"de batterij", fr:"la batterie"}, {t:3, nl:"het beeld", fr:"l'image"}, {t:3, nl:"bereikbaar zijn", fr:"être joignable"}, {t:3, nl:"bewaren, opslaan", fr:"sauvegarder"}, {t:3, nl:"de blog", fr:"le blog"}, {t:3, nl:"bericht", fr:"le message"}, {t:3, nl:"de chat", fr:"le tchat"}, {t:3, nl:"de communicatie", fr:"la communication"}, {t:3, nl:"communiceren", fr:"communiquer"}, {t:3, nl:"batterij is plat", fr:"la batterie est à plat"}, {t:3, nl:"het tv-journaal", fr:"le JT"}, {t:3, nl:"klank luider", fr:"augmenter le son"}, {t:3, nl:"klank stiller", fr:"baisser le son"}, {t:3, nl:"de doelgroep", fr:"le public cible"}, {t:3, nl:"downloaden", fr:"télécharger"}, {t:3, nl:"abonnement nemen", fr:"prendre un abonnement"}, {t:3, nl:"krant online lezen", fr:"lire un journal en ligne"}, {t:3, nl:"de e-mail", fr:"l'e-mail"}, {t:3, nl:"het e-mailadres", fr:"l'adresse mail"}, {t:3, nl:"het evenement", fr:"l'évènement"}, {t:3, nl:"het forum", fr:"le forum"}, {t:3, nl:"de hashtag", fr:"le hashtag"}, {t:3, nl:"de ICT", fr:"les TIC"}, {t:3, nl:"de informatie", fr:"l'information"}, {t:3, nl:"internationaal", fr:"international"}, {t:3, nl:"het interview", fr:"l'interview"}, {t:3, nl:"de journalist", fr:"le journaliste"}, {t:3, nl:"de klik", fr:"le clic"}, {t:3, nl:"klikken", fr:"cliquer"}, {t:3, nl:"de lader", fr:"le chargeur"}, {t:3, nl:"de link", fr:"le lien"}, {t:3, nl:"de login", fr:"le nom d'utilisateur"}, {t:3, nl:"lokaal", fr:"local"}, {t:3, nl:"de melding", fr:"la notification"}, {t:3, nl:"nieuws kijken", fr:"regarder les infos"}, {t:3, nl:"nieuws luisteren", fr:"écouter les nouvelles"}, {t:3, nl:"nationaal", fr:"national"}, {t:3, nl:"het nieuwsfeit", fr:"le fait divers"}, {t:3, nl:"online", fr:"en ligne"}, {t:3, nl:"op de hoogte blijven", fr:"suivre l'actualiteit"}, {t:3, nl:"opladen", fr:"recharger"}, {t:3, nl:"opnemen", fr:"enregistrer"}, {t:3, nl:"het paswoord", fr:"le mot de passe"}, {t:3, nl:"de politiek", fr:"la politique"}, {t:3, nl:"het publiek", fr:"le public"}, {t:3, nl:"de reclame", fr:"la pub"}, {t:3, nl:"regionaal", fr:"régional"}, {t:3, nl:"de smartphone", fr:"le smartphone"}, {t:3, nl:"de smiley", fr:"l'émoticône"}, {t:3, nl:"sociale netwerken", fr:"les réseaux sociaux"}, {t:3, nl:"internet surfer", fr:"l'internaute"}, {t:3, nl:"toegang hebben tot", fr:"avoir accès à"}, {t:3, nl:"de uitzending", fr:"l'émission"}, {t:3, nl:"verkeersinformatie", fr:"l'info trafic"}, {t:3, nl:"het volume", fr:"le volume"}, {t:3, nl:"zappen", fr:"zapper"}, {t:3, nl:"de zender", fr:"la chaîne"}, {t:3, nl:"zich aanmelden", fr:"se connecter"}, {t:3, nl:"zich abonneren", fr:"s'abonner"}, {t:3, nl:"zich afmelden", fr:"se déconnecter"}, {t:3, nl:"zich informeren", fr:"s'informer"}, {t:3, nl:"zich richten tot", fr:"s'adresse à"}, {t:3, nl:"gsm aanzetten", fr:"allumer son portable"}, {t:3, nl:"gsm uitzetten", fr:"éteindre son portable"}, {t:3, nl:"de zoekmachine", fr:"le moteur de recherche"},
    {t:4, nl:"aansluiten", fr:"brancher"}, {t:4, nl:"activeren", fr:"activer"}, {t:4, nl:"de adapter", fr:"l'adaptateur"}, {t:4, nl:"de afmeting", fr:"la dimension"}, {t:4, nl:"bevestigen", fr:"valider"}, {t:4, nl:"creëren", fr:"créer"}, {t:4, nl:"het doel", fr:"le but"}, {t:4, nl:"drukken op", fr:"appuyer sur"}, {t:4, nl:"efficiënt", fr:"efficace"}, {t:4, nl:"de elektriciteit", fr:"l'électricité"}, {t:4, nl:"de energie", fr:"l'énergie"}, {t:4, nl:"fabriceren", fr:"fabriquer"}, {t:4, nl:"het gebruik", fr:"l'emploi"}, {t:4, nl:"gebruikmaken van", fr:"se servir de"}, {t:4, nl:"het gewicht", fr:"le poids"}, {t:4, nl:"herbruikbaar", fr:"réutilisable"}, {t:4, nl:"herlaadbaar", fr:"rechargeable"}, {t:4, nl:"innoverend", fr:"innovant"}, {t:4, nl:"insteken", fr:"insérer"}, {t:4, nl:"de knop", fr:"le bouton"}, {t:4, nl:"de knutselaar", fr:"le bricoleur"}, {t:4, nl:"met behulp van", fr:"à l'aide de"}, {t:4, nl:"nutteloos", fr:"inutile"}, {t:4, nl:"ontwikkelen", fr:"développer"}, {t:4, nl:"produceren", fr:"produire"}, {t:4, nl:"programmeren", fr:"programmer"}, {t:4, nl:"simpel, eenvoudig", fr:"simple"}, {t:4, nl:"het systeem", fr:"le systeem"}, {t:4, nl:"het toestel", fr:"l'appareil"}, {t:4, nl:"uitschakelen", fr:"désactiver"}, {t:4, nl:"uitvinden", fr:"inventer"}, {t:4, nl:"de uitvinder", fr:"l'inventeur"}, {t:4, nl:"de uitvinding", fr:"l'invention"}, {t:4, nl:"het voorwerp", fr:"l'objet"}, {t:4, nl:"de werking", fr:"le fonctionnement"}, {t:4, nl:"het werktuig", fr:"l'outil"}, {t:4, nl:"zonne-", fr:"solaire"},
    {t:5, nl:"huishoudelijk afval", fr:"les déchets"}, {t:5, nl:"afvalwater", fr:"les eaux usées"}, {t:5, nl:"beperken", fr:"limiter"}, {t:5, nl:"de bescherming", fr:"la protection"}, {t:5, nl:"biol. afbreekbaar", fr:"biodégradable"}, {t:5, nl:"de compost", fr:"le compost"}, {t:5, nl:"het compostvat", fr:"le composteur"}, {t:5, nl:"composteren", fr:"composter"}, {t:5, nl:"de ecologie", fr:"l'écologie"}, {t:5, nl:"de energiebron", fr:"la source d'énergie"}, {t:5, nl:"het fijne deeltje", fr:"la particule"}, {t:5, nl:"de grond, bodem", fr:"le sol"}, {t:5, nl:"in bulk", fr:"en vrac"}, {t:5, nl:"het koolstofdioxide", fr:"le CO2"}, {t:5, nl:"het milieu", fr:"l'environnement"}, {t:5, nl:"de planeet", fr:"la planète"}, {t:5, nl:"plastic verpakking", fr:"l'emballage plastique"}, {t:5, nl:"het recipiënt", fr:"le contenant"}, {t:5, nl:"de recyclage", fr:"le recyclage"}, {t:5, nl:"recycleerbaar", fr:"recyclable"}, {t:5, nl:"recycleren", fr:"recycler"}, {t:5, nl:"schoon, milieuvriendelijk", fr:"propre"}, {t:5, nl:"het sorteren", fr:"le tri"}, {t:5, nl:"afval sorteren", fr:"trier"}, {t:5, nl:"de spaarlamp", fr:"l'ampoule basse conso"}, {t:5, nl:"de stortplaats", fr:"la décharge"}, {t:5, nl:"uitschakelen, afzetten", fr:"débrancher"}, {t:5, nl:"de vaststelling", fr:"le constat"}, {t:5, nl:"de verandering", fr:"le changement"}, {t:5, nl:"het verbruik", fr:"la consommation"}, {t:5, nl:"verbruiken", fr:"consommer"}, {t:5, nl:"de verbruiker", fr:"le consommateur"}, {t:5, nl:"verminderen", fr:"diminuer"}, {t:5, nl:"verspillen", fr:"gaspiller"}, {t:5, nl:"de verspilling", fr:"le gaspillage"}, {t:5, nl:"vervuilen", fr:"polluer"}, {t:5, nl:"vervuilend", fr:"polluant"}, {t:5, nl:"de vervuiler", fr:"le pollueur"}, {t:5, nl:"de vervuiling", fr:"la pollution"}, {t:5, nl:"vuil", fr:"sale"}, {t:5, nl:"de vuilniszak", fr:"le sac poubelle"}, {t:5, nl:"waterzuivering", fr:"la station d'épuration"}, {t:5, nl:"weggooien", fr:"jeter"}, {t:5, nl:"de windturbine", fr:"l'éolienne"}, {t:5, nl:"het zonnepaneel", fr:"le panneau solaire"},
    {t:6, nl:"de aanbieding", fr:"l'offre"}, {t:6, nl:"toevoegen aan mandje", fr:"ajouter au panier"}, {t:6, nl:"aanschuiven kassa", fr:"faire la queue"}, {t:6, nl:"bestelde artikel", fr:"l'article"}, {t:6, nl:"het bedrag", fr:"le montant"}, {t:6, nl:"beschadigd", fr:"endommagé"}, {t:6, nl:"beschikbaar zijn", fr:"être disponible"}, {t:6, nl:"de betaling", fr:"le paiement"}, {t:6, nl:"de afrekening", fr:"le règlement"}, {t:6, nl:"contant betalen", fr:"payer au comptant"}, {t:6, nl:"beschikbaarheid checken", fr:"vérifier les dispos"}, {t:6, nl:"dienst na verkoop", fr:"le S.A.V."}, {t:6, nl:"bestelling plaatsen", fr:"passer commande"}, {t:6, nl:"de fraude", fr:"la fraude"}, {t:6, nl:"frauduleus", fr:"frauduleux"}, {t:6, nl:"geld verdienen", fr:"gagner de l'argent"}, {t:6, nl:"goedkoop", fr:"bon marché"}, {t:6, nl:"gratis", fr:"gratuit"}, {t:6, nl:"de handel", fr:"le commerce"}, {t:6, nl:"gamma is beperkt", fr:"la gamme est limitée"}, {t:6, nl:"hoge prijs", fr:"le prix élevé"}, {t:6, nl:"koper", fr:"l'acheteur"}, {t:6, nl:"korting", fr:"la réduction"}, {t:6, nl:"extra kosten", fr:"les frais"}, {t:6, nl:"lage prijs", fr:"le prix bas"}, {t:6, nl:"leveringstermijn", fr:"le délai de livraison"}, {t:6, nl:"met kaart betalen", fr:"payer par kaart"}, {t:6, nl:"het pakket", fr:"le colis"}, {t:6, nl:"de reservatie", fr:"la réservation"}, {t:6, nl:"reserveren", fr:"faire une résa"}, {t:6, nl:"snel", fr:"rapide"}, {t:6, nl:"goede kwaliteit", fr:"être de bonne qualité"}, {t:6, nl:"leveringsvoorwaarden", fr:"les conditions de vente"}, {t:6, nl:"voordelig", fr:"avantageux"},
    {t:7, nl:"de aankomst", fr:"l'arrivée"}, {t:7, nl:"antimuggenspray", fr:"le spray antimoustiques"}, {t:7, nl:"het baden", fr:"la baignade"}, {t:7, nl:"badlaken", fr:"la serviette de plage"}, {t:7, nl:"boarden", fr:"embarquer"}, {t:7, nl:"de boarding", fr:"l'embarquement"}, {t:7, nl:"bagage ophalen", fr:"récupérer les bagages"}, {t:7, nl:"dienst voor toerisme", fr:"le syndicat d'initiative"}, {t:7, nl:"Fijne vakantie!", fr:"Bonnes vacances!"}, {t:7, nl:"gelegen", fr:"situé"}, {t:7, nl:"de grens", fr:"la frontière"}, {t:7, nl:"handbagage", fr:"les bagages à main"}, {t:7, nl:"beter te reserveren", fr:"il vaut mieux"}, {t:7, nl:"de hoogte", fr:"l'altitude"}, {t:7, nl:"identiteitskaart", fr:"la carte d'identité"}, {t:7, nl:"goede reis!", fr:"bon voyage!"}, {t:7, nl:"inchecken", fr:"enregistrer"}, {t:7, nl:"in de buurt", fr:"à proximité"}, {t:7, nl:"in de tent slapen", fr:"dormir sous la tente"}, {t:7, nl:"de inlichting", fr:"le renseignement"}, {t:7, nl:"wildkamperen", fr:"le camping sauvage"}, {t:7, nl:"het kampvuur", fr:"le feu de camp"}, {t:7, nl:"het kasteel", fr:"le château"}, {t:7, nl:"de koffer", fr:"la valise"}, {t:7, nl:"komende uit", fr:"en provenance de"}, {t:7, nl:"het kompas", fr:"la boussole"}, {t:7, nl:"landen", fr:"atterrir"}, {t:7, nl:"logeren", fr:"loger"}, {t:7, nl:"luchtmatras", fr:"le matelas"}, {t:7, nl:"luchtvaartmij", fr:"la compagnie aérienne"}, {t:7, nl:"luidruchtig", fr:"bruyant"}, {t:7, nl:"bestemming", fr:"à destination de"}, {t:7, nl:"natuurpark", fr:"le parc naturel"}, {t:7, nl:"onthalen", fr:"accueillir"}, {t:7, nl:"openingsuren", fr:"les heures d'ouverture"}, {t:7, nl:"opstijgen", fr:"décoller"}, {t:7, nl:"overstappen", fr:"changer de train"}, {t:7, nl:"paspoortcontrole", fr:"le contrôle passeport"}, {t:7, nl:"reisdocumenten", fr:"les documents de voyage"}, {t:7, nl:"reistas", fr:"le sac de voyage"}, {t:7, nl:"reiziger", fr:"le voyageur"}, {t:7, nl:"vooraf reserveren", fr:"réserver à l'avance"}, {t:7, nl:"de rugzak", fr:"le sac à dos"}, {t:7, nl:"de slaapzak", fr:"le sac de couchage"}, {t:7, nl:"de stage, kamp", fr:"le stage"}, {t:7, nl:"standplaats", fr:"l'emplacement"}, {t:7, nl:"ticketautomaat", fr:"la borne"}, {t:7, nl:"duurzaam toerisme", fr:"le tourisme"}, {t:7, nl:"toestemming", fr:"l'autorisation"}, {t:7, nl:"toilettas", fr:"la trousse"}, {t:7, nl:"veiligheidscontrole", fr:"le contrôle de sûreté"}, {t:7, nl:"het verblijf", fr:"le séjour"}, {t:7, nl:"het vertrek", fr:"le départ"}, {t:7, nl:"vliegen", fr:"voler"}, {t:7, nl:"de vlucht", fr:"le vol"}, {t:7, nl:"wereldreis", fr:"le tour du monde"}, {t:7, nl:"het zicht", fr:"la vue"}, {t:7, nl:"koffer maken", fr:"faire sa valise"}, {t:7, nl:"tent opvouwen", fr:"replier sa tente"}, {t:7, nl:"tent opzetten", fr:"monter sa tente"}, {t:7, nl:"zonnecrème", fr:"la crème solaire"}, {t:7, nl:"het zonnen", fr:"le bain de soleil"}
];

let allSets = [];
let currentSetIdx = 0, wordIdx = 0, timeLeft = 8, isPaused = false, interval;

function generateSets(trajetNum) {
    const grid = document.getElementById('set-grid');
    grid.innerHTML = '';
    if (!trajetNum) return;

    // Filter woorden op het gekozen traject [cite: 1]
    const gefilterd = woordenLijst.filter(w => w.t == trajetNum);
    allSets = [];

    // Maak precies 10 sets van 14 woorden met 5 woorden overlap (stap van 9)
    for (let i = 0; i < 10; i++) {
        let start = i * 9;
        let set = gefilterd.slice(start, start + 14);
        
        // Als de lijst te kort is voor 10 sets, vullen we aan met het begin om aan 10 sets te komen
        if (set.length < 14 && gefilterd.length > 0) {
             set = [...set, ...gefilterd.slice(0, 14 - set.length)];
        }
        
        if (set.length > 0) allSets.push(set);
    }

    // Toon de sets in het menu
    allSets.forEach((set, i) => {
        const card = document.createElement('div');
        card.className = 'set-card';
        card.innerHTML = `
            <h3>Série ${i+1}</h3>
            <p style="color:#888; font-size:14px;">Trajet ${trajetNum} - ${set.length} woorden</p>
            <button class="btn" onclick="startSet(${i})">🚀 Starten</button>
        `;
        grid.appendChild(card);
    });
}

function startSet(idx) {
    currentSetIdx = idx; wordIdx = 0;
    document.getElementById('container').style.display = 'none';
    document.getElementById('exercise').style.display = 'flex';
    nextWord();
}

function nextWord() {
    const set = allSets[currentSetIdx];
    if (wordIdx >= set.length) { showResults(); return; }
    
    timeLeft = 8; 
    document.getElementById('word-display').innerText = set[wordIdx].nl;
    document.getElementById('info-header').innerText = `Série ${currentSetIdx+1} — Woord ${wordIdx+1}/${set.length}`;
    updateTimerBar();

    if (interval) clearInterval(interval);
    interval = setInterval(() => {
        if (!isPaused) {
            timeLeft--; 
            updateTimerBar();
            if (timeLeft <= 0) { 
                wordIdx++; 
                nextWord(); 
            }
        }
    }, 1000);
}

function updateTimerBar() {
    const bar = document.getElementById('timer-bar');
    bar.style.width = (timeLeft / 8 * 100) + '%';
    bar.style.backgroundColor = timeLeft < 3 ? 'var(--danger)' : 'var(--success)';
}

function togglePause() {
    isPaused = !isPaused;
    document.getElementById('pause-btn').innerText = isPaused ? "Hervatten" : "Pause";
}

function showResults() {
    clearInterval(interval);
    document.getElementById('exercise').style.display = 'none';
    document.getElementById('result').style.display = 'flex';
    document.getElementById('res-body').innerHTML = allSets[currentSetIdx].map(w => `
        <tr><td>${w.nl}</td><td style="color:var(--primary); font-weight:bold;">${w.fr}</td></tr>
    `).join('');
}
</script>

</body>
</html>