# ProjectCloudComputing


    În cadrul acestui proiect am implementat patru microservicii, numite „**songs**”, „**users**”, ”**likes_and_comments**” și „**favourites**”. Serviciul ”**songs**” conține expunerea pentru crearea bazei de date și a tabelelor ”songs” și ”artists”. Pe lângă acestea, serviciul conține metodele de adăugare și citire a artiștilor, respectiv cântecelor în baza de date. 
    
   Serviciul ”**users**” gestionează operațiile asupra utilizatorilor din aplicație. Un utilizator poate alege mai multe cântece favorite prin intermediul microserviciului ”favourites”. Acesta are posibilitatea de a își vizualiza melodiile favorite într-un tabel. 
Fiecare cântec poate primi like-uri și comentarii din partea utilizatorilor în funcție de opiniile acestora. Pentru fiecare cântec va fi afișat numărul de like-uri primite. 

    Aplicația conține o singură bază de date reprezentată de o imagine Docker MYSQL, numită mysqldb. Containerele sunt pornite folosind docker compose. 
   
**Tehnologii folosite pentru kubernetes**

    MicroK8s este un sistem open-source pentru automatizarea deploymenturilor, scalarea și gestionarea aplicațiilor containerizate. Oferă funcționalitatea principalelor componente Kubernetes, într-o amprentă redusă, scalabilă de la un singur nod la un cluster de producție.
    
    Helm este un instrument care ne ajută să definim, să instalam și să actualizam aplicațiile care rulează pe Kubernetes.Functionalitatea cea mai des utilizata pentru Helm este aceea a unui motor de șabloane care creează manifeste Kubernetes. Ceea ce îl face pe Helm mai mult decât atât este că poate face upgrade și scala și aplicațiile.
    
    Pentru partea de Kubernetes am folosit MicroK8s cu ajutorul căruia ne-am creat un cluster cu un nod local. De asemenea, MicroK8s are un registry de imagini de docker preinstalat pentru a face push de imagini cărora le-am făcut build inainte, iar apoi Kubernetes le preia pentru crearea containerelor. 
    
    Cu ajutorul Helm-ului am generat deployment-ul doar pentru partea ce ține de baza de date. Pe celelalte microservicii am făcut build și push pe registry, iar mai apoi am realizat deployment-ul și service-ul (ne-am definit un NodePort pentru fiecare microserviciu prin intermediul căruia avem acces la resursele noastre). 
