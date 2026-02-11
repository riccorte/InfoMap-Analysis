## Parte di teoria

### Il problema
Si consideri un generico network individuato da $n$ nodi e $m$ link, directed o undirected indifferentemente, weighted o unweighted indifferentemente. Se il network è molto grande, spesso è di interesse individuare delle *comunità* (o *moduli*) di nodi che riassumano in maniera rappresentativa il network (eliminando alcuni dettagli microscopici ritenuti inutili). Chiamasi organizzazione su mesoscala. 
Di fatto devo individuare una partizione sui nodi in comunità. Nota che in genere non sia conoscenza a priori del numero di gruppi esistono, dunque l'identificazione di questi moduli è NP-hard

Il numero di possibili modi per assegnare $N$ nodi in un generico non fissato numero di moduli è $B_N$ ed è tale per cui:
$$
B(x) \approx e^{e^x - 1}
$$
super-exponentially. Dunque non si può fare brute-forcing su ogni possibile partizione del network per ogni possibile numero di comunità. 

Comunque per ora il problema è mal posto. In base a cosa definisco un "gruppo" comunitario di nodi, secondo che criterio? In parte è il problema che ci poniamo. Esistono diversi modi di definire una comunità di nodi e ognuno riflette diverse interpretazioni del concetto. 

### Modularità $Q$ di Newman
Introdotta in *Newman, M. E. Detecting community structure in networks*. Considera una generica partizione del network, ossia un modo di assegnare tutti i nodi a comunità distinte. Allora calcola la *modularità*:
$$
Q = \frac{1}{2m}\sum_{i,j = 1}^N (A_{ij}-P_{ij}) \delta_{b_i, b_j}
$$
dove $A_{ij}$ è la matrice di adiacenza del network (matrice che è 1 se c'è collegamento fra nodo $i$ e $j$ altrimenti 0). Il termine $\delta_{b_i, b_j}$ riduce la somma ai soli indici di nodi per cui $b_i = b_j$ dove $b_i$ è la partizione di $i$ (dunque solo coppie nodi nella stessa partizione). Il termine $P_{ij}$ è la null probability, e cioè la probabilità che la connessione fra i e j esista per puro caso (secondo il meccanismo dinamico che genera il network). Questa dipende dalla null hypothesis che si fa, comunque la scelta più frequente (che corrisponde al configuration model e che fa anche Newman nel suo articolo) è:
$$
P_{ij} = \frac{k_i k_j}{2m}
$$
dove $k_i$ e $k_j$ sono i gradi (numeri di link) dei nodi $i$ e $j$. Data quindi una partizione generica, uno può calcolare il "funzionale" sul network $Q$. Se ho scelto una buona partizione, mi aspetto che $Q$ sia grande! Infatti nel termine di differenza sto calcolando (per i soli nodi che credo essere nello stesso gruppo) la loro connettività attuale, vera ($A_{ij}$) con quella che mi aspetto sotto una null hypothesis, se il network fosse random (la $P_{ij}$). Se le due sono molto diverse, allora è sto dicendo che c'è una probabilità (diversa da quella puramente casuale) che due nodi nella stessa comunità creino un link fra di loro. Tanto più alta è questa probabilità rispetto al caso puramente random, tanto più alta è la differenza $((A_{ij}-P_{ij}))$ all'interno delle comunità e tanto più alta è $Q$.
Ergo, per trovare una buona partizione de network, mi basta cercare fra tutte le partizioni e trovare quella che massimizza $Q$. Qua l'interpretazione che diamo al concetto di comunità è "nodi fortemente connessi fra nodi nella stessa comunità, meno connessi con nodi di altre comunità"

### Map equation
Nella tecnica di $Q$, definiamo la comunità come un insieme di nodi molto connessi fra di loro, molto più di quanto non lo siano con altre comunità. è dunque una definizione. Qua ne diamo una nuova, che conduce ad un nuovo funzionale (la map-equation). 
It has been shown that it is possible to use dynamical processes to unravel the mesoscale organization of a complex network. The rationale is based on the idea that some processes such as random walks can be used as a proxy for how information propagates through a system: nodes exchanging information more quickly are expected to be more likely to be part of the same module. Rosvall and Bergstrom have proposed another method for detecting communities, named Infomap (611), which is based on the analysis of the flow of random walks by means of techniques based on information theory