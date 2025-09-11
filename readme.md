Turinys

1. Sprendžiamo uždavinio aprašymas 3

1.1 Sistemos paskirtis 3

1.2 Funkciniai reikalavimai 3

2. Sistemos architektūra 4
Sprendžiamo uždavinio aprašymas
1.1 Sistemos paskirtis

Sistemos tikslas – suteikti galimybę vartotojams dalintis receptais, kaupti jų aprašymus, bei diskutuoti apie patiekalus. Sistema leis struktūruotai saugoti receptus, jų ingredientus ir vartotojų atsiliepimus.

Veikimo principas – pačią kuriamą platformą sudaro dvi dalys: internetinė aplikacija, kuria naudosis svečiai, nariai, administratorius bei aplikacijų programavimo sąsaja (angl. trump. API).

Prisijungęs ir prisiregistravęs narys, naudodamasis šia platforma galės kurti įvairius patiekalų receptus ir užpildyti ingredientus. Receptai saugomi „rich text“ (markdown) formatu, todėl kurdamas šiuos receptus narys gali juos gražiai formatuoti. Kiekvienas svečias, bei narys gali peržiūrėti kitų receptus ir palikti atsiliepimus. Nariai gali redaguoti savo sukurtus receptus ir paliktus atsiliepimus. Administratorius gali trinti receptus, bei atsiliepimus.
1.2 Funkciniai reikalavimai

Neregistruotas sistemos naudotojas galės:

    Prisijungti prie internetinės aplikacijos;
    Prisiregistruoti prie internetinės aplikacijos;
    Palikti anoniminius atsiliepimus;
    Peržiūrėti kitų naudotojų sukurtus receptus.

Registruotas sistemos naudotojas galės:

    Atsijungti nuo internetinės aplikacijos;
    Sukurti receptą:
        Užpildyti recepto instrukciją;
        Užpildyti ingredientų sąrašą;
        Užpildyti maistingumo informacijos lentelę;
    Peržiūrėti kitų naudotojų sukurtus receptus;
    Įvertinti kitų sukurtų naudotojų receptus;
    Redaguoti savo sukurtus receptus;
    Šalinti savo sukurtus receptus;
    Redaguoti savo sukurtus atsiliepimus;
    Šalinti savo sukurtus atsiliepimus.

Administratorius galės:

    Šalinti sukurtus receptus;
    Šalinti sukurtus atsiliepimus.

2. Sistemos architektūra

Sistemos sudedamosios dalys:

    Kliento pusė (ang. Front-End) – naudojant sveltejs (SvelteKit);
    Serverio pusė (angl. Back-End) – naudojant python FastAPI. Duomenų bazė – SQLite.

Sistemos talpinimui yra naudojamas Linux serveris. Kiekviena sistemos dalis yra diegiama tame pačiame serveryje. Internetinė aplikacija yra pasiekiama per HTTP protokolą. Šios sistemos veikimui (pvz., duomenų manipuliavimui su duomenų baze) yra reikalingas TasteHub API, kuris pasiekiamas per aplikacijų programavimo sąsają. Pats TasteHub API vykdo duomenų mainus su duomenų baze - tam naudojama ORM sąsaja. Kadangi SQLite neturi serverio, pats db.sql failas yra laikomas TasteHub API proceso veikimo aplanke.
